#https://developer.twitter.com/en/docs
#https://github.com/twitterdev/Twitter-API-v2-sample-code

import requests
import time
import json
from tqdm import tqdm
from datetime import datetime

from RequestApi import *
import Keys
from UsersMethods import *

def main():
    str_date_time = datetime.now().strftime("%d_%m_%y_%H%M%S%f")[:-6]
    u=open("H:/My Drive/jkas/Mitacs/LabRisk/TwitterApi/users.json")
    users = json.load(u)
    node = {}
    noRequest = 0
    for i in tqdm(users,desc="Calculating time"):
        x = connect_to_endpoint(getUserInfo(i["id"]),get_paramsUserInfo())
        n = json.dumps(x["data"]["public_metrics"]["following_count"])
        noRequest += (int(int(n)/1000))+1
        n = json.dumps(x["data"]["public_metrics"]["followers_count"])
        noRequest += (int(int(n)/1000))+1
    timeRequired = noRequest/15
    if timeRequired > 1:
        flag = input("Time request will be {} min\nContinue? (Y/N): ".format(int(timeRequired)*15))
        if flag != "Y" or "y":
            u.close()
            f.close()
            quit()
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
    Keys.bToken = data['BearerToken']
    f.close()
    main()