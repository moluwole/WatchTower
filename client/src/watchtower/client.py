from .utils import Display
from .exception import (
    FailedErrorLog,
    ValidationError,
    AuthenticationError,
    ServerNotFoundError,
)
from json.decoder import JSONDecodeError

import requests
import socket

BASE_URL = "http://localhost:5003"


class WatchTower(object):
    def __init__(self, base_url: str = BASE_URL):
        self.display = Display()

        self.base_url = base_url

        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "watchtower-client"}
        )

    @staticmethod
    def get_ip_address():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 1))
            ip_address = s.getsockname()[0]
        except Exception:
            ip_address = '127.0.0.1'
        finally:
            s.close()
        return ip_address

    def send_to_tower(
        self,
        service: str,
        error_message: str,
        stack_trace: str,
        number_range: int
    ) -> bool:
        json = {
            "clientIp": self.get_ip_address(),
            "service": service,
            "errorMessage": error_message,
            "stackTrace": stack_trace,
            "numberRange": number_range
        }


        response = self.session.post(f"{self.base_url}/save", json=json)

        if response.status_code == requests.status_codes.codes.unauthorized:
            raise AuthenticationError("Invalid token", response.json())

        if response.status_code == requests.status_codes.codes.bad_request:
            raise ValidationError("Bad Request", response.json())

        try:
            res = response.json()
        except JSONDecodeError:
            raise ServerNotFoundError()

        if bool(res["success"]):
            self.display.print("SUCCESS", res['message'])
        else:
            raise FailedErrorLog()

    def view_errors(self):
        pass

    def search(self, param, offset=0, page_count=10):
        json = {

        }
