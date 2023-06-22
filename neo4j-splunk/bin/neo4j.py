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
from empty_results_exception import EmptyResultsExceptions


@Configuration()
class Neo4jCommand(GeneratingCommand):
    query = Option(require=True)
    host = Option(require=True)
    username = Option(require=False, default="")
    password = Option(require=False, default="")
    scheme = Option(require=False, default="bolt")
    database = Option(require=False, default="neo4j")
    query_params = Option(require=False, default="")

    def __get_data(
        self, query, host, username, password, scheme, database, query_params
    ):
        url = scheme + "://" + host
        # set up authentication parameters
        auth = None
        if username != "" and password != "":
            auth = basic_auth(username, password)
        driver = GraphDatabase.driver(url, auth=auth)
        parameters = {}
        if query_params:
            try:
                parameters = json.loads(query_params)
            except ValueError as e:
                raise ValueError(f"Error in query params dict: {e}")

        with driver.session(database=database) as session:
            results = list(session.run(query, parameters=parameters))
            if not results:
                raise EmptyResultsExceptions("No results found")

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
            self.query_params,
        )

        fields_extractor = FieldsExtractor()
        return fields_extractor.extract(results)


dispatch(Neo4jCommand, module_name=__name__)
