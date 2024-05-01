from fastapi import FastAPI, APIRouter, Request, Response
from typing import Callable, Any, Coroutine
from fastapi.middleware.cors import CORSMiddleware

class FAST_APP:
    def __init__(
        self,
        routers: list[APIRouter] = [],
        middleware: Callable[
            [
                Request,
                Callable[[], Response]
            ],
            Coroutine[Any, Any, Response]
        ] | None = None,
    ):
        self.app = FastAPI()
        self.middleware = middleware
        self.routers = routers

        self.__load_middleware__()
        self.__load_routers__()

    def __load_routers__(self):
        for router in self.routers:
            self.app.include_router(router)

    def __load_middleware__(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.app.middleware("http")(self.__middleware__)

    async def __middleware__(self, request: Request, call_next: Callable[[Request], Coroutine[Any, Any, Response]]):
        response = await call_next(request)
        
        def next():
            return response
        
        new_response = await self.middleware(request, next) if self.middleware else response
        
        return new_response

    def get_app(self):
        return self.app