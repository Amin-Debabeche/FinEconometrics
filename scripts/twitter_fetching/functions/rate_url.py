def create_rate_url():
    search_url = "https://api.twitter.com/1.1/application/rate_limit_status.json"
    query_params = {'resources' : 'help,users,search,statuses'}
    return (search_url, query_params)

if __name__ == "__main__":
    create_rate_url()