import uuid
from datetime import datetime
from src.common.database import Database

class Comment(object):
    def __init__(self,commenter,commentator,created_at="",_id=None,id=None):
        self.id = id if id is not None else uuid.uuid4().hex
        self.commenter = commenter
        self.commentator = commentator
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return "<Comments {}>".format(self.json())

    def save_database(self):
        Database.insert(collection='comments', data=self.json())

    @classmethod
    def findByAuthor(cls,commentator):
        comments = [cls(**comment) for comment in Database.find('comments',{"commentator": commentator})]
        return comments

    @classmethod
    def findById(cls,comment_id):
        return cls(**Database.find_one('comments', {"id": comment_id}))

    def json(self):
        return {
            "id": self.id,
            "commenter": self.commenter,
            "commentator": self.commentator,
            "created_at": self.created_at
        }
