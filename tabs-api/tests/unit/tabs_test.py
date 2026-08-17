import pytest
from fastapi import status

from app.models.tab import Tab
import app.services.tab_services as tab_services

@pytest.mark.asyncio
async def test_get_tab_success(client, monkeypatch, fake_s3_client):
    fake_tab = Tab(
        id=1,
        song_name="Test Tab",
        artist="Test Artist",
        genre="rock",
        style="finger-picking",
        description="Test Description",
        lyrics_included=True,
        preview_file_key="test-file.mp3",
        file_name = "Test file name",
    )

    async def mock_get_tab_by_id(tab_id, session):
        return fake_tab

    monkeypatch.setattr(tab_services, "get_tab_by_id", mock_get_tab_by_id)

    response = await client.get("tabs/tab/1")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["id"] == fake_tab.id
    assert data["song_name"] == fake_tab.song_name
    assert data["artist"] == fake_tab.artist
    assert data["genre"] == fake_tab.genre
    assert data["style"] == fake_tab.style
    assert data["description"] == fake_tab.description
    assert data["lyrics_included"] == fake_tab.lyrics_included
    assert data["file_url"] == "https://fake-s3/test-file.mp3"
    assert data["file_name"] == fake_tab.file_name

@pytest.mark.asyncio
async def test_get_tabs_success(client, monkeypatch):
    fake_tabs = [
        Tab(
            id=1,
            song_name="Song A",
            artist="Artist A",
            genre="rock",
            style="strumming",
            description="Desc A",
            lyrics_included=False,
            file_key="fileA.mp3",
            file_name="File A"
        ),
        Tab(
            id=2,
            song_name="Song B",
            artist="Artist B",
            genre="metal",
            style="finger-picking",
            description="Desc B",
            lyrics_included=True,
            file_key="fileB.mp3",
            file_name="File B"
        ),
    ]

    async def mock_get_tabs(session, limit, offset):
        return fake_tabs

    monkeypatch.setattr(tab_services, "get_tabs", mock_get_tabs)

    response = await client.get("tabs/?limit=10&offset=0")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data) == 2

    assert data[0]["id"] == 1
    assert data[0]["song_name"] == "Song A"
    assert data[0]["artist"] == "Artist A"
    assert data[0]["genre"] == "rock"
    assert data[0]["style"] == "strumming"
    assert data[0]["description"] == "Desc A"
    assert data[0]["lyrics_included"] is False
    assert data[0]["file_name"] == "File A"

    assert data[1]["id"] == 2
    assert data[1]["song_name"] == "Song B"
    assert data[1]["artist"] == "Artist B"
    assert data[1]["genre"] == "metal"
    assert data[1]["style"] == "finger-picking"
    assert data[1]["description"] == "Desc B"
    assert data[1]["lyrics_included"] is True
    assert data[1]["file_name"] == "File B"

@pytest.mark.asyncio
async def test_get_tabs_by_genre_success(client, monkeypatch):
    fake_tabs = [
        Tab(
            id=1,
            song_name="Rock Song A",
            artist="Artist A",
            genre="rock",
            style="strumming",
            description="Desc A",
            lyrics_included=False,
            file_key="fileA.mp3",
            file_name="File A"
        ),
        Tab(
            id=2,
            song_name="Rock Song B",
            artist="Artist B",
            genre="rock",
            style="finger-picking",
            description="Desc B",
            lyrics_included=True,
            file_key="fileB.mp3",
            file_name="File B"
        )
    ]

    async def mock_get_tabs_by_genre(genre, session, limit, offset):
        return fake_tabs

    monkeypatch.setattr(
        tab_services,
        "get_tabs_by_genre",
        mock_get_tabs_by_genre
    )

    response = await client.get("tabs/genre/rock?limit=10&offset=0")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data) == 2

    assert data[0]["id"] == 1
    assert data[0]["song_name"] == "Rock Song A"
    assert data[0]["artist"] == "Artist A"
    assert data[0]["genre"] == "rock"
    assert data[0]["style"] == "strumming"
    assert data[0]["description"] == "Desc A"
    assert data[0]["lyrics_included"] is False
    assert data[0]["file_name"] == "File A"

    assert data[1]["id"] == 2
    assert data[1]["song_name"] == "Rock Song B"
    assert data[1]["artist"] == "Artist B"
    assert data[1]["genre"] == "rock"
    assert data[1]["style"] == "finger-picking"
    assert data[1]["description"] == "Desc B"
    assert data[1]["lyrics_included"] is True
    assert data[1]["file_name"] == "File B"

@pytest.mark.asyncio
async def test_get_tabs_by_genre_filters_wrong_genre(client, monkeypatch):
    fake_tabs = [
        Tab(
            id=1,
            song_name="Correct Song",
            artist="Artist",
            genre="rock",
            style="strumming",
            description="desc",
            lyrics_included=True,
            file_key="rock.mp3",
            file_name="rock file"
        ),
        Tab(
            id=2,
            song_name="Wrong Song",
            artist="Artist",
            genre="metal",
            style="strumming",
            description="desc",
            lyrics_included=False,
            file_key="metal.mp3",
            file_name="metal file"
        ),
    ]

    async def mock_get_tabs_by_genre(genre, session, limit, offset):
        return fake_tabs

    monkeypatch.setattr(tab_services, "get_tabs_by_genre", mock_get_tabs_by_genre)

    response = await client.get("tabs/genre/rock?limit=10&offset=0")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    for tab in data:
        assert tab["genre"] == "rock", "API returned a tab with the wrong genre!"

@pytest.mark.asyncio
async def test_get_tabs_by_style_filters_wrong_style(client, monkeypatch):
    fake_tabs = [
        Tab(
            id=1,
            song_name="Correct Style",
            artist="Artist",
            genre="rock",
            style="finger-picking",
            description="desc",
            lyrics_included=True,
            file_key="rock.mp3",
            file_name="rock file"
        ),
        Tab(
            id=2,
            song_name="Wrong Style",
            artist="Artist",
            genre="rock",
            style="strumming",
            description="desc",
            lyrics_included=False,
            file_key="metal.mp3",
            file_name="metal file"
        ),
    ]

    async def mock_get_tabs_by_style(style, session, limit, offset):
        return fake_tabs

    monkeypatch.setattr(tab_services, "get_tabs_by_style", mock_get_tabs_by_style)

    response = await client.get("tabs/style/finger-picking?limit=10&offset=0")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    for tab in data:
        assert tab["style"] == "finger-picking", "API returned a tab with the wrong style!"

    returned_styles = {tab["style"] for tab in data}
    assert "strumming" not in returned_styles