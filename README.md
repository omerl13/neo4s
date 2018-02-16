# neo4s
## Use the power of neo4j over Splunk.

This app allows you to run cypher queries and get the results, all over splunk. This allows you to take advantage of both neo4j's cypher and splunk's SPL.

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
- `host` <small><b>(required)</b></small>: Hostname + graph port (7474)
- `query` <small><b>(required)</b></small>: Cypher query to run on the graph (can be of any kind)
- `username` <small><b>(optional)</b></small>: Username for authentication
- `password` <small><b>(optional)</b></small>: Password for authentication
- `scheme`<small><b>(optional)</b></small>: Default to HTTP

## Protocol
This app can query neo4j graphs in bolt protocol. The default is HTTP, in order to use bolt, set `scheme="bolt"` and use the bolt port at the end of the `host` parameter.

## Credits
- Uses neo4j python client [py2neo](https://github.com/technige/py2neo)
- App icon is taken from [Icons8](https://icons8.com/)