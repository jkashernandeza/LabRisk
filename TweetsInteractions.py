#https://developer.twitter.com/en/docs
#https://github.com/twitterdev/Twitter-API-v2-sample-code

#Libraries ###################################################################################
import json
from tqdm import tqdm
from datetime import datetime
##############################################################################################

#Methods #####################################################################################
from RequestApi import *
import Keys
from TweetsMethods import *
##############################################################################################

#Main ########################################################################################
def main():
    tweet = 1550956529859297280
    str_date_time = datetime.now().strftime("%d_%m_%y_%H%M%S%f")[:-6]
    band2 = True
    u=open("H:/My Drive/jkas/Mitacs/LabRisk/TwitterApi/tweets.json")
    tweets = json.load(u)
    if len(tweets) > 400:
        print("Fetching limit exceeded")
        Keys.bToken = ""
        u.close()
        quit()
    node = {}
    #Calculating time #########################################################################
    noRequest = 0
    for i in tqdm(tweets,desc="Calculating time"):
        x = connect_to_endpoint(getTweetInfo(i["id"]),get_paramsTweetInfo())
        n = json.dumps(x["data"]["public_metrics"]["retweet_count"])
        noRequest += (int(int(n)/1000))+1
    timeRequired = noRequest/15
    if timeRequired > 1:
        flag = input("Time request will be {} min\nContinue? (Y/N): ".format(int(timeRequired)*15))
        if flag != "Y" or "y":
            u.close()
            Keys.bToken = ""
            quit()
    #Fetching #################################################################################
    for band, tweetID in enumerate(tqdm(tweets, desc = "Fetching")):
        tweetInfo = connect_to_endpoint(getTweetInfo(tweetID["id"]),get_paramsTweetInfo())
        #print(tweetInfo)
        out_file = open("nodesT_{}.json".format(str_date_time), "a")
        #No info in the node retweet ##########################################################
        if tweetInfo["data"]["public_metrics"]["retweet_count"] == 0 and tweetInfo["data"]["public_metrics"]["like_count"] == 0:
            if band + 1 == len(tweets):
                out_file.write("\n]")
                out_file.close()
            continue
        try:
            retweets = fetchingRetweeters(tweetInfo)
        except Exception:
            retweets = []
        try:
            likers = fetchingLikers(tweetInfo)
        except Exception:
            likers = []
        node = {"tweetID" : tweetID["id"], "retweets" : retweets, "likers" : likers}
        #print(node)
        if band2:
            out_file.write("[\n")
            band2 = False
        else:
            out_file.write(",\n")
        json.dump(node, out_file, indent = 4)
        if band + 1 == len(tweets):
            out_file.write("\n]")
            out_file.close()
    u.close()
    Keys.bToken = ""
##############################################################################################

#Run and  set keys ###########################################################################
if __name__ == "__main__":
    f=open("H:/My Drive/jkas/Mitacs/LabRisk/TwitterApi/keys.json")
    data = json.load(f)
    Keys.bToken = data['BearerToken']
    f.close()
    main()
##############################################################################################