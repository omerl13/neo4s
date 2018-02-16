# neo4s
## Use the power of neo4j over Splunk.

This app allows you to run cypher queries and get the results, all over splunk. This allows you to take advantage of both neo4j's cypher and splunk's SPL.

App page on SplunkBase: https://splunkbase.splunk.com/app/3883/
## Examples

Basic usage:
```
| neo4j host="mygraph.com:7474" query="MATCH (n)-[r]->(m) RETURN n,r,m" | table *
```

Using neo4j authentication:
```
| neo4j host="secretgraph.com:7474" username="neo4j" password="neo4j" query="MATCH (n) RETURN n LIMIT 10"
```

Using bolt protocol:
```
| neo4j host="mygraph.com:7687" scheme="bolt" query="MATCH (n) RETURN n" | table *
```

## Options
- <b>`host`</b> <i>(required)</i>: Hostname + graph port (port is optional, default port is 7474 for HTTP and 7687 for bolt)
- <b>`query`</b> <i>(required)</i>: Cypher query to run on the graph (can be of any kind)
- <b>`username`</b> <i>(optional)</i>: Username for authentication
- <b>`password`</b> <i>(optional)</i>: Password for authentication
- <b>`scheme`</b> <i>(optional)</i>: Default to HTTP

## Protocol
This app can query neo4j graphs in bolt protocol. The default is HTTP, in order to use bolt, set `scheme="bolt"` and use the bolt port at the end of the `host` parameter.

## Credits
- Uses neo4j python client [py2neo](https://github.com/technige/py2neo)
- App icon is taken from [Icons8](https://icons8.com/)