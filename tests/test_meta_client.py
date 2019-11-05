from tempfile import NamedTemporaryFile

from garpunapiclient.client import GarpunApi
from garpunapiclient.http import MediaDownload
from garpunapiclient.model import MediaModel


def test_stream_pdf_response():
    api = GarpunApi.build("meta", "v1")

    request = api.get(
        "/media/v/d9aecced-35e9-42b1-9143-a5abc7ef620e", model=MediaModel()
    )

    source_file = NamedTemporaryFile(delete=False)
    media_download = MediaDownload(request, source_file)
    media_download.full_download()

    print(source_file.name)


def test_stream_metaql_response():
    api = GarpunApi.build("meta", "v1")

    q = """
    SELECT
      engine as platform,
      campaign_remote_id,
      SUM(impressions) as impressions,
      SUM(clicks) as clicks,
      1.0 * SUM(clicks) / NULLIF(SUM(impressions), 0) * 100 as ctr,
      ROUND(SUM(cost), 3) as cost
    FROM adplatform.campaign_stats_report
    WHERE stat_date BETWEEN '2017-03-01' AND '2017-03-02'
    GROUP BY platform, campaign_remote_id
    ORDER BY platform, campaign_remote_id
    """

    configuration = {
        "download": {
            # "skipHeaders": True,
            "dbQuery": {"command": q}
        }
    }

    request = api.post(
        "/meta/metaql/download-data", body_value=configuration, model=MediaModel()
    )

    source_file = NamedTemporaryFile(delete=False)
    media_download = MediaDownload(request, source_file)
    media_download.full_download()

    print("X")
    print(source_file.name)
