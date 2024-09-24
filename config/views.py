import asyncio

from django.http.response import StreamingHttpResponse


async def iterable_content():
    for _ in range(5):
        await asyncio.sleep(1)
        yield b"a" * 10000


def test_stream_view(request):
    return StreamingHttpResponse(iterable_content())
