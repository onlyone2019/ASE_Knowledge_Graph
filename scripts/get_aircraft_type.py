from py2neo import Graph
import re


graph = Graph(
    "http://47.94.94.136:7474",
    username="neo4j",
    password="1358044937"
)


cypher = 'match (a:`客机型号`) match(a)-[:`包含`]-(b) return b'
data = graph.run(cypher).data()

with open("客机型号.txt", 'w') as f:
    for i in data:
        matcher = re.search(r'\(_\d+:\w+ \{', str(i['b']))
        f.write(matcher.group().split(':')[1][:-2] + '\n')
