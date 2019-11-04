import shutil
from tempfile import NamedTemporaryFile

from garpunapiclient.client import GarpunApi
from garpunapiclient.model import MediaModel


def test_stream_response():
    api = GarpunApi.build("meta", "v1")

    response = api.get("/media/v/d9aecced-35e9-42b1-9143-a5abc7ef620e", model=MediaModel())
    response.raw.decode_content = True  # без этого файлы с mime application/json фигово скачиваются
    source_file = NamedTemporaryFile(delete=False)
    print("source_file.name = %s" % str(source_file.name))
    with open(source_file.name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
