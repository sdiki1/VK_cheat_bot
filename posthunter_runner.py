from threading import Thread as th
import time
from cheating import Likes, Reposts, Comments, Monitor
class PostHunter:
    def __init__(self):
        ...
    
    def run_comments(self):
        Comments().start()
    
    def run_likes(self):
        Likes().start()
    
    def run_reposts(self):
        Reposts().start()
    
    def run_posthunter(self):
        Monitor().run()

    def run(self):
        th(target=self.run_comments).start()
        time.sleep(0.1)
        th(target=self.run_likes).start()
        time.sleep(0.1)
        th(target=self.run_reposts).start()
        time.sleep(0.1)
        th(target=self.run_posthunter).start()
        print("Run")

if __name__ == "__main__":
    PostHunter().run()
