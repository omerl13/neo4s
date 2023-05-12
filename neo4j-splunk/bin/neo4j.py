import json
import sys
import time
from splunklib.searchcommands import (
    dispatch,
    GeneratingCommand,
    Configuration,
    Option,
    validators,
)
from neo4j import GraphDatabase, basic_auth
from neo4j.graph import Node, Relationship
from fields_extractor import FieldsExtractor


@Configuration()
class Neo4jCommand(GeneratingCommand):
    query = Option(require=True)
    host = Option(require=True)
    username = Option(require=False, default="")
    password = Option(require=False, default="")
    scheme = Option(require=False, default="bolt")
    database = Option(require=False, default="neo4j")

    def __get_data(self, query, host, username, password, scheme, database):
        url = scheme + "://" + host
        # set up authentication parameters
        auth = None
        if username != "" and password != "":
            auth = basic_auth(username, password)
        driver = GraphDatabase.driver(url, auth=auth)
        with driver.session(database=database) as session:
            results = session.run(query, parameters={})
            for record in results:
                yield (record)

    def generate(self):
        results = self.__get_data(
            self.query,
            self.host,
            self.username,
            self.password,
            self.scheme,
            self.database,
        )

        fields_extractor = FieldsExtractor()
        return fields_extractor.extract(results)


dispatch(Neo4jCommand, module_name=__name__)
