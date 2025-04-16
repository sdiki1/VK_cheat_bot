from threading import Thread as th
import time
from cheating import Likes
class PostHunter:
    def __init__(self):
        ...
    
    def run_comments(self):
        print("run comments")
    
    def run_likes(self):
        Likes().start()
    
    def run_reposts(self):
        print("run reposts")
    
    def run_posthunter(self):
        print("run posthunter")

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
