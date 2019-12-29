# 事件名称 时间 客机型号 航空公司 航班号 起飞地点 降落地点 出事地点
# 事件类型 航线类型 航班类型 天气情况 操作阶段 原因 结果 人员伤亡 等级
def addevent(name, time, plane, airline, flightnum, beginPlace, landPlace, incidentPalce,
             evenType, airlineType, flightType, weather, stage, reason, result, injured, grade):
    # 添加事件名节点
    s = "match (a:事件名称) create (b:"+name + \
        "{name:'"+name[1:]+"'}) create (a)-[:包含]->(b)"
    graph.run(s)
    index = "match (b:" + name + ")"
    # 时间节点建立
    if time != "":
        check_time = "T" + time
        find_result = matcher.match(check_time, name=time).first()
        if find_result == None:
            construct_time = index + " match (c:模式{name:'时间'}) create (d:T" + time + \
                "{name:'"+time + \
                "'}) create (c)-[:包含]->(d) create (b)-[:属性{name:'时间'}]->(d)"
            graph.run(construct_time)
        else:
            construct_time = index + \
                " match (d:T"+time+") create (b)-[:属性{name:'时间'}]->(d)"
            graph.run(construct_time)
    # 客机型号节点建立
    if plane != "":
        check_plane = plane
        find_plane = matcher.match(plane, name=plane).first()
        if find_plane == None:
            construct_plane = index + " match (g:模式{name:'客机型号'}) create(h:" + check_plane + \
                "{name:'"+check_plane + \
                "'}) create (g)-[:包含]->(h) create (b)-[:属性{name:'客机型号'}]->(h)"
            graph.run(construct_plane)
        else:
            construct_plane = index + \
                "match (h:"+check_plane+") create (b)-[:属性{name:'客机型号'}]->(h)"
            graph.run(construct_plane)
    # #航空公司节点建立
    if airline != "":
        check_airline = airline
        find_airline = matcher.match(airline, name=airline).first()
        if find_airline == None:
            construct_airline = index + " match (e:模式{name:'航空公司'}) create(f:" + check_airline + \
                "{name:'" + check_airline + \
                "'}) create (e)-[:包含]->(f) create (b)-[:属性{name:'航空公司'}]->(f)"
            graph.run(construct_airline)
        else:
            construct_airline = index + \
                "match (f:" + check_airline + \
                ") create (b)-[:属性{name:'航空公司'}]->(f)"
            graph.run(construct_airline)
    # 航班号节点建立
    if flightnum != "":
        construct_flight = index + "match (hbh:模式{name:'航班号'}) create(jhbh:h" + str(flightnum)+"{name:'" + str(
            flightnum) + "'}) create (hbh)-[:包含]->(jhbh) create (b)-[:属性{name:'航班号'}]->(jhbh)"
        graph.run(construct_flight)
    # 起飞地点节点建立
    if beginPlace != "":
        check_beginPlace = str(beginPlace)
        find_beginPlace = matcher.match(beginPlace, name=beginPlace).first()
        if find_beginPlace == None:
            construct_beginPlace = index + "match (qf:模式{name:'起飞地点'}) create(jqf:" + check_beginPlace + \
                "{name:'" + check_beginPlace + \
                "'}) create (qf)-[:包含]->(jqf) create (b)-[:属性{name:'起飞地点'}]->(jqf)"
            graph.run(construct_beginPlace)
        else:
            construct_beginPlace = index + \
                "match (qf:模式{name:'起飞地点'}) match(jqf:" + check_beginPlace + \
                ") create (qf)-[:包含]->(jqf) create (b)-[:属性{name:'起飞地点'}]->(jqf)"
            graph.run(construct_beginPlace)
    # 降落地点节点建立
    if landPlace != "":
        check_landPlace = str(landPlace)
        find_landPlace = matcher.match(landPlace, name=landPlace).first()
        if find_landPlace == None:
            construct_landPlace = index + " match (qf:模式{name:'降落地点'}) create(jqf:" + check_landPlace + \
                "{name:'" + check_landPlace + \
                "'}) create (qf)-[:包含]->(jqf) create (b)-[:属性{name:'降落地点'}]->(jqf)"
            graph.run(construct_landPlace)
        else:
            construct_landPlace = index + \
                " match (qf:模式{name:'降落地点'}) match(jqf:" + check_landPlace + \
                ") create (qf)-[:包含]->(jqf) create (b)-[:属性{name:'降落地点'}]->(jqf)"
            graph.run(construct_landPlace)
    # 出事地点节点建立
    if incidentPalce != "":
        check_incidentPlace = str(incidentPalce)
        if check_incidentPlace == "途中":
            construct_incidentPlace = index + \
                "match (a:途中） create (b)-[:属性{name:'出事地点'}]->(a)"
            graph.run(construct_incidentPlace)
        else:
            find_incidentPlace = matcher.match(
                incidentPalce, name=incidentPalce).first()
            if find_incidentPlace == None:
                construct_incidentPlace = index + " match(cs:模式{name:'出事地点'}) create(jcs:" + check_incidentPlace + \
                    "{name:'" + check_incidentPlace + \
                    "'}) create (cs)-[:包含]->(jcs) create (b)-[:属性{name:'出事地点'}]->(jcs)"
                graph.run(construct_incidentPlace)
            else:
                construct_incidentPlace = index + \
                    " match(cs:模式{name:'出事地点'}) match (jcs:" + check_incidentPlace + \
                    ") create (cs)-[:包含]->(jcs) create (b)-[:属性{name:'出事地点'}]->(jcs)"
                graph.run(construct_incidentPlace)
    # 事件类型节点建立
    if evenType != "":
        check_eventType = str(evenType)
        find_eventType = matcher.match(evenType, name=evenType).first()
        if find_eventType == None:
            construct_eventType = index + "match (sl:模式{name:'事件类型'}) create (jsl:" + check_eventType + \
                "{name:'" + check_eventType + \
                "'}) create (sl)-[:包含]->(jsl) create (b)-[:属性{name:'事件类型'}]->(jsl)"
            graph.run(construct_eventType)
        else:
            construct_eventType = index + \
                "match (jsl:" + check_eventType + \
                ") create (b)-[:属性{name:'事件类型'}]->(jsl)"
            graph.run(construct_eventType)
    # 航线类型节点建立
    if airlineType != "":
        check_airlineType = str(airlineType)
        if check_airlineType == "国际":
            construct_airlineType = index + \
                "match(jhl:国际) create (b)-[:属性{name:'航线类型'}]->(jhl)"
            graph.run(construct_airlineType)
        else:
            construct_airlineType = index + \
                "match(jhl:国内) create (b)-[:属性{name:'航线类型'}]->(jhl)"
            graph.run(construct_airlineType)
    # 航班类型节点建立
    if flightType != "":
        check_flightType = str(flightType)
        if check_flightType == "客运":
            construct_flightType = index + \
                "match (jhb:客运) create (b)-[:属性{name:'航班类型'}]->(jhb)"
            graph.run(construct_flightType)
        else:
            construct_flightType = index + \
                "match (jhb:货运) create (b)-[:属性{name:'航班类型'}]->(jhb)"
            graph.run(construct_flightType)
    # 天气情况节点建立
    if weather != "":
        check_weather = str(weather)
        find_weater = matcher.match(weather, name=weather).first()
        if find_weater == None:
            construct_weather = index + "match (tq:模式{name:'天气情况'}) create (jtq:" + check_weather + \
                "{name:'" + check_weather + \
                "'}) create (tq)-[:包含]->(jtq) create (b)-[:属性{name:'天气情况'}]->(jtq)"
            graph.run(construct_weather)
        else:
            construct_weather = index + \
                "match(jtq:" + check_weather + \
                ") create (b)-[:属性{name:'天气情况'}]->(jtq)"
            graph.run(construct_weather)
    # 操作阶段节点建立
    if stage != "":
        check_stage = str(stage)
        find_stage = matcher.match(stage, name=stage).first()
        if find_stage == None:
            construct_stage = index + "match (cj:模式{name:'操作阶段'}) create (jcj:" + check_stage + \
                "{name:'" + check_stage + \
                "'}) create (cj)-[:包含]->(jcj) create (b)-[:属性{name:'操作阶段'}]->(jcj)"
            graph.run(construct_stage)
        else:
            construct_stage = index + \
                "match(jcj:"+check_stage + \
                ") create (b)-[:属性{name:'操作阶段'}]->(jcj)"
            graph.run(construct_stage)
    # 原因节点建立
    # check_reason = reason
    if reason != "":
        find_reason = matcher.match(reason).first()
        if find_reason == None:
            construct_reason = index + "match (rea:模式{name:'原因'}) create (jrea:" + reason + \
                "{name:'" + reason + \
                "'}) create (rea)-[:包含]->(jrea) create (b)-[:属性{name:'原因'}]->(jrea)"
        else:
            construct_reason = index + \
                "match (jrea:" + reason + \
                "{name:'" + reason + "'}) create (b)-[:属性{name:'原因'}]->(jrea)"
        graph.run(construct_reason)
    # 结果节点建立
    if result != "":
        if result == "安全着陆":
            construct_result = index + \
                "match (a) where id(a)=7438 create (b)-[:属性{name:'结果'}]->(a)"
            graph.run(construct_result)
        else:
            # check_result = result
            find_result = matcher.match(result).first()
            if find_result == None:
                construct_result = index + "match (resul:模式{name:'结果'}) create (jresul:" + result + \
                    "{name:'" + result + \
                    "'}) create (resul)-[:包含]->(jresul) create (b)-[:属性{name:'结果'}]->(jresul)"
            else:
                construct_result = index + \
                    "match (jresul:" + result + \
                    "{name:'" + result + \
                    "'}) create (b)-[:属性{name:'结果'}]->(jresul)"
            graph.run(construct_result)
    # 人员伤亡节点建立
    if injured != "":
        if injured == "无":
            construct_injured = ""
        else:
            find_injured = matcher.match(injured, name=injured).first()
            if find_injured == None:
                construct_injured = index + "match (ry:模式{name:'人员伤亡'}) create (jresul:" + injured + \
                    "{name:'" + injured + \
                    "'}) create (ry)-[:包含]->(jresul) create (b)-[:属性{name:'人员伤亡'}]->(jresul)"
            else:
                construct_injured = index + \
                    "match (jresul:" + injured + \
                    "{name:'" + injured + \
                    "'}) create (b)-[:属性{name:'人员伤亡'}]->(jresul)"
            graph.run(construct_injured)
    # 事件等级节点建立
    if grade != "":
        find_grade = matcher.match(grade, name=grade).first()
        if find_grade == None:
            construct_grade = index + " match (dj:模式{name:'等级'}) create (jdj:" + grade + \
                "{name:'" + grade + \
                "'}) create (dj)-[:包含]->(jdj) create (b)-[:属性{name:'等级'}]->(jdj)"
            graph.run(construct_grade)
        else:
            construct_grade = index + \
                " match (jdj:" + grade + ") create (b)-[:属性{name:'等级'}]->(jdj)"
            graph.run(construct_grade)
