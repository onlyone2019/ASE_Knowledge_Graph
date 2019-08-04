from flask import Flask, render_template, request
from py2neo import Graph, Node, Relationship, NodeMatcher
import json
import math

app = Flask(__name__)

# 连接neo4j
graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="m1358044937"
)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route('/all_events_intro') # 不写请求方式，默认为 get
def all_events_intro():  # 返回page页事件的简介信息
    per_page = 15   # 每页中包含的事件个数
    page_num = math.ceil(graph.run('match (a:航空安全事件) match (a)-[:`包含`]->(b) return count(b)').data()[0]['count(b)'] / per_page) # 计算总页数，ceil 用于向上取整
    page = request.args['page']     # get 请求的 url 类似这样：/events_intro?page=1。问号后面的参数会以字典的形式存放在 request.args 中。
    data = graph.run("match (a:航空安全事件) match (a)-[:`包含`]->(b) return b.name skip %s limit %s" % (page, per_page))
    strdata = []
    for i in data:
        strdata.append('S' + str(i['b.name']))
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
    sort_events = sorted(events, key=lambda keys: keys['日期'], reverse=True)
    sort_events.append({'page_num':page_num})
    return json.dumps(sort_events, ensure_ascii=False)  # 打包成 json 返回


@app.route('/events_intro')
def events_intro():  # 返回指定属性的事件简介信息
    key = request.args['key']
    value = request.args['value']
    find_node = graph.run('match (b:' + value + ') return b.name')
    for data in find_node:
        node = data['b.name']
    node = str(node)
    if key == '时间':
        node = 'T' + node
    find_event = graph.run('match (a:' + node + ') match (a)<-[:属性]-(b) return b.name')
    events = []
    for data in find_event:
        events.append('S' + str(data['b.name']))
    events_info = []
    for event in events:
        one_info = {}
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
    return json.dumps(events_info, ensure_ascii=False)


@app.route('/event_info')
def event_info():  # 根据事件名返回事件所有属性
    event_name = request.args['event_name']
    find_event = graph.run('match (b:' + event_name + ') return b.name')
    for data in find_event:
        node = data['b.name']
    node = str(node)
    event = 'S' + node
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
    return json.dumps(one_info, ensure_ascii=False)
