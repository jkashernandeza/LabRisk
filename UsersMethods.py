import json
from RequestApi import *

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