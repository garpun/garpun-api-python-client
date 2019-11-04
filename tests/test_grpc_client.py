from garpunapiclient.client import GarpunApi


def test_key2param():
    api = GarpunApi.build("trafficestimator", "v1")

    resp, content = api.post("keyword/get", post_data={"keywords": ["bmw", "mersedes"]})
    print(resp)
    print(u"content = %s" % str(content))
