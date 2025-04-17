from hmac import new
import threading, datetime
import time, vk_api, random
from typing import Optional
from queue import Queue
from requests import session
from sqlalchemy import and_, or_, func
from tg_bot.models import Task, Account, sessionmaker, services, engine



class Reposts:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        self.db = session
        self.task_queue = Queue()
        self.active_threads = []
        self.is_running = False
        self.max_threads = 5
        self.check_interval = 1

    def start(self):
        self.is_running = True
        threading.Thread(target=self._monitor_tasks).start()

    def stop(self):
        self.db.close()
        self.is_running = False

    def _monitor_tasks(self):

        while True:
            self._check_new_tasks()
            time.sleep(self.check_interval)
        print(self.is_running)

    def _check_new_tasks(self):
        try:


            new_tasks = self.db.query(Task).filter(
                Task.type == 'repost',
                Task.status == 'pending',
                Task.account.is_(None),
                Task.next_run<datetime.datetime.now()
            ).limit(10).all() + self.db.query(Task).filter(
                Task.type == 'repost',
                Task.status == 'failed',
                Task.account.is_(None),
                Task.next_run<datetime.datetime.now()
            ).limit(10).all()
            # print(new_tasks)
            for task in new_tasks:
                if not self._is_task_in_queue(task.id):
                    self.task_queue.put(task)

            self._balance_threads()

        except Exception as e:
            print(e)

    def _is_task_in_queue(self, task_id: int) -> bool:
        return any(task.id == task_id for task in list(self.task_queue.queue))

    def _balance_threads(self):
        current_threads = sum(1 for t in self.active_threads if t.is_alive())
        
        while (current_threads < self.max_threads and 
               not self.task_queue.empty() and 
               self.is_running):
            
            task = self.task_queue.get()
            thread = threading.Thread(
                target=self._process_task,
                args=(task,),
                daemon=True
            )
            thread.start()
            self.active_threads.append(thread)
            current_threads += 1
            # time.sleep(1)

        self.active_threads = [t for t in self.active_threads if t.is_alive()]

    def _process_task(self, task: Task):
        try:
            
            account = self._get_available_account(task.url)
            account_token = account.token
            if not account:
                self.task_queue.put(task)
                print("no account")
                return
            session2 = sessionmaker(bind=engine)()
            task = session2.query(Task).filter(Task.id == task.id).first()
            task.account = account.token
            task.status = 'processing'
            task_id = task.id
            session2.add(task)
            session2.commit()
            session2.close()
            
            success = self.set_repost(account_token, task_id)

            session2 = sessionmaker(bind=engine)()
            task = session2.query(Task).filter(Task.id == task_id).first()
            task.status = 'completed' if success else 'failed'
            session2.add(task)
            session2.commit()
            session2.close()

        except Exception as e:
            print(e)
            session2 = sessionmaker(bind=engine)()
            task = session2.query(Task).filter(Task.id == task_id).first()
            task.status = 'failed'
            self.db.commit()
            session2.add(task)
            session2.commit()
            session2.close()

    def _get_available_account(self, post_url: str) -> Optional[Account]:
        try:
            accs = self.db.query(Task.account).filter(Task.url == post_url).filter(Task.type=="report").all()
            accs2 = [i[0] for i in accs if i[0] is not None]
            return self.db.query(Account).filter(Account.is_banned == False).filter(Account.token.not_in(accs2)).order_by(func.random()).first()
        except Exception as e:
            print(e)

    def set_repost(self, account_token: str, task_id: int) -> bool:
        print("create data")
        
        session2 = sessionmaker(bind=engine)()
        task = session2.query(Task).filter(Task.id == task_id).first()
        url = task.url

        data = url[url.find("wall"):]
        print(data)
        print("done")
        session = vk_api.VkApi(token=task.account)
        session.http.headers['User-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0'
        api = session.get_api()
        owner_id = int(data.split("_")[0])
        try:
            api.group.join(group_id=owner_id)
        except:
            pass
        id = api.account.get_profile_info()["id"]
        print(id)
        r = api.messages.send(user_id=id, attachment=data, random_id=0)
        print(r)
        task.status = 'completed'
        session2.add(task)
        session2.commit()
        return True
    