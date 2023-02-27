# This test is from here: https://stackoverflow.com/questions/53621682/multi-threaded-xml-rpc-python3-7-1
# see in-depth commenting in concurrency_test.py

import xmlrpc.client
from concurrent.futures import ThreadPoolExecutor, as_completed


def submit_sleep():
    server = xmlrpc.client.ServerProxy("http://localhost:8000/", allow_none=True)
    return server.sleep()


with ThreadPoolExecutor() as executor:
    sleeps = {executor.submit(submit_sleep) for _ in range(4)}
    for future in as_completed(sleeps):
        sleep_time = future.result()
        print(sleep_time)
