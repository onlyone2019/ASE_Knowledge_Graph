# ASE_Knowledge_Graph
a knowledge graph of aviation safety event 

onlyone 负责数据库建立，数据库备份数据会以7_30_8.dump（7月30日备份文件包含8个事件信息）文件形式上传。
使用命令 "./neo4j-admin load --from=/home/2016-10-02.dump --database=graph.db --force" 可恢复数据库。
数据库备注：
所有事件名称与Excel表格里面数据有所差别，如原始记录为12.20AS-73的时间名称数据库中将会存为 1220AS_73。已存入数据库的数据存放在sheet2中，还未存的数据存放在sheet1中。

marsvet 负责前端设计

xingxingyxx 负责后端逻辑
