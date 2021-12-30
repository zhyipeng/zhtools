from __future__ import annotations

import functools
import logging
from enum import Enum
from typing import Optional
from urllib.parse import urljoin

import aiohttp
import requests

from zhtools.exceptions import (ExternalServiceError,
                                NotFoundError,
                                ParameterError, PermissionDenied,
                                ResponseIsNotJSONable,
                                Unauthorized, UnknownServiceError)


class APIPath(Enum):
    pass


class RequestMethod(Enum):
    POST = 'post'
    GET = 'get'
    PUT = 'put'


def API(method: RequestMethod,
        api: APIPath,
        *params: str,
        **default):
    def _api(self: 'Service', *args, **kwargs):
        data = {params[i]: arg for i, arg in enumerate(args)}
        data.update(kwargs)
        if set(data) != set(params):
            raise ParameterError()

        data.update(default)
        return self._request(api, data=data, method=method)
    return _api


def AsyncAPI(method: RequestMethod,
             api: APIPath,
             *params: str,
             **default):
    async def _api(self: Service, *args, **kwargs):
        data = {params[i]: arg for i, arg in enumerate(args)}
        data.update(kwargs)
        if set(data) != set(params):
            raise ParameterError()

        data.update(default)
        return await self.async_request(api, data=data, method=method)
    return _api


PostAPI = functools.partial(API, RequestMethod.POST)
GetAPI = functools.partial(API, RequestMethod.GET)
AsyncPostAPI = functools.partial(AsyncAPI, RequestMethod.POST)
AsyncGetAPI = functools.partial(AsyncAPI, RequestMethod.GET)


class Service:
    """
    Simple way to define an api client.
    >>> class MyAPI(API):
    >>>     Login = '/api/v1/login/'
    >>>     GetUsers = '/api/v1/users/'
    >>> class MyApiService(Service):
    >>>     HOST = 'http://localhost:8000/'
    >>>     # sync api
    >>>     login = PostAPI(MyAPI.Login, 'username', 'password', force=False)
    >>>     # async api
    >>>     get_user = AsyncGetAPI(MyAPI.GetUsers, 'page', 'size')
    sync api:
    >>> service = MyApiService()
    >>> service.login('admin', 'pwd')
    async api:
    >>> async def get_users(page: int, size: int):
    >>>    return await service.get_user(page, size)
    """
    HOST = None

    def prepare_request(self,
                        data: Optional[dict],
                        method: RequestMethod) -> tuple[dict, dict]:
        return data or {}, {}

    def _request(self,
                 api: APIPath,
                 method: RequestMethod = RequestMethod.POST,
                 data: dict = None,
                 form_data: dict = None):
        data, headers = self.prepare_request(data, method)
        url = urljoin(self.HOST, api.value)
        params = _data = None
        if method == RequestMethod.GET:
            params = data
        else:
            _data = data

        logging.info('http request: %s, data: %s', url, data)
        resp: requests.Response = requests.request(method.value,
                                                   url,
                                                   params=params,
                                                   json=_data,
                                                   data=form_data,
                                                   timeout=5,
                                                   headers=headers or None)
        if resp.status_code == 404:
            logging.info('response got 404: %s', resp.url)
            raise NotFoundError()
        elif resp.status_code == 401:
            raise Unauthorized()
        elif resp.status_code == 400:
            raise ParameterError()
        elif resp.status_code == 403:
            raise PermissionDenied()
        elif resp.status_code >= 500:
            raise ExternalServiceError(error_code=str(resp.status_code))
        elif resp.status_code >= 400:
            logging.info('response got 4xx: %s', resp.content)
            raise UnknownServiceError(error_code=str(resp.status_code))

        try:
            ret = resp.json()
        except Exception:
            raise ResponseIsNotJSONable()

        return self.handle_result(ret)

    async def async_request(self,
                            api: APIPath,
                            method: RequestMethod = RequestMethod.POST,
                            data: dict = None,
                            form_data: dict = None):
        data, headers = self.prepare_request(data, method)
        url = urljoin(self.HOST, api.value)
        params = _data = None
        if method == RequestMethod.GET:
            params = data
        else:
            _data = data

        logging.info('async http request: %s, data: %s', url, data)
        async with aiohttp.ClientSession() as session:
            async with session.request(method.value,
                                       url,
                                       params=params,
                                       json=_data,
                                       data=form_data,
                                       timeout=5,
                                       headers=headers or None) as resp:
                if resp.status == 404:
                    logging.info('response got 404: %s', resp.url)
                    raise NotFoundError()
                elif resp.status == 401:
                    raise Unauthorized()
                elif resp.status == 400:
                    raise ParameterError()
                elif resp.status == 403:
                    raise PermissionDenied()
                elif resp.status >= 500:
                    raise ExternalServiceError(error_code=str(resp.status))
                elif resp.status >= 400:
                    logging.info('response got 4xx: %s', resp.content)
                    raise ExternalServiceError(error_code=str(resp.status))

                try:
                    ret = await resp.json()
                except Exception:
                    raise ResponseIsNotJSONable()

                return self.handle_result(ret)

    def handle_result(self, result: dict):
        return result
