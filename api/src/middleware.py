from fastapi import Request, Response
# from fastapi.responses import RedirectResponse
from typing import Callable

async def middleware(
    request: Request,
    next: Callable[[], Response]
):
    print(request.cookies.items())

    return next()