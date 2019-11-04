from garpunapiclient.client import GarpunApi


def test_key2param():
    api = GarpunApi.build("trafficestimator", "v1")

    resp = api.post("keyword/get", post_data={"keywords": ["bmw", "mersedes"]})
    print(resp)
    print(u"content = %s" % str(resp.text))
