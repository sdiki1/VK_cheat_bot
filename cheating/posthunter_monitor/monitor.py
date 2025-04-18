import datetime, random, time
from tg_bot.models import Task, Account, sessionmaker, services, engine, PostHunterRequest, TaskManager
import vk_api
class Monitor:
    def __init__(self):
        ...

    def run(self):
        while True:
            Session = sessionmaker(bind=engine)
            session2 = Session()
            Hunted = session2.query(PostHunterRequest).all()
            account = session2.query(Account).filter(Account.is_banned==False).first()

            session = vk_api.VkApi(token=account.token)
            session.http.headers['User-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0'
            api = session.get_api()

            for hunt in Hunted:
                is_changed = False
                for url in hunt.group_url:
                    
                    if url[-1] == "/":
                        domain = url.split("/")[-2]
                    else:
                        domain = url.split("/")[-1]
                    # hunt.created_at = datetime.datetime.now()
                    ans = api.wall.get(domain=domain)
                    for i in ans["items"]:
                        date = i["date"]
                        date_post = datetime.datetime.fromtimestamp(date)
                        if date_post < hunt.created_at:
                            continue
                        is_comment=False
                        comments = api.wall.get_comments(owner_id=i["from_id"], post_id=i["id"])
                        for j in comments["items"]:
                            if hunt.keyword in j["text"]:
                                is_comment = True
                        print(date_post, hunt.created_at, is_comment, date_post >= hunt.created_at)
                        
                        if date_post >= hunt.created_at and is_comment:
                            is_changed = True
                            intervals = {
                                'like': random.randint(20, 30),
                                'comment': random.randint(60, 70),
                                'repost': random.randint(120, 180)
                            }
                            quantity = 3
                            url = f"https://vk.com/wall{i['from_id']}_{i['id']}"
                            task_type = "comment"
                            quantity = hunt.comments
                            for i in range(quantity):
                                interval = hunt.interval*i
                                TaskManager.create_task(
                                    task_type=task_type,
                                    url=url,
                                    params={'comment_text':'comment_text'},
                                    interval=interval
                                )
                            task_type = "like"
                            quantity = hunt.likes
                            for i in range(quantity):
                                interval = hunt.interval*i
                                TaskManager.create_task(
                                    task_type=task_type,
                                    url=url,
                                    params={'comment_text':'comment_text'},
                                    interval=interval
                                )
                            task_type = "repost"
                            quantity = hunt.reposts
                            for i in range(quantity):
                                interval = hunt.interval*i
                                TaskManager.create_task(
                                    task_type=task_type,
                                    url=url,
                                    params={'comment_text':'comment_text'},
                                    interval=interval)
                if is_changed:
                    hunt.created_at = datetime.datetime.now()
            session2.commit()
            session2.close()
            time.sleep(25)


