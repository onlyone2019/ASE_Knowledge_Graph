from config import graph
def get_pattern_bottom():
    result = []
    find_names = graph.run("match (a:模式) where a.grade=2 return a.name")
    for data in find_names:
        s = str(data['a.name'])
        find_child = graph.run("match (a:模式) where a.name='" + s +
                               "' match (a)-[r]->(b) where exists(b.name) return a.name limit 1")
        for detail in find_child:
            result.append(detail['a.name'])
    result = list(set(result))
    return result