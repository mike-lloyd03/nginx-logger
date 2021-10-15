import re
from datetime import datetime


class Request:
    def __init__(self, raw_log):
        pattern = r'^\[(?P<time>.+)\] (?P<remote_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - (?P<remote_user>\S+) "(?P<server_name>[^"]+)" "(?P<request>[^"]*)" (?P<status_code>\d{3}) (?P<bytes_sent>\d+) "(?P<http_referer>[^"]+)" "(?P<user_agent>[^"]+)"'

        match = re.search(pattern, raw_log)

        time = match.group("time")
        self.time = datetime.strptime(time, "%d/%b/%Y:%H:%M:%S %z")
        self.remote_ip = match.group("remote_ip")
        self.remote_user = match.group("remote_user")
        self.server_name = match.group("server_name")
        self.request = match.group("request")
        self.status_code = match.group("status_code")
        self.bytes_sent = match.group("bytes_sent")
        self.http_referer = match.group("http_referer")
        self.user_agent = match.group("user_agent")

    def to_dict(self):
        return self.__dict__


class RequestList:
    def __init__(self):
        self.items = []

    def append(self, request):
        self.items.append(request)

    def to_list(self):
        return [req.to_dict() for req in self.items]
