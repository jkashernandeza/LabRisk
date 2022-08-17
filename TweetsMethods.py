#Libraries ###################################################################################
import json
from RequestApi import *
##############################################################################################

#Tweet info ####################################################################################
def getTweetInfo(tweet_id):
    # Replace with tweet ID below
    return "https://api.twitter.com/2/tweets/{}".format(tweet_id)
def get_paramsTweetInfo():
    return {"tweet.fields": "author_id,public_metrics"}
##############################################################################################

#Retweets list ###############################################################################
def getRetweets(tweet_id):
    # Replace with tweet ID below
    return "https://api.twitter.com/2/tweets/{}/retweeted_by?max_results=100".format(tweet_id)
def get_paramsRetweets():
    return {"user.fields": "public_metrics"}
##############################################################################################

#Liking list #################################################################################
def getLiking(tweet_id):
    # Replace with tweet ID below
    return "https://api.twitter.com/2/tweets/{}/liking_users?max_results=100".format(tweet_id)
def get_paramsLiking():
    return {"user.fields": "public_metrics"}
##############################################################################################

#Getting Retweeters list #####################################################################
def fetchingRetweeters(tweetInfo):
    n = json.dumps(tweetInfo["data"]["public_metrics"]["retweet_count"])
    loop = (int(int(n)/100))+1
    try:
        del retweetersList
    except Exception:
        pass
    retweetersList = []
    urlRetweeters = getRetweets(tweetInfo["data"]["id"])
    paramsRetweeters = get_paramsRetweets()
    for i in range(loop):
        if i == 0:
            #print(urlRetweeters, paramsRetweeters)
            retweeters = connect_to_endpoint(urlRetweeters, paramsRetweeters)
            #print(json.dumps(retweeters["data"]))
            for x in retweeters["data"]:
                retweetersList.append(x['id'])
                
            try:
                nextToken = (json.dumps(retweeters["meta"]["next_token"])).replace('"','')
                #print(nextToken)
            except Exception:
                pass
        else:
            new = urlRetweeters+"&pagination_token="+nextToken
            aux = connect_to_endpoint(new, paramsRetweeters)
            #print(json.dumps(aux))
            for x in aux["data"]:
                retweetersList.append(x['id'])
    #print(len(retweetersList))
    #print(retweetersList)
    return retweetersList
##############################################################################################

#Getting Liking list #########################################################################
def fetchingLikers(tweetInfo):
    n = json.dumps(tweetInfo["data"]["public_metrics"]["like_count"])
    loop = (int(int(n)/100))+1
    try:
        del likingList
    except Exception:
        pass
    likingList = []
    urlLiking = getLiking(tweetInfo["data"]["id"])
    paramsLiking = get_paramsLiking()
    for i in range(loop):
        if i == 0:
            #print(urlLiking, paramsLiking)
            likers = connect_to_endpoint(urlLiking, paramsLiking)
            #print(json.dumps(likers["data"]))
            for x in likers["data"]:
                likingList.append(x['id'])
                
            try:
                nextToken = (json.dumps(likers["meta"]["next_token"])).replace('"','')
                #print(nextToken)
            except Exception:
                pass
        else:
            new = urlLiking+"&pagination_token="+nextToken
            aux = connect_to_endpoint(new, paramsLiking)
            #print(json.dumps(aux))
            for x in aux["data"]:
                likingList.append(x['id'])
    #print(len(likingList))
    #print(likingList)
    return likingList
##############################################################################################