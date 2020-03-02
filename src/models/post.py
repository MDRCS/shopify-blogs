import uuid
from datetime import datetime
from src.common.database import Database
import pymongo

class Post(object):

    def __init__(self,blog_id,title,content,author,_id=0,created_at="",comments=[],id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_at = datetime.utcnow()
        self.id = id if id else uuid.uuid4().hex
        self.comments = []
        self.comments.extend(comments) #comments_ids
        #today.strftime("%d-%m-%Y %H:%m:%2.s")

    def save_database(self):
        Database.insert(collection='posts', data=self.json())

    def update_record(self,data):
        Database.update(collection='posts',query={'id':self.id},data=data)

    @classmethod
    def findOnebyId(cls,id):
        post_info =  Database.find_one(collection='posts',query={'id': id})
        #return cls(blog_id=post_info['blog_id'],title=post_info['title'],content=post_info['content'],author=post_info['author'],id=post_info['id'])
        return cls(**post_info)

    @classmethod
    def findbyBlogId(cls, id):
        blog_posts = [cls(**post) for post in Database.find(collection='posts', query={'blog_id': id})]
        # cls(blog_id=blog_posts_info['blog_id'],title=blog_posts_info['title'],content=blog_posts_info['content'],author=blog_posts_info['author'],id=blog_posts_info['id'])
        return blog_posts

    def __repr__(self):
        return "<Post {}>".format(self.json())

    def json(self):
        return {
            "id": self.id,
            "blog_id": self.blog_id,
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "created_at": self.created_at,
            "comments": self.comments
        }

