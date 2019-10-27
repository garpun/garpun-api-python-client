from garpunauth.client import GarpunCredentials

from garpunapiclient.client import GarpunApi


GarpunCredentials.authenticate_user(['cloud-platform', 'meta.dev'])

api = GarpunApi.build("trafficestimator", "v1")

resp, content = api.post("keyword/get", post_data={
    "keywords": [
        "bmw",
        "mersedes"
    ]
})
print(resp)
print(u"content = %s" % str(content))
