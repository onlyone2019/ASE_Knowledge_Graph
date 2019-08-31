# ASE_Knowledge_Graph

A knowledge graph of aviation safety event.

## 任务分工

@onlyone 负责数据库建立，数据库备份数据会以 7_30_8.dump（7 月 30 日备份文件包含 8 个事件信息）文件形式上传。

恢复数据库：

```powershell
./neo4j-admin load --from=/home/2016-10-02.dump --database=graph.db --force
```

数据库备注：所有事件名称与 Excel 表格里面数据有所差别，如原始记录为 12.20AS-73 的时间名称数据库中将会存为 1220AS_73。已存入数据库的数据存放在 sheet2 中，还未存的数据存放在 sheet1 中。

@marsvet 负责前端设计。

@xingxingyxx 负责后端逻辑。

## 项目预览

在线演示地址：[http://47.94.94.136:5000](http://47.94.94.136:5000)

## 如何贡献

步骤（注：前两步只在第一次运行时执行）：

1. 安装用于管理 python 虚拟环境的包 `pipenv`：

   ```bash
   pip install pipenv
   ```

2. 进入项目目录，创建虚拟环境并安装依赖包：

   ```bash
   cd ASE_Knowledge_Graph
   pipenv install	# 这一步如果失败，将 Pipfile 和 Pipfile.lock 中的 python_version 改为你电脑里安装的 Python 版本即可
   ```

3. 进入虚拟环境：

   ```bash
   pipenv shell
   ```

4. 配置临时环境变量（临时环境变量仅在当前 shell 中有效）：

   Linux / Mac OS:

   ```bash
   export FLASK_APP=app/app.py  # 指定次应用的入口文件
   export FLASK_DEBUG=1	# 开启 debug 模式
   ```

   Windows cmd:

   ```cmd
   set FLASK_APP=app/app.py
   set FLASK_DEBUG=1
   ```

   Windows powershell:

   ```powershell
   $Env:FLASK_APP=app/app.py
   $Env:FLASK_DEBUG=1
   ```

5. 启动应用程序：

   ```bash
   flask run    # 或 python -m flask run
   ```

6. 启动 neo4j 数据库

7. 浏览器输入 `http://localhost:5000` 即可访问。
