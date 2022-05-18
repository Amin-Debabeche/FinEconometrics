def status(response):
    if not response.ok:
        raise Exception(response.status_code, response.text)