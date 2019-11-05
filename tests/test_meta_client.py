from tempfile import NamedTemporaryFile

from garpunapiclient.client import GarpunApi
from garpunapiclient.http import MediaDownload
from garpunapiclient.model import MediaModel


def test_stream_pdf_response():
    api = GarpunApi.build("meta", "v1")

    request = api.get("/media/v/d9aecced-35e9-42b1-9143-a5abc7ef620e", model=MediaModel())

    source_file = NamedTemporaryFile(delete=False)
    media_download = MediaDownload(request, source_file)
    media_download.full_download()

    print("X")
    print(source_file.name)
