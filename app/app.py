#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import re
import os
import jieba
import config
from flask import Flask, render_template, request, jsonify
from py2neo import Graph, Node, Relationship, NodeMatcher
from addevent import addevent
from get_pattern_bottom import get_pattern_bottom
from config import app, graph

@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/event_search")
def event_search():
    return render_template("event-search.html")


@app.route('/pattern')
def pattern_graph():
    return render_template("pattern.html")


@app.route('/data_graph')
def data_graph():
    options = get_pattern_bottom()
    return render_template("data-graph.html")


@app.route('/statistics')
def statistics():
    options = get_pattern_bottom()
    return render_template("statistics.html")


@app.route('/pattern_bottom')
def pattern_bottom():
    return jsonify(get_pattern_bottom())


@app.route('/all_events_intro')  # 不写请求方式，默认为 get
def get_all_events_intro():  # 返回page页事件的简介信息
    PER_PAGE = 15  # 每页中包含的事件个数。常量名约定为全大写
    page = int(request.args['page'])
    data = graph.run(
        'match (a:事件名称) match (a)-[:`包含`]->(b) return b.sortflag order by b.sortflag desc')
    strdata = [str(i['b.sortflag']) for i in data]
    page_num = math.ceil(len(strdata) / PER_PAGE)
    startnum = (page - 1) * PER_PAGE
    index = 0
    if startnum == 0:
        index = 16
    else:
        index=15
    newstr = strdata[startnum: (startnum + index)]
    events = []
    for name in newstr:
        one_info = {}
        flag = str(name)
        names = ["S" + i['a.name'] for i in graph.run(
            "match (a) where a.sortflag ='" + flag + "' return a.name")]
        names = list(set(names))
        to_search_attributes = ['时间', '出事地点', '航班号', '客机型号', '航空公司']
        for its in names:
            one_info['事件名称'] = its
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
    page = request.args['page']
    PER_PAGE = 15
    if key == '事件名称':
        events.append(value)
    elif key == '原因' or key == '结果':
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
        find_node = graph.run("match (c:模式{name:'" + key + "'}) match(c)-[:包含]->(a) match (a) where a.name='"
                              + value + "' match (a)<-[:属性]-(b) return b.name")
        for data in find_node:
            events.append("S" + data['b.name'])
    events = list(set(events))  # 去重
    num = len(events)
    page_num = math.ceil(num / PER_PAGE)
    startnum = (int(page) - 1) * PER_PAGE
    events_info = []
    events = events[startnum:startnum+PER_PAGE]
    for event in events:
        one_info = {}
        one_info['事件名称'] = event
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
def get_event_info():  # 根据事件名称返回事件所有属性
    event_name = request.args['event_name']
    find_event = graph.run('match (b:' + event_name + ') return b.name')
    for data in find_event:
        node = data['b.name']
    node = str(node)
    event = 'S' + node
    one_info = {}
    one_info['事件名称'] = event
    to_search_attributes = get_pattern_bottom()
    for attr in to_search_attributes:
        eventinfo = graph.run(
            'match (a:%s) match (a)-[:属性{name:"%s"}]->(b) return b.name' % (event, attr))
        for data in eventinfo:
            one_info[attr] = str(data['b.name'])
    return jsonify(one_info)


@app.route('/patt_node')
def get_patt_node():  # 返回模式结点和边（source:link:target）
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
    # print(max_rank)
    for i in range(0, max_rank):
        min_node = graph.run('match (a) where a.grade=' +
                             str(i) + ' return a.name')
        for data_min in min_node:
            max_nodes = []
            max_node = graph.run(
                'match (a:模式{name:"' + data_min['a.name'] + '"})  match (a)-[:`包含`]->(b) where exists(b.grade) return b.name')
            for data_max in max_node:
                max_nodes.append(data_max['b.name'])
            for maxnode in max_nodes:
                links = {}
                links['source'] = data_min['a.name']
                links['target'] = maxnode
                links['linkText'] = '包含'
                link.append(links)
    patt_nodes['links'] = link
    return jsonify(patt_nodes)


@app.route('/all_detail')
def get_all_detail():  # 返回所有事件名称、航空公司、操作阶段等
    key = request.args['key']
    if(key == "事件名称"):
        find_details = graph.run(
            "match (a:事件名称) match (a)-[:包含]->(b) return b.name")
        result = [('S' + item['b.name']) for item in find_details]
    else:
        find_details = graph.run(
            "match (a:模式{name:'%s'}) match (a)-[:包含]->(b) return b.name" % key)
        result = [item['b.name'] for item in find_details]
    result = list(set(result))
    return jsonify(result)


@app.route('/pattern_details')
def get_pattern_details():  # 返回模式图下的具体数据节点
    name = request.args['name']
    limit = request.args['limit']
    details = []
    finddetail = graph.run(
        "match (a:模式{name:'" + name + "'}) match (a)-[:`包含`]->(b) return b.name limit " + limit)
    for detail in finddetail:
        details.append(detail['b.name'])
    return jsonify(details)


@app.route('/reason_participle')
def get_reason_participle():  # 返回原因的分词
    result = {}
    findreason = graph.run(
        "match (a:模式{name:'原因'}) match (a)-[:包含]->(b) return b.name")
    for data in findreason:
        seg_list = jieba.cut(str(data['b.name']), cut_all=False)
        for detail in seg_list:
            if result.get(detail, -1) == -1:
                result[detail] = 1
            else:
                result[detail] += 1
    result = sorted(result.items(), key=lambda x: x[1], reverse=False)
    return jsonify(result)


@app.route('/some_event')
def get_some_event():  # 返回16个事件信息
    aptt_node = {}  # 以节点和边的形式返回 (source:link:target)
    nodes = []
    node = {}
    links = []
    link = {}
    node['id'] = "航空安全事件"
    node['grade'] = 1
    nodes.append(node.copy())
    cnt = 0
    cnt2 = 0
    to_search_attributes = ['时间', '客机型号', '航空公司', '航班号', '起飞地点', '降落地点',
                            '出事地点', '事件类型', '航线类型', '航班类型', '天气情况', '操作阶段', '原因', '人员伤亡', '结果', '等级']
    find_names = graph.run(
        "match(a:事件名称) match (a)-[:包含]->(b) return b.name limit 15")
    for name in find_names:
        # cnt=cnt+1
        tmpname = name['b.name']
        onename = "S" + tmpname
        node['id'] = tmpname
        node['grade'] = 2
        cnt = cnt+1
        link['source'] = 0
        link['target'] = cnt
        link['linkText'] = "包含"
        links.append(link.copy())
        cnt2 = 0
        nodes.append(node.copy())  # 注意要放备份 不能直接放原版 否则后面修改影响前面数据
        for attr in to_search_attributes:
            eventinfo = graph.run(
                'match (a:%s) match (a)-[:属性{name:"%s"}]->(b) return b.name' % (onename, attr))
            for data in eventinfo:
                node['id'] = data['b.name']
                node['grade'] = 3
                cnt2 = cnt2+1
                link['source'] = cnt
                link['target'] = cnt+cnt2
                link['linkText'] = attr
                nodes.append(node.copy())
                links.append(link.copy())
                break
        cnt = cnt+cnt2
    # 追加一条属性比较完整的时间信息
    node['id'] = "S0115US_1549"
    node['grade'] = 2
    nodes.append(node.copy())
    cnt = cnt+1
    link['source'] = 0
    link['target'] = cnt
    link['linkText'] = "包含"
    links.append(link.copy())
    cnt2 = 0
    for attr in to_search_attributes:
        eventinfo = graph.run(
            'match (a:%s) match (a)-[:属性{name:"%s"}]->(b) return b.name' % ("S0115US_1549", attr))
        for data in eventinfo:
            node['id'] = data['b.name']
            node['grade'] = 3
            cnt2 = cnt2+1
            link['source'] = cnt
            link['target'] = cnt+cnt2
            link['linkText'] = attr
            nodes.append(node.copy())
            links.append(link.copy())
    aptt_node['nodes'] = nodes
    aptt_node['links'] = links
    return jsonify(aptt_node)


@app.route('/one_event')  # 用于事件图中查找具体信息
def get_one_event():  # 输入要查询的key和value 返回和那个节点相关的节点和边
    nodes = []
    node = {}
    links = []
    link = {}
    cnt1 = 0
    cnt2 = 0
    key = request.args['key']
    value = request.args['value']
    to_search_attributes = ['时间', '客机型号', '航空公司', '航班号', '起飞地点', '降落地点',
                            '出事地点', '事件类型', '航线类型', '航班类型', '天气情况', '操作阶段', '原因', '人员伤亡', '结果', '等级']
    if key == '事件名称':  # 如果根据事件名称查询事件具体信息
        node['id'] = value
        node['grade'] = 1
        nodes.append(node.copy())
        for attr in to_search_attributes:
            str = 'match (b) where b.name="%s" match (b)-[:属性{name:"%s"}]->(a) return a.name' % (
                value, attr)
            print(str)
            event_info = graph.run(str)
            for data in event_info:
                node['id'] = data['a.name']
                node['grade'] = 2
                cnt2 = cnt2+1
                link['source'] = cnt1
                link['target'] = cnt1+cnt2
                link['linkText'] = attr
                nodes.append(node.copy())
                links.append(link.copy())
                break
    else:  # 如果查的是某个属性关联的东西
        node['id'] = value
        node['grade'] = 2
        nodes.append(node.copy())
        for attr in to_search_attributes:
            str = 'match (b) where b.name="%s" match (a)-[:属性{name:"%s"}]->(b) return a.name' % (
                value, attr)
            # print(str)
            event_info = graph.run(str)
            for data in event_info:
                node['id'] = data['a.name']
                node['grade'] = 1
                cnt2 = cnt2+1
                link['source'] = cnt1+cnt2
                link['target'] = cnt1
                link['linkText'] = attr
                nodes.append(node.copy())
                links.append(link.copy())
                break
        # cnt1 = cnt1 + cnt2+1
        cnt2 = cnt1 + cnt2
        event_info = graph.run(
            'match (b) where b.name="%s" match (a)-[:包含]->(b) return a.name' % (value))
        for data in event_info:
            node['id'] = data['a.name']
            node['grade'] = 1
            cnt2 = cnt2+1
            link['source'] = cnt1+cnt2
            link['target'] = cnt1
            link['linkText'] = "包含"
            nodes.append(node.copy())
            links.append(link.copy())
            break
    aptt_node = {}
    aptt_node['nodes'] = nodes
    aptt_node['links'] = links
    return jsonify(aptt_node)


@app.route('/del_oneevent', methods=["POST"])  # 删除一个事件的信息
def to_del_oneevent():
    name = request.json['事件名称']
    graph.run("match(a:%s)  match (a)-[b]-() delete b delete a" % name)
    result = {}
    result['success'] = True
    return jsonify(result)


@app.route('/add_oneevent', methods=["POST"])  # 添加一个事件
def to_add_oneevent():
    name = request.json['事件名称']
    time = request.json['时间']
    plane = request.json['客机型号']
    airline = request.json['航空公司']
    flightnum = request.json['航班号']
    beginPlace = request.json['起飞地点']
    landPlace = request.json['降落地点']
    incidentPalce = request.json['出事地点']
    evenType = request.json['事件类型']
    airlineType = request.json['航线类型']
    flightType = request.json['航班类型']
    weather = request.json['天气情况']
    stage = request.json['操作阶段']
    reason = request.json['原因']
    result = request.json['结果']
    injured = request.json['人员伤亡']
    grade = request.json['等级']
    addevent(name, time, plane, airline, flightnum, beginPlace, landPlace, incidentPalce,
             evenType, airlineType, flightType, weather, stage, reason, result, injured, grade)
    return_result = {}
    return_result['success'] = True
    return jsonify(return_result)


@app.route('/update_oneevent', methods=["POST"])  # 修改一个事件
def to_update_oneevent():
    name = request.json['事件名称']
    graph.run("match(a:%s)  match (a)-[b]-() delete b delete a" % ("S"+name))
    time = request.json['时间']
    plane = request.json['客机型号']
    airline = request.json['航空公司']
    flightnum = request.json['航班号']
    beginPlace = request.json['起飞地点']
    landPlace = request.json['降落地点']
    incidentPalce = request.json['出事地点']
    evenType = request.json['事件类型']
    airlineType = request.json['航线类型']
    flightType = request.json['航班类型']
    weather = request.json['天气情况']
    stage = request.json['操作阶段']
    reason = request.json['原因']
    result = request.json['结果']
    injured = request.json['人员伤亡']
    grade = request.json['等级']
    addevent(name, time, plane, airline, flightnum, beginPlace, landPlace, incidentPalce,
             evenType, airlineType, flightType, weather, stage, reason, result, injured, grade)
    return_result = {}
    return_result['success'] = True
    return jsonify(return_result)


@app.route('/time_data')
def get_time_data():
    from_t = request.args['from_time']
    to_t = request.args['to_time']
    from_time = int(from_t)
    to_time = int(to_t) + 1
    to_search_grade = ['一般', '重大', '严重', '特大', '事件', '事故']
    result = []
    for i in range(from_time, to_time):
        tmp = {}
        time = str(i)
        tmp['time'] = time
        for grade in to_search_grade:
            sql = "match(a) where a.name=~'.*" + time + ".*' " + \
                "match (b)-[:属性{name:'时间'}]->(a) " + "match (b)-[:属性{name:'等级'}]->(c) where c.name=~'.*" + str(
                    grade) + ".*' return count(c)"
            cnt = graph.run(sql)
            for detail in cnt:
                tmp['grade'] = grade
                tmp['cnt'] = detail['count(c)']
                result.append(tmp.copy())
                break
    return jsonify(result)


@app.route('/update_attr', methods=["POST"])
def to_update_attr():
    name = str(request.json['name'])
    key = str(request.json['key'])
    value = str(request.json['value'])
    sql = "match (a:%s) match (a)-[:属性{name:'%s'}]->(b) match (b)-[r]-() return count(r)" % (
        name, key)
    sql_re = graph.run(sql)
    cnt = 0
    for detail in sql_re:
        cnt = int(detail['count(r)'])
        break
    if cnt > 2:
        sql = "match (a:%s) match (a)-[r:属性{name:'%s'}]->(b)  delete r " % (
            name, key)
    else:
        sql = "match (a:%s) match (a)-[:属性{name:'%s'}]->(b) match (b)-[r]-(c)  delete r delete b " % (
            name, key)
    graph.run(sql)
    if key != "时间":
        find_key = matcher.match(value, name=value).first()
    else:
        find_key = matcher.match("T" + value, name=value).first()
    if find_key == None:
        if key != "时间":
            sql = "match (s:%s) match (a:模式{name:'%s'}) create (b:%s{name:'%s'}) create (a)-[:包含]->(b) create (s)-[:属性{name:'%s'}]->(b)" % (
                name, key, value, value, key)
        else:
            sql = "match (s:%s) match (a:模式{name:'%s'}) create (b:%s{name:'%s'}) create (a)-[:包含]->(b) create (s)-[:属性{name:'%s'}]->(b)" % (
                name, key, "T"+value, value, key)
        graph.run(sql)
    else:
        sql = "match (s:%s) match (b) where b.name='%s' create (s)-[:属性{name:'%s'}]->(b)" % (
            name, value, key)
        graph.run(sql)
    return_result = {}
    return_result['success'] = True
    return jsonify(return_result)


@app.route('/delete_attr', methods=["POST"])
def to_delete_attr():
    name = str(request.json['name'])
    key = str(request.json['key'])
    sql = "match (a:%s) match (a)-[r:属性{name:'%s'}]->(b) delete r" % (
        name, key)
    graph.run(sql)
    return_result = {}
    return_result['success'] = True
    return jsonify(return_result)
