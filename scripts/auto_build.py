# -*- coding: utf-8 -*-
import pandas as pd
from py2neo import Graph, Node, Relationship

invoice_data = pd.read_excel('./event.xls', header=0, encoding='utf8')
graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="*******"
)

pattren_node = []
data_node = []
sumnode = []


def Pattern_graph_node():
    for i in range(0, len(invoice_data.columns)):
        pattren_node.append(invoice_data.columns[i])
    print(pattren_node)  # 模式图（表头）结点

    # 创建模式图单个结点，存入总结点列表
    for i in range(0, len(pattren_node)):
        node = Node('模式数据属性', name=pattren_node[i])
        graph.create(node)
        sumnode.append(node)


def build_link():
    for i in range(0, len(pattren_node)):
        for n in range(0, len(invoice_data.columns)):
            # 获取每一单行数据
            data_node.append(invoice_data[invoice_data.columns[n]][i])
        data_strnode = [str(k) for k in data_node]  # 转化为字符串
        # 建立事件头结点
        node = Node('数据', name=data_strnode[0])
        graph.create(node)
        p_r1 = Relationship(sumnode[0], '包含', node)
        graph.create(p_r1)
        for t in range(1, len(invoice_data.columns)):
            node1 = Node('数据', name=data_strnode[t])
            graph.create(node1)
            p_r = Relationship(sumnode[t], '包含', node1)  # 建立模式结点与数据结点包含关系
            graph.create(p_r)
            self_r = Relationship(node, '属性', node1)  # 建立事件头结点与其他数据结点属性关系
            graph.create(self_r)
        data_node.clear()  # 清空该单行数据


Pattern_graph_node()
build_link()
