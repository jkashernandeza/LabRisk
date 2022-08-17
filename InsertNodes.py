#Libraries ###################################################################################
import json
from sys import flags
from turtle import rt
from neo4jConn import *
from tkinter import *
from tkinter import filedialog
from tqdm import tqdm
##############################################################################################

#Open file and set type ######################################################################
def openJSON():
    filepath = filedialog.askopenfilename(
        initialdir="/Desktop",title="Open JSON",
        filetypes=(("json files","*.json"),("all files","*.*")))
    global nType, flag, jsonNodes, keysDict, r1Type, r2Type
    if ("nodesU" in filepath):
        nType = "user"
        r1Type = "follows"
        flag = True
    else:
        nType = "tweet"
        r1Type = "retweeted_by"
        r2Type = "likes"
        flag = False
    file = open(filepath,'r')
    jsonNodes = json.load(file)
    file.close()
    keysDict = []
    for i in jsonNodes[0].keys():
        keysDict.append(i)
##############################################################################################

#Read and Insert Nodes in DB #################################################################
def ReadInsertNodes(conn):
    for node in tqdm(jsonNodes,desc="Updating Data Base"):
        conn.createNode(nType,node[keysDict[0]])
        for x in  tqdm(node[keysDict[1]], desc = "Reading nodes"):
            conn.createNode("user",x)
            if flag:
                conn.createRelationship(nType, nType, r1Type, x, node[keysDict[0]])
            else:
                conn.createRelationship(nType, "user", r1Type, node[keysDict[0]], x)
        for x in tqdm(node[keysDict[2]], desc = "Reading nodes"):
            conn.createNode("user",x)
            if flag:
                conn.createRelationship(nType, nType, r1Type, node[keysDict[0]], x)
            else:
                conn.createRelationship("user", nType, r2Type, x, node[keysDict[0]])
##############################################################################################

#Run and  set keys ###########################################################################
if __name__ == "__main__":
    openJSON()
    f=open("H:/My Drive/jkas/Mitacs/LabRisk/TwitterApi/keys.json")
    data = json.load(f)
    password = data['DBTwitterPass']
    uri = data['neo4jTwittweURI']
    f.close()
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    conn = nodeConn(uri, "neo4j", password)
    ReadInsertNodes(conn)
    conn.close()
##############################################################################################