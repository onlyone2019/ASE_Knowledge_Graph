from py2neo import *

# graph = Graph("http://localhost:7474", username="neo4j", password="comeon2017")
graph = Graph("http://localhost:7474",auth=('neo4j','comeon2017'))
matcher = NodeMatcher(graph)

#事件名称 时间 客机型号 航空公司 航班号 起飞地点 降落地点 出事地点
#事件类型 航线类型 航班类型 天气情况 操作阶段 原因 结果 人员伤亡 等级
def addevent(name, time, plane, airline, flightnum, beginPlace, landPlace, incidentPalce,
	evenType,airlineType,flightType,weather,stage,reason,result,injured,grade):
	event_name = "S" + name
	#添加事件名节点
	s = "match (a:事件名称) create (b:"+event_name+"{name:'"+name+"'}) create (a)-[:包含]->(b)"
	print(s)
	graph.run(s)
	index = "match (b:" + event_name + ")"
	print(index)
	#时间节点建立
	check_time = "T" + time
	find_result = matcher.match(check_time, name=time).first()
	print(find_result)
	if find_result==None:
		construct_time = index + " match (c:模式{name:'时间'}) create (d:T" + time +"{name:'"+time+"'}) create (c)-[:包含]->(d) create (b)-[:属性{name:'时间'}]->(d)"
		print(construct_time)
		graph.run(construct_time)
	else:
		construct_time = index + " match (d:T"+time+") create (b)-[:属性{name:'时间'}]->(d)"
		graph.run(construct_time)
	#客机型号节点建立
	check_plane = plane
	find_plane = matcher.match(plane, name=plane).first()
	print(find_plane)
	if find_plane==None:
		construct_plane = index + " match (g:模式{name:'客机型号'}) create(h:" + check_plane + "{name:'"+check_plane+"'}) create (g)-[:包含]->(h) create (b)-[:属性{name:'客机型号'}]->(h)"
		print(construct_plane)
		graph.run(construct_plane)
	else :
		construct_plane = index + "match (h:"+check_plane+") create (b)-[:属性{name:'客机型号'}]->(h)"
		print(construct_plane)
		graph.run(construct_plane)
	# #航空公司节点建立
	check_airline = airline
	find_airline =matcher.match(airline, name=airline).first()
	print(find_airline)
	if find_airline==None:
		construct_airline = index + " match (e:模式{name:'航空公司'}) create(f:"+ check_airline + "{name:'" + check_airline +"'}) create (e)-[:包含]->(f) create (b)-[:属性{name:'航空公司'}]->(f)"
		print(construct_airline)
		graph.run(construct_airline)
	else:
		construct_airline = index + "match (f:" + check_airline +") create (b)-[:属性{name:'航空公司'}]->(f)"
		print(construct_plane)
		graph.run(construct_airline)
	# 航班号节点建立
	construct_flight = index + "match (hbh:模式{name:'航班号'}) create(jhbh:h" +str(flightnum)+"{name:'"+ str(flightnum) +"'}) create (hbh)-[:包含]->(jhbh) create (b)-[:属性{name:'航班号'}]->(jhbh)"
	print(construct_flight)
	graph.run(construct_flight)
	#起飞地点节点建立
	check_beginPlace = str(beginPlace)
	find_beginPlace = matcher.match(beginPlace, name=beginPlace).first()
	print(find_beginPlace)
	if find_beginPlace == None:
		construct_beginPlace = index + "match (qf:模式{name:'起飞地点'}) create(jqf:"+ check_beginPlace +"{name:'"+ check_beginPlace +"'}) create (qf)-[:包含]->(jqf) create (b)-[:属性{name:'起飞地点'}]->(jqf)"
		print(construct_beginPlace)
		graph.run(construct_beginPlace)
	else:
		construct_beginPlace = index + "match (qf:模式{name:'起飞地点'}) match(jqf:"+ check_beginPlace +") create (qf)-[:包含]->(jqf) create (b)-[:属性{name:'起飞地点'}]->(jqf)"
		print(construct_beginPlace)
		graph.run(construct_beginPlace)
	#降落地点节点建立
	check_landPlace = str(landPlace)
	find_landPlace =matcher.match(landPlace, name=landPlace).first()
	print(find_landPlace)
	if find_landPlace == None:
		construct_landPlace = index + " match (qf:模式{name:'降落地点'}) create(jqf:" + check_landPlace + "{name:'"+ check_landPlace +"'}) create (qf)-[:包含]->(jqf) create (b)-[:属性{name:'降落地点'}]->(jqf)"
		print(construct_landPlace)
		graph.run(construct_landPlace)
	else:
		construct_landPlace = index + " match (qf:模式{name:'降落地点'}) match(jqf:" + check_landPlace +") create (qf)-[:包含]->(jqf) create (b)-[:属性{name:'降落地点'}]->(jqf)"
		print(construct_landPlace)
		graph.run(construct_landPlace)
	#出事地点节点建立
	check_incidentPlace = str(incidentPalce)
	if check_incidentPlace == "途中":
		construct_incidentPlace = index + "match (a:途中） create (b)-[:属性{name:'出事地点'}]->(a)"
		graph.run(construct_incidentPlace)
	else:
		find_incidentPlace = matcher.match(incidentPalce, name=incidentPalce).first()
		print(find_incidentPlace)
		if find_incidentPlace == None:
			construct_incidentPlace = index + " match(cs:模式{name:'出事地点'}) create(jcs:"+ check_incidentPlace + "{name:'" +check_incidentPlace +"'}) create (cs)-[:包含]->(jcs) create (b)-[:属性{name:'出事地点'}]->(jcs)"
			graph.run(construct_incidentPlace)
		else:
			construct_incidentPlace = index + " match(cs:模式{name:'出事地点'}) match (jcs:" + check_incidentPlace +") create (cs)-[:包含]->(jcs) create (b)-[:属性{name:'出事地点'}]->(jcs)"
			graph.run(construct_incidentPlace)
	#事件类型节点建立
	check_eventType = str(evenType)
	find_eventType = matcher.match(evenType, name=evenType).first()
	print(find_eventType)
	if find_eventType ==None:
		construct_eventType = index + "match (sl:模式{name:'事件类型'}) create (jsl:"+ check_eventType + "{name:'"+ check_eventType +"'}) create (sl)-[:包含]->(jsl) create (b)-[:属性{name:'事件类型'}]->(jsl)"
		graph.run(construct_eventType)
	else:
		construct_eventType = index + "match (jsl:"+ check_eventType +") create (b)-[:属性{name:'事件类型'}]->(jsl)"
		graph.run(construct_eventType)
	#航线类型节点建立
	check_airlineType = str(airlineType)
	if check_airlineType == "国际":
		construct_airlineType = index + "match(jhl:国际) create (b)-[:属性{name:'航线类型'}]->(jhl)"
		graph.run(construct_airlineType)
	else:
		construct_airlineType = index + "match(jhl:国内) create (b)-[:属性{name:'航线类型'}]->(jhl)"
		graph.run(construct_airlineType)
	#航班类型节点建立
	check_flightType = str(flightType)
	if check_flightType == "客运":
		construct_flightType = index + "match (jhb:客运) create (b)-[:属性{name:'航班类型'}]->(jhb)"
		graph.run(construct_flightType)
	else:
		construct_flightType = index + "match (jhb:货运) create (b)-[:属性{name:'航班类型'}]->(jhb)"
		graph.run(construct_flightType)
	#天气情况节点建立
	check_weather = str(weather)
	find_weater = matcher.match(weather, name=weather).first()
	print(find_weater)
	if find_weater==None:
		construct_weather = index + "match (tq:模式{name:'天气情况'}) create (jtq:"+ check_weather +"{name:'"+ check_weather +"'}) create (tq)-[:包含]->(jtq) create (b)-[:属性{name:'天气情况'}]->(jtq)"
		graph.run(construct_weather)
	else:
		construct_weather = index + "match(jtq:"+ check_weather +") create (b)-[:属性{name:'天气情况'}]->(jtq)"
		graph.run(construct_weather)
	#操作阶段节点建立
	check_stage = str(stage)
	find_stage = matcher.match(stage, name=stage).first()
	print(find_stage)
	if find_stage == None:
		construct_stage = index + "match (cj:模式{name:'操作阶段'}) create (jcj:" + check_stage +"{name:'"+ check_stage +"'}) create (cj)-[:包含]->(jcj) create (b)-[:属性{name:'操作阶段'}]->(jcj)"
		graph.run(construct_stage)
	else:
		construct_stage = index + "match(jcj:"+check_stage +") create (b)-[:属性{name:'操作阶段'}]->(jcj)"
		graph.run(construct_stage)
	#原因节点建立
	# check_reason = reason
	find_reason = matcher.match(reason).first()
	if find_reason==None:
		construct_reason = index + "match (rea:模式{name:'原因'}) create (jrea:"+ reason +"{name:'"+ reason +"'}) create (rea)-[:包含]->(jrea) create (b)-[:属性{name:'原因'}]->(jrea)"
	else:
		construct_reason = index + "match (jrea:"+ reason +"{name:'"+ reason +"'}) create (b)-[:属性{name:'原因'}]->(jrea)"
	graph.run(construct_reason)
	#结果节点建立
	if result == "安全着陆":
		construct_result = index + "match (a) where id(a)=7438 create (b)-[:属性{name:'结果'}]->(a)"
		graph.run(construct_result)
	else:
		# check_result = result
		find_result = matcher.match(result).first()
		if find_result==None:
			construct_result = index + "match (resul:模式{name:'结果'}) create (jresul:"+ result +"{name:'"+ result +"'}) create (resul)-[:包含]->(jresul) create (b)-[:属性{name:'结果'}]->(jresul)"
		else:
			construct_result = index + "match (jresul:"+ result +"{name:'"+ result +"'}) create (b)-[:属性{name:'结果'}]->(jresul)"
		graph.run(construct_result)
	#人员伤亡节点建立
	if injured == "无":
		construct_injured = ""
	else:
		find_injured = matcher.match(injured, name=injured).first()
		print(find_injured)
		if find_injured==None:
			construct_injured = index + "match (ry:模式{name:'人员伤亡'}) create (jresul:"+ injured +"{name:'"+ injured +"'}) create (ry)-[:包含]->(jresul) create (b)-[:属性{name:'人员伤亡'}]->(jresul)"
		else:
			construct_injured=index+"match (jresul:"+ injured +"{name:'"+ injured +"'}) create (b)-[:属性{name:'人员伤亡'}]->(jresul)"
		graph.run(construct_injured)
	#事件等级节点建立
	find_grade = matcher.match(grade, name=grade).first()
	print(find_grade)
	if find_grade == None:
	    construct_grade = index + " match (dj:模式{name:'等级'}) create (jdj:"+ grade + "{name:'" + grade +"'}) create (dj)-[:包含]->(jdj) create (b)-[:属性{name:'等级'}]->(jdj)"
	    graph.run(construct_grade)
	else:
	    construct_grade = index + " match (jdj:"+ grade +") create (b)-[:属性{name:'等级'}]->(jdj)"
	    graph.run(construct_grade)

print("begin")
addevent("1023DL_1234", "2011231", "Boeing747_123", "qwefqwefqe", "DL_1234","aaacd", "成cawec",
	"case", "发动机故障", "国际", "客运", "不恶劣", "爬升", "test",
	"cewf", "无", "一般")
print("end")
