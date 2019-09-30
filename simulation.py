#!/usr/bin/env python3

import queue
from Request import Request
from Server import Server
import csv
import io
import urllib.request
import argparse
import random

parser = argparse.ArgumentParser("Server simulation")
parser.add_argument(
    "url",
    help="url with csv content",
    type=str
)
parser.add_argument(
    "servers",
    help="Number of servers to instantiate",
    type=int
)

args = parser.parse_args()


def download_requests(url):
    """
    Function downloads csv content from a given
    url and returns a list of request objects.
    :param str url:
    :return: list
    """
    response = urllib.request.urlopen(url)
    data_reader = csv.reader(io.TextIOWrapper(response))
    requests = []
    for row in data_reader:
        requests.append(Request(row[0], row[1], row[2]))

    return requests


def simulate_one_server(filename):

    request_list = download_requests(filename)
    incoming_requests = queue.Queue()
    server = Server()
    waiting_time = []

    max_seconds = len(request_list)

    # Put 'incoming requests' on a queue
    for entry in request_list:
        incoming_requests.put(entry)

    for second in range(max_seconds):

        # add incoming requests to queue
        if not incoming_requests.empty():
            new_request = incoming_requests.get()
            print(incoming_requests.qsize())
            server.queue.put(new_request)

        # Process request in queue if server is not busy
        if (not server.busy()) and (not server.queue.empty()):
            next_request = server.queue.get()
            waiting_time.append(next_request.wait_time())
            server.start_next(next_request)

        server.tick()

        average_wait = sum(waiting_time) / len(waiting_time)

        print("Average Wait {:.2f} sec, {:3d} tasks remaining.".format(average_wait, server.queue.qsize()))


def simulate_many_servers(filename, servers):

    request_list = download_requests(filename)
    incoming_requests = queue.Queue()
    waiting_time = []

    # create servers
    server_list = []

    for num in range(servers):
        server_list.append(Server())

    max_seconds = len(request_list)

    # Put 'incoming requests' on a queue
    for entry in request_list:
        incoming_requests.put(entry)

    for second in range(max_seconds):

        # pick random server
        server = server_list[random.randint(1, len(server_list) - 1)]

        # add incoming requests to random queue
        if not incoming_requests.empty():
            new_request = incoming_requests.get()
            print(incoming_requests.qsize())
            server.queue.put(new_request)

        # Process request in queue if server is not busy
        if (not server.busy()) and (not server.queue.empty()):
            next_request = server.queue.get()
            waiting_time.append(next_request.wait_time())
            server.start_next(next_request)

        server.tick()

        average_wait = sum(waiting_time) / len(waiting_time)

        print("Average Wait {:.2f} sec, {:3d} tasks remaining.".format(average_wait, server.queue.qsize()))


def main(arguments):

    if len(arguments) == 1:
        simulate_one_server(arguments.filename)
    else:
        simulate_many_servers(arguments.filename, arguments.servers)


if __name__ == "__main__":
    main(args)
