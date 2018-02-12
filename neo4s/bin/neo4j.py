import json
from py2neo import authenticate, Graph, NodeSelector
import sys
import time
from splunklib.searchcommands import dispatch, GeneratingCommand, Configuration, Option, validators


@Configuration()
class Neo4jCommand(GeneratingCommand):
    query = Option(require=True)
    host = Option(require=True)
    username = Option(require=False, default="")
    password = Option(require=False, default="")
    scheme = Option(require=False, default="http")
    extract_fields = Option(require=False, default=True)

    def __get_data(self, query, host, username, password, scheme):
        url = scheme + "://" + host
        # set up authentication parameters
        if username != "" and password != "":
            authenticate(host, username, password)

        # connect to authenticated graph database
        graph = Graph(url + "/db/data/")
        a = graph.run(query)
        return a.data()

    def with_field_extraction(self, results):
        for r in results:
            data = dict(r)
            data["_raw"] = r
            yield data

    def generate(self):
        results = self.__get_data(self.query, self.host,
                                  self.username, self.password, self.scheme)
        if self.extract_fields:
            return self.with_field_extraction(results)
        else:
            return ({'_raw': result} for result in results)


dispatch(Neo4jCommand, sys.argv, sys.stdin, sys.stdout, __name__)
