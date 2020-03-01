import uuid
from .post import Post
from src.common.database import Database


class Blog(object):
    def __init__(self,author,title,description,author_id,_id,id=None):
        self.author = author
        self.author_id = author_id
        self.title = title
        self.description = description
        self.id = id if id else uuid.uuid4().hex

    def new_post(self,title,content):
        post = Post(blog_id=self.id,title=title,content=content,author=self.author)
        post.save_database()

    def get_posts(self):
        return Post.findbyBlogId(self.id)

    def save_database(self):
        Database.insert('blogs', self.json())

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "author": self.author,
            "author_id": self.author_id
        }

    @classmethod
    def getOneBlog(cls,id):
        blog_info = Database.find_one(collection='blogs',query={'id': id})
        #author=blog_info['author'],title=blog_info['title'],description=blog_info['description'],id=blog_info['id']
        return cls(**blog_info)

    @classmethod
    def getBlogsByAuthorId(cls,author_id):
        return [cls(**blog) for blog in Database.find('blogs', {'author_id':author_id})]

