from instagrapi import Client

class RESTClient:
    def __init__(self, client):
        self.client = client
        
    def get_user_info(self, username):
        return self.client.user_info_by_username(username)
        
    def get_media(self, media_pk):
        return self.client.media_info(media_pk)
        
    def search_users(self, query):
        return self.client.user_search(query)