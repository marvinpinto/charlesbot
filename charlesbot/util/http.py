import asyncio
import aiohttp
import logging
log = logging.getLogger(__name__)


@asyncio.coroutine
def http_get_auth_request(auth_string,
                          url,
                          content_type="application/json",
                          auth_method="Token",
                          payload={}):
    headers = {
        'Content-type': content_type,
        'Authorization': "%s %s" % (auth_method, auth_string),
    }
    response = yield from aiohttp.get(url, headers=headers, params=payload)
    if not response.status == 200:
        text = yield from response.text()
        log.error("URL: %s" % url)
        log.error("Response status code was %s" % str(response.status))
        log.error(response.headers)
        log.error(text)
        response.close()
        return ""
    return (yield from response.text())


@asyncio.coroutine
def http_get_request(url, content_type="application/json"):
    headers = {
        'Content-type': content_type,
    }
    response = yield from aiohttp.get(url, headers=headers)
    if not response.status == 200:
        text = yield from response.text()
        log.error("URL: %s" % url)
        log.error("Response status code was %s" % str(response.status))
        log.error(response.headers)
        log.error(text)
        response.close()
        return ""
    return (yield from response.text())
