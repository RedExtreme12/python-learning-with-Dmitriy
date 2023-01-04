from pprint import pprint
from datetime import timedelta
from typing import Union, Any
import requests
import asyncio
import aiohttp


class SafeRequest:

    _not_set = object()

    def __init__(self, timeout: Union[float, timedelta] = 3.0, default: Any = _not_set):
        self._timeout = None

        self.timeout = timeout
        self._default = default

    @property
    def timeout(self):
        return self._timeout

    @property
    def default(self):
        return self._default

    @timeout.setter
    def timeout(self, timeout_: Union[float, timedelta]):
        if isinstance(timeout_, timedelta):
            self._timeout = timeout_
        elif isinstance(timeout_, float):
            self._timeout = timedelta(seconds=timeout_)
        else:
            raise TypeError('Incorrect type of timeout')

    def _return_default(self):
        if self.default is self._not_set:
            raise
        return self.default

    async def _make_request_async(self, url):
        timeout = aiohttp.ClientTimeout(total=self.timeout.total_seconds())

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=timeout) as response:
                    text = await response.text()
                    return text
            except asyncio.exceptions.TimeoutError:
                return self._return_default()

    async def invoke(self, url: str):
        return await self._make_request_async(url)

    def __call__(self, url: str):
        try:
            response = requests.get(url, timeout=self.timeout.total_seconds())
        except requests.exceptions.Timeout:
            return self._return_default()

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if response.status_code == 404:
                return self._return_default()
            raise
        else:
            return response.content


if __name__ == '__main__':
    sf = SafeRequest(default=False, timeout=3.0)
    # sf.timeout = 2.0
    # sf('https://afternoon-ravine-94298.herokuapp.com/api/v1/')
    # asyncio.run(sf.invoke('https://afternoon-ravine-94298.herokuapp.com/api/v1/'))
    # print(sf('https://afternoon-ravine-94298.herokuapp.com/api/v1/'))
    pprint(sf('https://www.google.com/'))
