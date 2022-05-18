import datetime
import time

def throttling(response):
    reset = response.headers["x-rate-limit-reset"]
    wait = int(reset) - int(datetime.datetime.now().strftime(format='%s'))
    print(f"One request from being rate limited. Waiting on Twitter.\n\tResume Time: {reset}")
    time.sleep(wait+5)
    return
