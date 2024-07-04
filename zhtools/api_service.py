import functools
from collections.abc import Callable
from enum import StrEnum
from typing import Any, Awaitable, ClassVar
from urllib.parse import urljoin

from zhtools.config import config
from zhtools.exceptions import ModuleRequired

try:
    import httpx
except ImportError:
    raise ModuleRequired("httpx")


class NotSuccessResponse(Exception):
    def __init__(self, status_code: int, resp: httpx.Response):
        self.status_code = status_code
        self.resp = resp


class RequestParamError(Exception):
    pass


class RequestMethod(StrEnum):
    POST = "post"
    GET = "get"
    PUT = "put"
    DELETE = "delete"
    PATCH = "patch"


def API(
    method: RequestMethod, path: str, *params: str, **default: Any
) -> Callable[..., dict]:
    def _api(self: "Service", *args: str, **kwargs: Any) -> dict:
        data = {params[i]: arg for i, arg in enumerate(args)}
        data.update(kwargs)
        if set(data) != set(params):
            raise RequestParamError()

        for k, v in default.items():
            data.setdefault(k, v)
        return self._request(path, data=data, method=method)

    return _api


def AsyncAPI(
    method: RequestMethod, path: str, *params: str, **default: Any
) -> Callable[..., Awaitable[dict]]:
    async def _api(self: "Service", *args: str, **kwargs: Any) -> dict:
        data = {params[i]: arg for i, arg in enumerate(args)}
        data.update(kwargs)
        if set(data) != set(params):
            raise RequestParamError()

        for k, v in default.items():
            data.setdefault(k, v)
        return await self._async_request(path, data=data, method=method)

    return _api


PostAPI = functools.partial(API, RequestMethod.POST)
GetAPI = functools.partial(API, RequestMethod.GET)
PutAPI = functools.partial(API, RequestMethod.PUT)
DeleteAPI = functools.partial(API, RequestMethod.DELETE)
PatchAPI = functools.partial(API, RequestMethod.PATCH)
AsyncPostAPI = functools.partial(AsyncAPI, RequestMethod.POST)
AsyncGetAPI = functools.partial(AsyncAPI, RequestMethod.GET)
AsyncPutAPI = functools.partial(AsyncAPI, RequestMethod.PUT)
AsyncDeleteAPI = functools.partial(AsyncAPI, RequestMethod.DELETE)
AsyncPatchAPI = functools.partial(AsyncAPI, RequestMethod.PATCH)


class Service:
    """
    Simple way to define an api client.
    >>> class MyAPI(StrEnum):
    >>>     Login = '/api/v1/login/'
    >>>     GetUsers = '/api/v1/users/'
    >>> class MyApiService(Service):
    >>>     HOST = 'http://localhost:8000/'
    >>>     # sync api
    >>>     login: Callable[[str, str], dict] = PostAPI(MyAPI.Login, 'username', 'password', force=False)
    >>>     # async api
    >>>     get_user: Callable[[int, int], Awaitable[dict]] = AsyncGetAPI(MyAPI.GetUsers, 'page', 'size')
    sync api:
    >>> service = MyApiService()
    >>> service.login('admin', 'pwd')
    async api:
    >>> async def get_users(page: int, size: int):
    >>>    return await service.get_user(page, size)
    """

    HOST: ClassVar[str]
    TIMEOUT: ClassVar[int] = 5

    def prepare_request(
        self, data: dict | None, method: RequestMethod
    ) -> tuple[dict, dict]:
        return data or {}, {}

    def _request(
        self,
        path: str,
        method: RequestMethod = RequestMethod.POST,
        data: dict | None = None,
        form_data: dict | None = None,
    ) -> dict:
        data, headers = self.prepare_request(data, method)
        url = urljoin(self.HOST, path)
        params = json_data = None
        if method == RequestMethod.GET:
            params = data
        else:
            json_data = data

        config.log_info(f"http request: {url}, data: {data}")
        resp = httpx.request(
            method,
            url,
            params=params,
            json=json_data,
            data=form_data,
            timeout=self.TIMEOUT,
            headers=headers or None,
        )
        return self.handle_result(resp)

    async def _async_request(
        self,
        path: str,
        method: RequestMethod = RequestMethod.POST,
        data: dict | None = None,
        form_data: dict | None = None,
    ) -> dict:
        data, headers = self.prepare_request(data, method)
        url = urljoin(self.HOST, path)
        params = json_data = None
        if method == RequestMethod.GET:
            params = data
        else:
            json_data = data
        async with httpx.AsyncClient() as cli:
            resp = await cli.request(
                method,
                url,
                params=params,
                json=json_data,
                data=form_data,
                timeout=self.TIMEOUT,
                headers=headers or None,
            )
            return self.handle_result(resp)

    def handle_result(self, resp: httpx.Response) -> dict:
        if resp.status_code != 200:
            raise NotSuccessResponse(resp.status_code, resp)
        return resp.json()
