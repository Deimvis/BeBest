import logging
import pprint
import requests
import traceback
from abc import ABC, abstractmethod
from typing import Dict, Optional

from lib.utils.functools import try_while


class RequesterBase(ABC):

    @abstractmethod
    def request(self, method, url, **kwargs) -> requests.Response:
        pass

    def get(self, *args, **kwargs):
        return self.request('get', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request('post', *args, **kwargs)

    def _raw_request_with_retries(self, method, url, max_retries, sleep_time_s, **kwargs) -> requests.Response:
        response = None

        def make_request():
            nonlocal response
            response = self._try_raw_request(method, url, **kwargs)

        try_while(while_=lambda: response is None,
                  sleep_time_s=sleep_time_s, max_retries=max_retries, max_retries_error_msg=f'Failed to make request {max_retries} times')(
            make_request
        )()
        return response

    def _try_raw_request(self, method, url, **kwargs) -> Optional[requests.Response]:
        try:
            response = self._raw_request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except Exception as error:
            self._on_failed_request(error)
        return None

    def _raw_request(self, method, url, **kwargs) -> requests.Response:
        return requests.request(method, url, **kwargs)

    def _on_failed_request(self, error: Exception, arguments: Dict = None):
        logging.debug(f'Failed to make request: {error}\n',
                      f'Arguments:\n {pprint.pformat(arguments, indent=2)}\n',
                      f'Traceback:\n {traceback.format_exc()}')
