# LabRisk
This project is part of a research about toxicity in social media hosting in Concordia University by dr. Ketra Schmitt.\
The first scope of the research is limit to Twitter, and this code is limited to that.\
The repository has two parts:
## Scraper using Twitter API
The first step is the request for a developer account in order to get a BToken key.\
In the code I am consuming the keys from a local json file, each one has to replace their owns keys.\
The 'RequestApi.py' file set the connection with the API. Note that has a timer of 15 min, that is because is the default time we need to wait when we get a 'Limit Request' error.\
Then we have two branches of the scraper:
### Tweets interactions
There are two python files. 'TweetsMethods.py' has the functions, meanwhile in 'TweetsInteractions'py' is a runnable file. Once we start the code we need to select a local json file with the IDs info. The code has a file picker by itself.\
Example of the input json:\
[\
{"TweetID":"xxxxxxxxxxxxxxxxxx","UserID":"xxxxxxxxxxxxxxxxxx"},\
{"TweetID":"xxxxxxxxxxxxxxxxxx","UserID":"xxxxxxxxxxxxxxxxxx"},\
...\
{"TweetID":"xxxxxxxxxxxxxxxxxx","UserID":"xxxxxxxxxxxxxxxxxx"}\
]
The code will give an approximation of the time it will takes running. We accept by inserting a 'Y' (case sensitive). When it finish we will have a json file named 'nodesT_dd_mm_yy_hhmmss.json'. Save the location because we need it later.
The output file contains the user who likes and retweet the tweet, like this:\
[\
{\
    "tweetID": xxxxxxxxxxxxxxxxxx,\
    "retweets": [\
        "xxxxxxxxxxxxxxxxxx\
    ],\
    "likers": [\
        "xxxxxxxxxxxxxxxxxx"\
    ]\
}\
]
### Users Relationships
It has the same structure of the last scraper and we also need to feed it with the same input json
The code will also give us an approximation, not necessarily the same time.
When it finish we will have a json file named 'nodesU_dd_mm_yy_hhmmss.json'. Save the location because we need it later.\
The output file contains the user followers and followings, like this:\
[\
{\
    "userID": xxxxxxxxxxxxxxxxxx,\
    "followers": [\
        "xxxxxxxxxxxxxxxxxx\
    ],\
    "following": [\
        "xxxxxxxxxxxxxxxxxx"\
    ]\
}\
]

Please note that you can run in parallel the codes. How to running is your choose.
## Storage in Neo4j
There are previous steps before you can run the code:
- Have a Neo4j data base.
- Have the 'nodesX_dd_mm_yy_hhmmss.json' files
- Install neo4jConn in your python environment
We also have two python files. The 'neo4jConn.py' is a class that contains the methods for connection, close, create nodes and relationships.\
The code connects it self by the URI method, I set the URI and password in a local json file, each one has to replace their owns info.\
The file 'InsertNode.py' will ask for a input file, we need to feed it with the outputs that we got before.
The code will insert the nodes and relationships without duplicates. At the end of the run we will have the nodes and relationships in our data base, ready for the data analysis.\
Note that for a right execution the DB service needs to be running.\
The code in this repository only insert nodes with the IDs, in a future scope will be able to insert the labels of toxicity. Also the relationship of who posted the tweet is not consider in this version.