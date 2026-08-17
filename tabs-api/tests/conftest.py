import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db.session import get_session
from app.external_services.s3_client import get_s3_client

class FakeUser:
    def __init__(
        self,
        user_id: int = 1,
        email: str = "user@example.com",
        first_name: str = "Test",
        last_name: str = "User",
    ):
        self.id = user_id
        self.email = email
        self.password = "hashed-password"
        self.first_name = first_name
        self.last_name = last_name


@pytest_asyncio.fixture
def fake_user():
    def _factory(**kwargs):
        return FakeUser(**kwargs)
    return _factory

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://localhost:8000/api/v1"
    ) as ac:
        yield ac

@pytest_asyncio.fixture(autouse=True)
async def mock_db_session():
    """
    Automatically override get_session in all tests unless explicitly replaced.
    """
    async def _mock_get_session():
        yield None

    app.dependency_overrides[get_session] = _mock_get_session
    yield
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
def fake_s3_client():
    """
    Override the get_s3_client dependency with an in-memory fake so router
    tests don't have to reach into S3Client internals.
    """
    class FakeS3Client:
        def __init__(self):
            self.presigned_urls = {}
            self.deleted_keys = []

        def generate_presigned_url(self, object_name, expires_in=3600):
            return self.presigned_urls.get(object_name, f"https://fake-s3/{object_name}")

        async def upload_fileobj(self, object_name, file):
            pass

        def delete_object(self, object_name):
            self.deleted_keys.append(object_name)

    fake_client = FakeS3Client()

    app.dependency_overrides[get_s3_client] = lambda: fake_client
    yield fake_client
    app.dependency_overrides.pop(get_s3_client, None)

@pytest_asyncio.fixture
def mock_boto_client(monkeypatch):
    """
    Patch boto3.client so S3Client gets a mock instead of a real connection.
    """
    class MockS3:
        def __init__(self):
            self.generated_url = None
            self.upload_called = False
            self.deleted = False

        def generate_presigned_url(self, ClientMethod, Params, ExpiresIn):
            return f"https://fake-url/{Params['Key']}?expires={ExpiresIn}"

        def upload_fileobj(self, file_obj, bucket, object_name, ExtraArgs):
            self.upload_called = True

        def delete_object(self, Bucket, Key):
            self.deleted = True

    mock_s3 = MockS3()

    def mock_client(*args, **kwargs):
        return mock_s3

    monkeypatch.setattr("boto3.client", mock_client)
    return mock_s3