#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from py2neo import Graph, Node, Relationship, NodeMatcher
import json
import math, re

app = Flask(__name__)

# 连接neo4j
graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password=""
)
matcher = NodeMatcher(graph)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/all_events_intro')  # 不写请求方式，默认为 get
def all_events_intro():  # 返回page页事件的简介信息
    per_page = 15  # 每页中包含的事件个数
    page_num = math.ceil(graph.run('match (a:事件名称) match (a)-[:`包含`]->(b) return count(b)').data()[0][
                             'count(b)'] / per_page)  # 计算总页数，ceil 用于向上取整
    page = request.args['page']  # get 请求的 url 类似这样：/events_intro?page=1。问号后面的参数会以字典的形式存放在 request.args 中。

    data = graph.run('match (a:事件名称) match (a)-[:`包含`]->(b) return b.name')
    strdata = []
    for i in data:
        strdata.append('S' + str(i['b.name']))
    strdata = list(set(strdata))  # 去重
    print(strdata)
    events = []
    for name in strdata:
        one_info = {}
        one_info['事件名'] = name
        event = graph.run('match (a:' + name + ') match (a)-[:属性{name:"时间"}]->(b) return b.name')
        for data in event:
            one_info['时间'] = str(data['b.name'])
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

    sort_events = sorted(events, key=lambda keys: keys['时间'], reverse=True)
    get_events = sort_events[per_page * (page - 1):per_page * (page - 1) + per_page]
    get_events.append({'page_num': page_num})
    print(get_events)
    return json.dumps(get_events, ensure_ascii=False)  # 打包成 json 返回


@app.route('/events_intro')
def events_intro():  # 返回指定属性的事件简介信息
    key = request.args['key']
    value = request.args['value']
    events = []
    if key == '事件名称':
        value = 'S' + value  # 事件名称最好能做下拉列表
        find_node = graph.run('match (b:' + value + ') return b.name')
        for data in find_node:
            events.append(data['b.name'])
    elif key == '时间':
        value = 'T' + value
        event = ''
        find_node = graph.run('match (b:' + value + ') return b.name')
        for data in find_node:
            event = 'T' + data['b.name']
        rnode = graph.run(
            'match (a:' + event + ') match(a)<-[:属性]-(b) return b.name')
        for data in rnode:
            events.append(data['b.name'])
    else:
        find_str = "match (a:模式{name:'" + key + "'})  match (b) where b.name=~'.*" + \
                   value + ".*' match(a)-[:包含]->(b) return b.name"
        dnode = graph.run(find_str)
        event_add = []
        for data in dnode:
            event_add.append(data['b.name'])
        for add in event_add:
            rnode = graph.run(
                "match (a) where a.name='" + add + "' match(a)<-[:属性]-(b) return b.name")  # 反向查询事件
            for data in rnode:
                events.append(data['b.name'])  # 事件名称
        events = list(set(events))  # 去重
    events_info = []
    for event in events:
        one_info = {}
        one_info['事件名'] = event
        eee = event
        event = 'S' + str(event)
        matcher_event = NodeMatcher(graph)
        find_event = matcher_event.match(event, name=eee).first()
        if find_event != None:
            eventinfo = graph.run(
                'match (a:' + event + ') match (a)-[:属性{name:"时间"}]->(b) return b.name')
            # return json.dumps(str(event), ensure_ascii=False)
            for data in eventinfo:
                one_info['时间'] = str(data['b.name'])
            eventinfo = graph.run(
                'match (a:' + event + ') match (a)-[:属性{name:"出事地点"}]->(b) return b.name')
            for data in eventinfo:
                one_info['出事地点'] = str(data['b.name'])
            eventinfo = graph.run(
                'match (a:' + event + ') match (a)-[:属性{name:"航班号"}]->(b) return b.name')
            for data in eventinfo:
                one_info['航班号'] = str(data['b.name'])
            eventinfo = graph.run(
                'match (a:' + event + ') match (a)-[:属性{name:"客机型号"}]->(b) return b.name')
            for data in eventinfo:
                one_info['客机型号'] = str(data['b.name'])
            eventinfo = graph.run(
                'match (a:' + event + ') match (a)-[:属性{name:"结果"}]->(b) return b.name')
            for data in eventinfo:
                one_info['结果'] = str(data['b.name'])
            events_info.append(one_info)
    num = len(events_info)
    per_page = 15
    page_num = math.ceil(num / per_page)  # 计算总页数，ceil 用于向上取整
    events_info = sorted(
        events_info, key=lambda keys: (keys['时间']), reverse=False)
    events_info.append({'page_num': page_num})
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


@app.route('/patt_node')
def patt_node():#返回模式结点和边（source:link:target）
    patt_nodes = {}
    nodes = []
    pat_nodes = graph.run('match (a:模式) return a.name,a.grade')
    for data in pat_nodes:
        node = {}
        node['id'] = data['a.name']
        node['grade'] = data['a.grade']
        nodes.append(node)
    patt_nodes['nodes'] = nodes
    link = []
    t_rank = []
    rank = graph.run('match (a:模式) where exists(a.grade) return a.grade')
    for data in rank:
        t_rank.append(data['a.grade'])
    max_rank = max(t_rank)
    print(max_rank)
    for i in range(0, max_rank):
        min_node = graph.run('match (a) where a.grade=' + str(i) + ' return a.name')
        for data_min in min_node:
            max_nodes = []
            max_node = graph.run('match (a:模式{name:"' + data_min['a.name'] + '"})  match (a)-[:`包含`]->(b) where exists(b.grade) return b.name')
            for data_max in max_node:
                max_nodes.append(data_max['b.name'])
            for maxnode in max_nodes:
                links = {}
                links['source'] = data_min['a.name']
                links['target'] = maxnode
                links['linkText'] = '包含'
                link.append(links)
    patt_nodes['links']=link
    print(patt_nodes)
    return json.dumps(link, ensure_ascii=False)

@app.route('/get_eventname')
def get_eventname():  #返回所有事件名
    eventName = []
    findname = graph.run("match (a:事件名称) match (a)-[:包含]->(b) return b.name")
    for data in findname:
        eventName.append(data['b.name'])
    return json.dumps(eventName, ensure_ascii=False)

@app.route('/get_patternDetails')
def get_patternDetails():  #返回模式图下的具体数据节点
    key = request.args['key']
    value = request.args['value']
    details=[]
    finddetail = graph.run("match (a:模式{name:'" + key + "'}) match (a)-[:`包含`]->(b) return b.name limit " + value)
    for detail in finddetail:
        details.append(detail['b.name'])
    return json.dumps(details, ensure_ascii=False)

@app.route('/get_reasonParticiple')
def get_reasonParticiple():  #返回原因的分词
    result = {}
    findreason = graph.run("match (a:模式{name:'原因'}) match (a)-[:包含]->(b) return b.name")
    for data in findreason:
        seg_list = jieba.cut(str(data['b.name']), cut_all=False)
        for detail in seg_list:
            if result.get(detail, -1) == -1:
                result[detail] = 1
            else:
                result[detail] += 1
    result = sorted(result.items(), key=lambda x: x[1], reverse=False)
    return json.dumps(result, ensure_ascii=False)
