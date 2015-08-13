import asynctest
from asynctest.mock import call
from asynctest.mock import patch
from asynctest.mock import CoroutineMock


class TestGetAuthRequest(asynctest.TestCase):

    def setUp(self):
        patcher = patch('charlesbot.util.http.aiohttp.get')
        from charlesbot.util.http import http_get_auth_request
        self.http_get_auth_request = http_get_auth_request
        self.addCleanup(patcher.stop)
        self.mock_aiohttp_get = patcher.start()

    def test_non_200_response(self):
        response = CoroutineMock()
        response.status = 201
        response.text.return_value = "this is my return value"
        self.mock_aiohttp_get.side_effect = [response]
        retval = yield from self.http_get_auth_request("sekrit",
                                                       "https://www.example.com")  # NOQA
        expected = call('https://www.example.com',
                        headers={
                            'Authorization': 'Token sekrit',
                            'Content-type': 'application/json'
                        },
                        params={})
        self.assertEqual(self.mock_aiohttp_get.mock_calls, [expected])
        self.assertEqual(response.close.mock_calls, call())
        self.assertEqual(retval, "")

    def test_200_response(self):
        response = CoroutineMock()
        response.status = 200
        response.text.return_value = "this is my return value"
        self.mock_aiohttp_get.side_effect = [response]
        retval = yield from self.http_get_auth_request("sekrit",
                                                       "https://www.example.com")  # NOQA
        expected = call('https://www.example.com',
                        headers={
                            'Authorization': 'Token sekrit',
                            'Content-type': 'application/json'
                        },
                        params={})
        self.assertEqual(self.mock_aiohttp_get.mock_calls, [expected])
        self.assertEqual(response.close.mock_calls, [])
        self.assertEqual(retval, "this is my return value")
