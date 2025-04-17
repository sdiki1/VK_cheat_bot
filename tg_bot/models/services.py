from .DBSM import Session, Task, engine
from datetime import datetime, timedelta
import random

class TaskManager:
    @staticmethod
    def create_task(task_type, url, params, interval):
        session = Session()
        try:
            task = Task(
                type=task_type,
                url=url,
                parameters=params,
                interval=interval,
                next_run=datetime.now() + timedelta(seconds=interval)
            )
            print("next run:", datetime.now() + timedelta(seconds=interval))
            session.add(task)
            session.commit()
            print("TASK CHanged")
            return task
        finally:
            session.close()

    @staticmethod
    def get_due_tasks():
        session = Session()
        try:
            return session.query(Task).filter(
                Task.status == 'pending',
                Task.next_run <= datetime.now()
            ).all()
        finally:
            session.close()

    @staticmethod
    def reschedule_task(task_id):
        session = Session()
        try:
            task = session.query(Task).get(task_id)
            if task:
                if task.type == 'repost':
                    interval = random.randint(120, 180)
                else:
                    interval = task.interval
                
                task.next_run = datetime.now() + timedelta(seconds=interval)
                session.commit()
        finally:
            session.close()
    
    @staticmethod
    def mark_task_completed(task_id):
        session = Session()
        try:
            task = session.query(Task).get(task_id)
            if task:
                task.status = 'completed'
                session.commit()
        finally:
            session.close()

    @staticmethod
    def mark_task_failed(task_id):
        session = Session()
        try:
            task = session.query(Task).get(task_id)
            if task:
                task.status = 'failed'
                session.commit()
        finally:
            session.close()