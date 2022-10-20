import asyncio
from datetime import timedelta
from typing import Union, Any
import requests
import aiohttp


class SafeRequest:

    _not_set = object()

    def __init__(self, timeout: Union[float, timedelta] = 3.0, default: Any = _not_set):
        self._timeout = timeout
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
            self._timeout = timeout_.seconds
        elif isinstance(timeout_, float):
            self._timeout = timeout_
        else:
            raise TypeError('Incorrect type of timeout')

    def _return_default(self):
        if self.default is self._not_set:
            raise
        else:
            return self.default

    async def _make_request_async(self, url):
        timeout = aiohttp.ClientTimeout(total=self._timeout)

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=timeout) as response:
                    text = await response.text()
                    return text
            except asyncio.exceptions.TimeoutError:
                return self._return_default()

    def invoke(self, url: str):
        result = asyncio.run(self._make_request_async(url))
        return result

    def __call__(self, url: str):
        try:
            response = requests.get(url, timeout=self.timeout)
        except requests.exceptions.Timeout:
            return self._return_default()

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            return self._return_default()
        else:
            return response.text


if __name__ == '__main__':
    sf = SafeRequest(timeout=0.01, default=False)
    # sf('https://afternoon-ravine-94298.herokuapp.com/api/v1/')
    print(sf('https://afternoon-ravine-94298.herokuapp.com/api/v1/'))
