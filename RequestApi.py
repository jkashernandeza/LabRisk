import requests
import time
from tqdm import tqdm
import Keys

#Requests ####################################################################################
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {Keys.bToken}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r
def connect_to_endpoint(*url):
    response = requests.request("GET", url[0], auth=bearer_oauth, params=url[1])
    #print(response.status_code)
    if response.status_code == 429:
        for i in enumerate(tqdm(range(10000), desc = "Limit of Request reached, Waiting",position=0, leave=True)):
            time.sleep(0.0905)
            pass
        response = requests.request("GET", url[0], auth=bearer_oauth, params=url[1])
    elif response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()
##############################################################################################