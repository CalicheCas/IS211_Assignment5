#!/usr/bin/env python3


class Request:

    def __init__(self, received_at, file, time_to_process):
        self.received_at = received_at
        self.file = file
        self.ttp = time_to_process

    def get_timestamp(self):
        return self.received_at

    def get_file(self):
        return self.file

    def wait_time(self):
        return int(self.ttp)
