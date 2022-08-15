#Libraries ###################################################################################
import imp
import json
from neo4jConn import *
import Keys
from tkinter import *
from tkinter import filedialog
##############################################################################################

def openJSON():
    filepath = filedialog.askopenfilename(
        initialdir="/Desktop",title="Open JSON",
        filetypes=(("json files","*.json"),("all files","*.*")))
    global nType
    if ("nodesU" in filepath):
        nType = "user"
    else:
        nType = "tweet"
    global jsonNodes
    file = open(filepath,'r')
    jsonNodes = json.load(file)
    file.close()
    global keysDict
    keysDict = []
    for i in jsonNodes[0].keys():
        keysDict.append(i)

def ReadInsertNodes(conn):
    for node in jsonNodes:
        conn.createNode(nType,node[keysDict[0]])
        for x in node[keysDict[1]]:
            conn.createNode("user",x)
            conn.createRelationship(nType,keysDict[1],node[keysDict[0]],x)
        for x in node[keysDict[2]]:
            conn.createNode("user",x)
            conn.createRelationship(nType,keysDict[2],node[keysDict[0]],x)

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