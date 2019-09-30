#!/usr/bin/env python3

import queue


class Server:

    def __init__(self):
        self.current_request = None
        self.time_remaining = 0
        self.queue = queue.Queue()

    def tick(self):
        if self.current_request is not None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_request = None

    def busy(self):
        if self.current_request is None:
            return False
        else:
            return True

    def start_next(self, new_request):
        self.current_request = new_request
        self.time_remaining = new_request.wait_time()





