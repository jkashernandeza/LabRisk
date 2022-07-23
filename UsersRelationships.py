import requests
import time
import json
from tqdm import tqdm
from datetime import datetime

#User info ####################################################################################
def getUserInfo(user_id):
    # Replace with user ID below
    return "https://api.twitter.com/2/users/{}".format(user_id)
def get_paramsUserInfo():
    return {"user.fields": "public_metrics"}
##############################################################################################

#Followers list ##############################################################################
def getFollowers(user_id):
    # Replace with user ID below
    return "https://api.twitter.com/2/users/{}/followers?max_results=1000".format(user_id)
def get_paramsFollowers():
    return {"user.fields": "id"}
##############################################################################################

#Following list ##############################################################################
def getFollowing(user_id):
    # Replace with user ID below
    return "https://api.twitter.com/2/users/{}/following?max_results=1000".format(user_id)
def get_paramsFollowing():
    return {"user.fields": "id"}
##############################################################################################

#Requests ####################################################################################
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bToken}"
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

#Getting followers list ######################################################################
def fetchingFollowers(userInfo):
    n = json.dumps(userInfo["data"]["public_metrics"]["followers_count"])
    loop = (int(int(n)/1000))+1
    try:
        del followersList
    except Exception:
        pass
    followersList = []
    urlFollowers = getFollowers(userInfo["data"]["id"])
    paramsFollowers = get_paramsFollowers()
    for i in range(loop):
        if i == 0:
            #print(urlFollowers, paramsFollowers)
            followers = connect_to_endpoint(urlFollowers, paramsFollowers)
            #print(json.dumps(followers["data"]))
            for x in followers["data"]:
                followersList.append(x['id'])
                
            try:
                nextToken = (json.dumps(followers["meta"]["next_token"])).replace('"','')
                #print(nextToken)
            except Exception:
                pass
        else:
            new = urlFollowers+"&pagination_token="+nextToken
            aux = connect_to_endpoint(new, paramsFollowers)
            #print(json.dumps(aux))
            for x in aux["data"]:
                followersList.append(x['id'])
    #print(len(followersList))
    #print(followersList)
    return followersList
##############################################################################################

#Getting following list ######################################################################
def fetchingFollowing(userInfo):
    n = json.dumps(userInfo["data"]["public_metrics"]["following_count"])
    loop = (int(int(n)/1000))+1
    try:
        del followingList
    except Exception:
        pass
    followingList = []
    urlFollowing = getFollowing(userInfo["data"]["id"])
    paramsFollowing = get_paramsFollowing()
    for i in range(loop):
        if i == 0:
            #print(urlFollowing, paramsFollowing)
            following = connect_to_endpoint(urlFollowing, paramsFollowing)
            #print(json.dumps(following["data"]))
            for x in following["data"]:
                followingList.append(x['id'])
                
            try:
                nextToken = (json.dumps(following["meta"]["next_token"])).replace('"','')
                #print(nextToken)
            except Exception:
                pass
        else:
            new = urlFollowing+"&pagination_token="+nextToken
            aux = connect_to_endpoint(new, paramsFollowing)
            #print(json.dumps(aux))
            for x in aux["data"]:
                followingList.append(x['id'])
    #print(len(followingList))
    #print(followingList)
    return followingList
##############################################################################################

def main():    
    #userID = 1027925857392885761 #JuanC
    #userID = 1673751446 #Ketra
    #users = [1673751446,1027925857392885761]
    str_date_time = datetime.now().strftime("%d_%m_%y_%H%M%S%f")[:-6]
    u=open("H:/My Drive/jkas/Mitacs/LabRisk/TwitterApi/users.json")
    users = json.load(u)
    node = {}
    for band, userID in enumerate(tqdm(users, desc = "Fetching")):
        userInfo = connect_to_endpoint(getUserInfo(userID["id"]),get_paramsUserInfo())
        node = {"userID" : userID["id"], "followers" : fetchingFollowers(userInfo), 
        "following" : fetchingFollowing(userInfo)}
        #print(node)
        out_file = open("nodes_{}.json".format(str_date_time), "a")
        if band == 0:
            out_file.write("[\n")
        json.dump(node, out_file, indent = 4)
        if band + 1 == len(users):
            out_file.write("\n]")
            out_file.close()
        else:
            out_file.write(",\n")
    u.close()

if __name__ == "__main__":
    f=open("H:/My Drive/jkas/Mitacs/LabRisk/TwitterApi/keys.json")
    data = json.load(f)
    bToken = data['BearerToken']
    main()
    f.close()