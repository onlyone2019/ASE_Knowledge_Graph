from py2neo import Graph, Node, Relationship, NodeMatcher
from flask import Flask
from flask_scss import Scss
class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    JSON_AS_ASCII = False
    PY2NEO_CONFIG = {       # py2neo 连接配置
        "host": "localhost",
        "username": "neo4j",
        "password": "zd0908101085"
    }

    @staticmethod
    def init_app(app):
        pass
    
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