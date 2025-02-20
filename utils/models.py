from instagrapi.types import DirectThread, DirectItem, User as InstaUser

class Message:
    def __init__(self, item, thread):
        self.item = item
        self.thread = thread
        
    @property
    def text(self):
        return self.item.text
        
    @property
    def sender(self):
        return User(self.item.user)
        
class User:
    def __init__(self, user: InstaUser):
        self.user = user
        
    @property
    def username(self):
        return self.user.username
        
    @property
    def pk(self):
        return self.user.pk