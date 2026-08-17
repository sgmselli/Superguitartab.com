from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.business_logic.tab_uploader import TabUploader
from app.constants.genre import Genre
from app.constants.style import Style
from app.exceptions.s3 import S3ClientException
from app.exceptions.tab import IncorrectFileType
from app.external_services.s3_client import S3Client, get_s3_client
from app.models.user import User
from app.services import tab_services
from app.schema.tab import TabResponse, TabFileUrlResponse
from app.db.session import get_session
from app.constants.http_error_codes import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from app.services.tab_services import register_user_tab_download
from app.utils.auth.current_user import get_current_user_or_raise_http_error, get_current_user_or_return_none
from app.utils.logging import Logger, LogLevel

router = APIRouter()

@router.get("/tab/{tab_id}", response_model=TabResponse)
async def get_tab(
    tab_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user_or_return_none),
    s3_client: S3Client = Depends(get_s3_client),
):
    """
    Route to fetch tab by id and return it.
    """
    tab = await tab_services.get_tab_by_id(tab_id, session)
    if not tab:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Tab not found")

    try:
        if current_user:
            presigned_url = s3_client.generate_presigned_url(tab.file_key)
        else:
            presigned_url = s3_client.generate_presigned_url(tab.preview_file_key)
    except S3ClientException:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Failed to get tab")
    
    tab_response = TabResponse.model_validate(tab)
    tab_response.file_url = presigned_url
    return tab_response

@router.get("/tab/{tab_id}/download")
async def get_tab(
    tab_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user_or_raise_http_error),
    s3_client: S3Client = Depends(get_s3_client),
):
    """
    Route to fetch tab file url and increment downloads
    """
    tab = await tab_services.get_tab_by_id(tab_id, session)
    if not tab:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Tab not found")

    try:
        presigned_url = s3_client.generate_presigned_url(tab.file_key)
    except S3ClientException:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Failed to download tab")

    await register_user_tab_download(current_user.id, tab_id, session)

    return TabFileUrlResponse(file_url=presigned_url)

@router.get("/", response_model=list[TabResponse])
async def get_tabs(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    """
    Route to fetch all tabs of a specific genre with pagination.
    """
    return await tab_services.get_tabs(session, limit, offset)

@router.get("/genre/{genre}", response_model=list[TabResponse])
async def get_tabs_by_genre(
    genre: Genre,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    """
    Route to fetch all tabs of a specific genre with pagination.
    """
    tabs = await tab_services.get_tabs_by_genre(genre, session, limit, offset)
    return [tab for tab in tabs if tab.genre == genre]

@router.get("/style/{style}", response_model=list[TabResponse])
async def get_tabs_by_style(
    style: Style,
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    """
    Route to fetch all tabs of a specific style with pagination.
    """
    tabs = await tab_services.get_tabs_by_style(style, session, limit, offset)
    return [tab for tab in tabs if tab.style == style]

@router.post("/upload", status_code=HTTP_201_CREATED)
async def upload_tab_pdf(
    song_name: str = Form(...),
    artist: str = Form(...),
    tab_pdf_original: UploadFile = File(...),
    tab_pdf_preview: UploadFile = File(...),
    tab_thumbnail: UploadFile = File(...)
):
    """
    Upload a tab file to s3 bucket.
    """
    tab_uploader = TabUploader(song_name, artist)
    try:
        await tab_uploader.upload_tab_original(tab_pdf_original)
        await tab_uploader.upload_tab_preview(tab_pdf_preview)
        await tab_uploader.upload_tab_thumbnail(tab_thumbnail)

    except IncorrectFileType as e:
        tab_uploader.rollback_uploads()
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

    except S3ClientException:
        tab_uploader.rollback_uploads()
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload tabs")

    return {
        "id": None,
        "song_name": song_name,
        "artist": artist,
        "album": None,
        "genre": None,
        "style": None,
        "difficulty": None,
        "description": None,
        "lyrics_included": None,
        "file_key": tab_uploader.get_s3_tab_original_file_key(),
        "file_name": tab_uploader.get_file_name(),
        "downloads": 0,
        "preview_file_key": tab_uploader.get_s3_tab_preview_file_key(),
        "thumbnail_file_key": tab_uploader.get_s3_tab_thumbnail_file_key()
    }

@router.get("/search", response_model=list[TabResponse])
async def search_tabs(
    query: str,
    session: AsyncSession = Depends(get_session)
):
    return await tab_services.search_tabs(query, session)