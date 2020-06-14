import json
import sys
import time
from splunklib.searchcommands import dispatch, GeneratingCommand, Configuration, Option, validators
from neo4j import GraphDatabase, basic_auth
from neo4j.graph import Node, Relationship


@Configuration()
class Neo4jCommand(GeneratingCommand):
    query = Option(require=True)
    host = Option(require=True)
    username = Option(require=False, default="")
    password = Option(require=False, default="")
    scheme = Option(require=False, default="bolt")

    def __get_data(self, query, host, username, password, scheme):
        url = scheme + "://" + host
        # set up authentication parameters
        auth = None
        if username != "" and password != "":
            auth = basic_auth(username, password)
        driver = GraphDatabase.driver(
            url,
            auth=auth)
        session = driver.session()
        results = session.run(query, parameters={})
        for record in results:
            yield(record)

    def with_field_extraction(self, results):
        # return results
        for r in results:
            data = {}
            result_dict = dict(r)
            for k,v in result_dict.items():
                if isinstance(v, Node) or isinstance(v, Relationship):
                    print(type(v))
                    for inner_k, inner_v in dict(v).items():
                        data[k + "." + inner_k] = inner_v
                else:
                    data[k] = v
            data["_raw"] = r
            yield data

    def generate(self):
        results = self.__get_data(self.query, self.host,
                                  self.username, self.password, self.scheme)
        return self.with_field_extraction(results)


dispatch(Neo4jCommand, module_name=__name__)
