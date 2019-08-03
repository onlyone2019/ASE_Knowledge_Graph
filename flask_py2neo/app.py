from flask import Flask
from py2neo import Graph, Node, Relationship, NodeMatcher

app = Flask(__name__)

# 连接neo4j
graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="******"
)


@app.route('/events_intro/<page>', methods=['GET', 'POST'])
def events_intro(page):  # 返回page页事件的简介信息
    page = str(page)
    data = graph.run('match (a:航空安全事件) match (a)-[:`包含`]->(b) return b.name skip ' + page + ' limit 30')
    strdata = []
    for i in data:
        strdata.append('S' + str(i['b.name']))
    print(strdata)
    events = []
    for name in strdata:
        one_info = {}
        one_info['事件名'] = name
        event = graph.run('match (a:' + name + ') match (a)-[:属性{name:"时间"}]->(b) return b.name')
        for data in event:
            one_info['日期'] = str(data['b.name'])
        event = graph.run('match (a:' + name + ') match (a)-[:属性{name:"出事地点"}]->(b) return b.name')
        for data in event:
            one_info['出事地点'] = str(data['b.name'])
        event = graph.run('match (a:' + name + ') match (a)-[:属性{name:"航班号"}]->(b) return b.name')
        for data in event:
            one_info['航班号'] = str(data['b.name'])
        event = graph.run('match (a:' + name + ') match (a)-[:属性{name:"客机型号"}]->(b) return b.name')
        for data in event:
            one_info['客机型号'] = str(data['b.name'])
        event = graph.run('match (a:' + name + ') match (a)-[:属性{name:"航空公司"}]->(b) return b.name')
        for data in event:
            one_info['航空公司'] = str(data['b.name'])
        events.append(one_info)
    sort_events = sorted(events, key=lambda keys: keys['日期'])
    return sort_events


@app.route('/event_info', methods=['GET', 'POST'])
def event_info(key, value):  # 返回指定属性的事件简介信息
    find_node = graph.run('match (b:' + value + ') return b.name')
    for data in find_node:
        node = data['b.name']
    node = str(node)
    if key == '时间':
        node = 'T' + node
    print(node)
    find_event = graph.run('match (a:' + node + ') match (a)<-[:属性]-(b) return b.name')
    events = []
    for data in find_event:
        events.append('S' + str(data['b.name']))
    print(events)
    events_info = []
    for event in events:
        one_info = {}
        print(event)
        event = str(event)
        one_info['事件名'] = event
        eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"时间"}]->(b) return b.name')
        for data in eventinfo:
            one_info['日期'] = str(data['b.name'])
        eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"出事地点"}]->(b) return b.name')
        for data in eventinfo:
            one_info['出事地点'] = str(data['b.name'])
        eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"航班号"}]->(b) return b.name')
        for data in eventinfo:
            one_info['航班号'] = str(data['b.name'])
        eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"客机型号"}]->(b) return b.name')
        for data in eventinfo:
            one_info['客机型号'] = str(data['b.name'])
        eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"航空公司"}]->(b) return b.name')
        for data in eventinfo:
            one_info['航空公司'] = str(data['b.name'])
        events_info.append(one_info)
    return events_info


# event_info('航空公司', '天空服务航空公司')


@app.route('/events_intro/<event_name>', methods=['GET', 'POST'])
def events_intro(event_name):  # 根据事件名返回事件所有属性
    find_event = graph.run('match (b:' + event_name + ') return b.name')
    for data in find_event:
        node = data['b.name']
    node = str(node)
    event = 'S' + node
    print(event)
    one_info = {}
    one_info['事件名'] = event
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"时间"}]->(b) return b.name')
    for data in eventinfo:
        one_info['日期'] = str(data['b.name'])
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"出事地点"}]->(b) return b.name')
    for data in eventinfo:
        one_info['出事地点'] = str(data['b.name'])
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"航班号"}]->(b) return b.name')
    for data in eventinfo:
        one_info['航班号'] = str(data['b.name'])
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"客机型号"}]->(b) return b.name')
    for data in eventinfo:
        one_info['客机型号'] = str(data['b.name'])
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"航空公司"}]->(b) return b.name')
    for data in eventinfo:
        one_info['航空公司'] = str(data['b.name'])
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"起飞地点"}]->(b) return b.name')
    for data in eventinfo:
        one_info['起飞地点'] = str(data['b.name'])
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"降落地点"}]->(b) return b.name')
    for data in eventinfo:
        one_info['降落地点'] = str(data['b.name'])
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"事件类型"}]->(b) return b.name')
    for data in eventinfo:
        one_info['事件类型'] = str(data['b.name'])
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"航线类型"}]->(b) return b.name')
    for data in eventinfo:
        one_info['航线类型'] = str(data['b.name'])
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"航班类型"}]->(b) return b.name')
    for data in eventinfo:
        one_info['航班类型'] = str(data['b.name'])
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"天气情况"}]->(b) return b.name')
    for data in eventinfo:
        one_info['天气情况'] = str(data['b.name'])
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"操作阶段"}]->(b) return b.name')
    for data in eventinfo:
        one_info['操作阶段'] = str(data['b.name'])
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"原因"}]->(b) return b.name')
    for data in eventinfo:
        one_info['原因'] = str(data['b.name'])
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"结果"}]->(b) return b.name')
    for data in eventinfo:
        one_info['结果'] = str(data['b.name'])
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"人员伤亡"}]->(b) return b.name')
    for data in eventinfo:
        one_info['人员伤亡'] = str(data['b.name'])
    eventinfo = graph.run('match (a:' + event + ') match (a)-[:属性{name:"等级"}]->(b) return b.name')
    for data in eventinfo:
        one_info['等级'] = str(data['b.name'])
    return one_info

# events_intro('S0529JA848C')
