import datetime
import time
import sys

def throttling(response):
    remaining = int(response.headers["x-rate-limit-remaining"])
    if remaining <= 1:
        reset = response.headers["x-rate-limit-reset"]
        wait = (reset - datetime.now()).seconds
        print(f"One request from being rate limited. Waiting on Twitter.\n\tResume Time: {reset}")
        time.sleep(wait+5)
        return
    time.sleep(1)
    
if __name__ == "__main__":
    response = sys.argv[1]
    throttling(response)