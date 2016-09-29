# coding=utf-8
from config import DATABASE_URI, MACHINE_NAME
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import BaseModel
import time

engine = create_engine(DATABASE_URI, encoding='utf-8')
DBSession = sessionmaker(engine)

from master.Master import Master
from slave.TaskWorker import TaskWorker


def run(role):
    BaseModel.metadata.create_all(engine)
    if role == 'master':
        server = Master()
    elif role == 'slave':
        server = TaskWorker(MACHINE_NAME)
    else:
        raise Exception('只支持master和slave参数')
    server.serve()
    while True:
        if not server.is_live():
            raise Exception('%s 守护线程已死亡' % type(server))
        time.sleep(1)
