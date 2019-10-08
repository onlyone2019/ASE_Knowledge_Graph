#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from py2neo import Graph, Node, Relationship, NodeMatcher
from flask_scss import Scss
import math
import re
import os
import jieba

######### config.py #########

# basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    JSON_AS_ASCII = False
    PY2NEO_CONFIG = {       # py2neo 连接配置
        "host": "47.94.94.136",
        "username": "neo4j",
        "password": "1358044937"
    }

    @staticmethod
    def init_app(app):
        pass

######### config.py #########

app = Flask(__name__)
config = Config()
app.config.from_object(config)
Scss(app, static_dir='app/static/css', asset_dir='app/static/scss')

# 连接neo4j
graph = Graph(
    host=app.config["PY2NEO_CONFIG"]["host"],
    username=app.config["PY2NEO_CONFIG"]["username"],
    password=app.config["PY2NEO_CONFIG"]["password"]
)
matcher = NodeMatcher(graph)


def get_pattern_bottom():
    result = []
    find_names = graph.run("match (a:模式) where a.grade=2 return a.name")
    for data in find_names:
        s = str(data['a.name'])
        find_child = graph.run("match (a:模式) where a.name='" + s + "' match (a)-[r]->(b) where exists(b.name) return a.name limit 1")
        for detail in find_child:
            result.append(detail['a.name'])
    result = list(set(result))
    return result


@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html", title='首页', active=1)

@app.route("/event_search")
def event_search():
    options = get_pattern_bottom()
    return render_template("event-search.html", title="事件检索", options=options, active=2)

@app.route('/pattern')
def pattern_graph():
    return render_template("pattern.html", title='模式图', active=3)

@app.route('/all_events_intro')  # 不写请求方式，默认为 get
def get_all_events_intro():  # 返回page页事件的简介信息
    PER_PAGE = 15  # 每页中包含的事件个数。常量名约定为全大写
    page = int(request.args['page'])
    data = graph.run('match (a:事件名称) match (a)-[:`包含`]->(b) return b.sortflag order by b.sortflag desc')
    strdata = [str(i['b.sortflag']) for i in data]
    page_num = math.ceil(len(strdata)/PER_PAGE)
    startnum = (page - 1) * PER_PAGE
    newstr = strdata[startnum: (startnum + 15)]
    events = []
    for name in newstr:
        one_info = {}
        flag = str(name)
        names = ["S" + i['a.name'] for i in graph.run(
            "match (a) where a.sortflag ='" + flag + "' return a.name")]
        names = list(set(names))
        to_search_attributes = ['时间', '出事地点', '航班号', '客机型号', '航空公司']
        for its in names:
            one_info['事件名'] = its
            for attr in to_search_attributes:
                event = graph.run(
                    'match (a:%s) match (a)-[:属性{name:"%s"}]->(b) return b.name' % (its, attr))
                for data in event:
                    one_info[attr] = str(data['b.name'])
            events.append(one_info)
    events.append({'page_num': page_num})
    return jsonify(events)   # 使用 flask 自带的 json 打包函数


@app.route('/events_intro')
def get_events_intro():  # 返回指定属性的事件简介信息
    key = request.args['key']
    value = request.args['value']
    events = []
    page=request.args['page']
    PER_PAGE = 15
    if key == '事件名称':
        events.append('S' + value)
    elif (key == '原因') | (key == '结果'):
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
                events.append("S" + data['b.name'])  # 事件名称
    else:
        find_node = graph.run("match (c:模式{name:'" + key + "'}) match(c)-[:包含]->(a) match (a) where a.name='" \
             + value + "' match (a)<-[:属性]-(b) return b.name")
        for data in find_node:
            events.append("S" + data['b.name'])
    events = list(set(events))  # 去重
    num=len(events)
    page_num = math.ceil(num / PER_PAGE)
    startnum = (int(page) - 1) * PER_PAGE
    events_info = []
    events=events[startnum:startnum+PER_PAGE]
    for event in events:
        one_info = {}
        one_info['事件名'] = event
        matcher_event = NodeMatcher(graph)
        find_event = matcher_event.match(event).first()
        if find_event != None:
            to_search_attributes = ['时间', '出事地点', '航班号', '客机型号', '航空公司']
            for attr in to_search_attributes:
                eventinfo = graph.run(
                    'match (a:%s) match (a)-[:属性{name:"%s"}]->(b) return b.name' % (event, attr))
                for data in eventinfo:
                    one_info[attr] = str(data['b.name'])
            events_info.append(one_info)
    events_info = sorted(
        events_info, key=lambda keys: (keys['时间']), reverse=False)
    events_info.append({'page_num': page_num})
    return jsonify(events_info)

@app.route('/event_info')
def get_event_info():  # 根据事件名返回事件所有属性
    event_name = request.args['event_name']
    find_event = graph.run('match (b:' + event_name + ') return b.name')
    for data in find_event:
        node = data['b.name']
    node = str(node)
    event = 'S' + node
    one_info = {}
    one_info['事件名'] = event
    to_search_attributes = get_pattern_bottom()
    for attr in to_search_attributes:
        eventinfo = graph.run('match (a:%s) match (a)-[:属性{name:"%s"}]->(b) return b.name' % (event, attr))
        for data in eventinfo:
            one_info[attr] = str(data['b.name'])
    return jsonify(one_info)


@app.route('/patt_node')
def get_patt_node():#返回模式结点和边（source:link:target）
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
    return jsonify(patt_nodes)

@app.route('/all_detail')
def get_all_detail():  #返回所有事件名、航空公司、操作阶段等
    key = request.args['key']
    result = []
    if(key == "事件名称"):
        find_details = graph.run("match (a:事件名称) match (a)-[:包含]->(b) return b.name")
    else:
        find_details = graph.run("match (a:模式{name:'%s'}) match (a)-[:包含]->(b) return b.name" % key)
    for data in find_details:
        result.append(data['b.name'])
    result = list(set(result))
    return jsonify(result)

@app.route('/pattern_details')
def get_pattern_details():  #返回模式图下的具体数据节点
    name = request.args['name']
    limit = request.args['limit']
    details=[]
    finddetail = graph.run("match (a:模式{name:'" + name + "'}) match (a)-[:`包含`]->(b) return b.name limit " + limit)
    for detail in finddetail:
        details.append(detail['b.name'])
    return jsonify(details)

@app.route('/reason_participle')
def get_reason_participle():  #返回原因的分词
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
    return jsonify(result)
