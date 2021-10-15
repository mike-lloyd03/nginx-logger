import pytest
from datetime import datetime, timezone, timedelta
from read_log import Request


class TestRequest:
    def setup(self):
        self.log_entry = '[14/Oct/2021:01:19:07 -0700] 2.56.59.237 - - "home.presidio.blue" "POST /boaform/admin/formLogin HTTP/1.1" 301 169 "http://75.84.172.74:80/admin/login.asp" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0" "-"'

        self.want = {
            "time": datetime(
                2021,
                10,
                14,
                1,
                19,
                7,
                tzinfo=timezone(timedelta(days=-1, seconds=61200)),
            ),
            "remote_ip": "2.56.59.237",
            "remote_user": None,
            "server_name": "home.presidio.blue",
            "request": "POST /boaform/admin/formLogin HTTP/1.1",
            "status_code": "301",
            "bytes_sent": "169",
            "http_referer": "http://75.84.172.74:80/admin/login.asp",
            "user_agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0",
            "http_x_forwarded_for": None,
        }
        with open("nginx.log", "r") as f:
            self.log_lines = f.readlines()

    def test_parsing(self):
        got = Request(self.log_entry)

        assert self.want["time"] == got.time
        assert self.want["remote_ip"] == got.remote_ip
        assert self.want["server_name"] == got.server_name
        assert self.want["request"] == got.request
        assert self.want["status_code"] == got.status_code
        assert self.want["bytes_sent"] == got.bytes_sent
        assert self.want["http_referer"] == got.http_referer
        assert self.want["user_agent"] == got.user_agent
        assert self.want["http_x_forwarded_for"] == got.http_x_forwarded_for

    def test_to_dict(self):
        got = Request(self.log_entry)
        assert self.want == got.to_dict()

    def test_no_error_on_logs(self):
        for log in self.log_lines:
            Request(log)
