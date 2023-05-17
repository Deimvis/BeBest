import requests
from contextlib import contextmanager
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from typing import Dict, Generator

from lib.utils.functools import max_calls_per_second
from .base import RequesterBase


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class DefaultRequester(RequesterBase):
    TIMEOUT = 10
    RETRIES = 3
    RETRIES_DELAY_S = 1
    MAX_RPS = 10

    def __init__(self,
                 *args,
                 timeout=TIMEOUT,
                 retries=RETRIES,
                 retries_delay_s=RETRIES_DELAY_S,
                 max_rps=MAX_RPS,
                 **kwargs):
        self.timeout = timeout
        self.retries = retries
        self.retries_delay_s = retries_delay_s
        self.rps_limiter = max_calls_per_second(max_rps)
        super().__init__(*args, **kwargs)

    def request(self, method, url, **kwargs) -> requests.Response:
        @self.rps_limiter
        def do_request():
            request_kwargs = self._update_request_kwargs(**kwargs)
            return self._raw_request_with_retries(method, url, self.retries, self.retries_delay_s, **request_kwargs)
        return do_request()

    def _update_request_kwargs(self, **kwargs) -> Dict:
        kwargs['timeout'] = self.timeout
        return kwargs

    @contextmanager
    def update(self, timeout=None, retries=None, retries_delay_s=None) -> Generator['DefaultRequester', None, None]:
        cur_timeout = self.timeout
        cur_retries = self.retries
        cur_retries_delay_s = self.retries_delay_s
        try:
            self.timeout = timeout or self.timeout
            self.retries = retries or self.retries
            self.retries_delay_s = retries_delay_s or self.retries_delay_s
            yield self
        finally:
            self.timeout = cur_timeout
            self.retries = cur_retries
            self.retries_delay_s = cur_retries_delay_s
