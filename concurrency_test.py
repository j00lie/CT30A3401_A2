import xmlrpc.client
import concurrent.futures


def send_request(topic_name):
    with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
        notes = proxy.get_notes(topic_name)
    print(f"Notes for {topic_name}: {notes}\n")


if __name__ == "__main__":
    topic_names = ["test1", "test2"]  # hardcode testing values from xml mock db
    num_requests = 10
    # ThreadPoolExecutor creates a thread pool that can be used to execute tasks concurrently.

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(num_requests):
            topic_name = topic_names[
                i % len(topic_names)
            ]  # Cycle through list repetedly using modulo
            future = executor.submit(
                send_request, topic_name
            )  # submits a callable to the thread pool for execution
            futures.append(future)

        # After all requests have been submitted, another loop runs over the futures list
        # and waits for each future to complete using the concurrent.futures.as_completed() method.
        # This method yields futures as they complete to process results as they're available,
        # rather than waiting for all requests to complete.

        for future in concurrent.futures.as_completed(futures):
            # The result() method is called on each completed Future
            # to get the return value from send_request
            result = future.result()
            # process result if needed
