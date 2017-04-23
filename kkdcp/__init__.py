import asyncio
from aiohttp import web
from kkdcp import codec

__version__ = "0.1.0"

# Maximum length we handle is 128 kB
MAX_LENGTH = 128 * 1024


async def handle_kkdcp(request):

    length = request.content_length
    if length is None:
        raise web.HTTPLengthRequired(text="Length is required.")
    if length > MAX_LENGTH:
        raise web.HTTPRequestEntityTooLarge(text="Request is too large.")

    try:
        data = await request.read()
        proxy_request = codec.decode(data)
    except codec.ParserError as e:
        raise web.HTTPBadRequest(text=str(e))

    loop = asyncio.get_event_loop()

    # TODO: Change this to look up the KDC to talk to
    try:
        krb5_response = await asyncio.wait_for(forward_kerberos(proxy_request.message, loop=loop), timeout=15, loop=loop)
    except asyncio.TimeoutError:
        raise web.HTTPServiceUnavailable(text="Timeout waiting for Kerberos server")

    return web.Response(body=codec.encode(krb5_response), content_type="application/kerberos")


async def forward_kerberos(data: bytes, loop=None) -> bytes:
    """"Forward a proxy request to a kerberos server and return the response"""
    reader, writer = await asyncio.open_connection('kdc.demo.kblin.org', 88, loop=loop)
    writer.write(data)
    resp = await reader.read()
    return resp


app = web.Application()
app.router.add_post("/", handle_kkdcp)
