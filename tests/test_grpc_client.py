import unittest

from garpun.apiclient.client import GarpunApi


class GarpunApiTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_key2param(self):
        api = GarpunApi.build("trafficestimator", "v1")

        resp, content = api.post("keyword/get", post_data={
            "keywords": [
                "bmw",
                "mersedes"
            ]
        })
        print(resp)
        print(u"content = %s" % str(content))
