# neo4s
## Use the power of neo4j over Splunk.

This app allows you to run cypher queries and get the results, all over splunk. This allows you to take advantage of both neo4j's cypher and splunk's SPL.

App page on SplunkBase: https://splunkbase.splunk.com/app/3883/
## Examples

Basic usage:
```
| neo4j host="mygraph.com:7687" query="MATCH (n)-[r]->(m) RETURN n,r,m" | table *
```

Using neo4j authentication:
```
| neo4j host="secretgraph.com:7687" username="neo4j" password="neo4j" query="MATCH (n) RETURN n LIMIT 10"
```

Using different scheme:
```
| neo4j host="mygraph.com:7687" scheme="neo4j" query="MATCH (n) RETURN n" | table *
```

## Options
- <b>`host`</b> <i>(required)</i>: Hostname + graph port (port is optional)
- <b>`query`</b> <i>(required)</i>: Cypher query to run on the graph (can be of any kind)
- <b>`username`</b> <i>(optional)</i>: Username for authentication
- <b>`password`</b> <i>(optional)</i>: Password for authentication
- <b>`scheme`</b> <i>(optional)</i>: Default to bolt

## Protocol
The default is bolt, in order to use different scheme in the url, set `scheme="<scheme_name>"` and use the appropriate port at the end of the `host` parameter.

## Credits
- Uses neo4j official python client [neo4j-driver](https://neo4j.com/docs/api/python-driver/current/)
- App icon is taken from [Icons8](https://icons8.com/)