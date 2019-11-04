from garpunapiclient.client import GarpunApi


def test_json_response():
    api = GarpunApi.build("trafficestimator", "v1")

    resp = api.post("keyword/get", body_value={"keywords": ["bmw", "mersedes"]})

    print("XX")
    print("XX")
    print(resp)
