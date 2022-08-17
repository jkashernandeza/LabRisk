#Libraries ###################################################################################
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
##############################################################################################


#Class Node###################################################################################
class nodeConn:
    ##########################################################################################
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    ##########################################################################################
    def close(self):
        self.driver.close()
    ##########################################################################################
    def createNode(self, nType, nID):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_return_node, nType, nID)
    ##########################################################################################
    @staticmethod
    def _create_and_return_node(tx, nType, nID):
        result = tx.run("MERGE (n : {} {{myID : '{}' }}) "
                        "RETURN n".format(nType,nID))
        return result.single()[0]
    ##########################################################################################
    def createRelationship(self, n1Type, n2Type, rType, nID1, nID2):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_return_relationship, n1Type, n2Type, rType, nID1, nID2)
    ##########################################################################################     
    @staticmethod
    def _create_and_return_relationship(tx, n1Type, n2Type, rType, nID1, nID2):
        result = tx.run("""MATCH (n1 : {0} {{myID: '{3}'}})
                            MATCH (n2 : {1} {{myID: '{4}'}})
                            MERGE (n1)-[r : {2}]->(n2)
                            RETURN n1,n2""".format(n1Type,n2Type,rType,nID1,nID2))
        return result.single()[0]
##############################################################################################