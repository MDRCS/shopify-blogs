import os

from flask import Flask, render_template, request, session, make_response
from src.models.blog import Blog
from src.models.post import Post
from src.models.user import User
from src.models.comment import Comment
from src.common.database import Database
import pymongo

app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/logout")
def logout():
    User.logout(session['email'])
    return render_template("home.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/auth/login",methods=['POST'])
def login_user():
    """
    login.html
    <input type="text" id="email" name="email">
	<input type="password" id="password" name="password">
	"""

    email = request.form['email'] #Get email from request -> name attribut
    password = request.form['password']
    if User.valid_login(email, password):
        User.login(email)
        user = User.getByEmail(email)
        return make_response(user_blogs(user.id))
    else:
        session['email'] = None
        return render_template("profile.html", email=session['email'])


@app.route("/auth/register",methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    User.register(email,password)
    # return render_template("profile.html", email=session['email'])
    user = User.getByEmail(email)
    return make_response(user_blogs(user.id))

@app.route("/blogs/<string:user_id>")
@app.route("/blogs")
def user_blogs(user_id=None):
    try:
        test_session = session['email']
    except KeyError as e:
        return make_response(login_page())
    else:
        if user_id is not None:
            user = User.getById(user_id)
        else:
            user = User.getByEmail(session['email'])

        blogs = user.getBlogs()
        return render_template("user_blogs.html", blogs=blogs, email=user.email)

@app.route("/posts/<string:blog_id>")
def blog_posts(blog_id):
    blog = Blog.getOneBlog(blog_id)
    posts = blog.get_posts()
    return render_template("posts_listing.html",posts=posts,blog_name=blog.title,blog_id=blog_id )

@app.route("/post/<string:post_id>")
def blog_post(post_id):
    post = Post.findOnebyId(post_id)
    comments = []
    if len(post.comments) != 0:
        for comment_id in post.comments:
            comments.append(Comment.findById(comment_id))
    return render_template("post.html",post=post,comments=comments)

@app.route("/blogs/new",methods=['POST','GET'])
def create_newblog():
    if request.method == 'GET':
        return render_template("newblog.html")
    else:
        user = User.getByEmail(session['email'])
        title = request.form['title']
        description = request.form['description']
        blog = Blog(author=user.email,title=title,description=description,author_id=user.id,_id=0)
        blog.save_database()
        return make_response(user_blogs(user.id))

@app.route("/posts/new/<string:blog_id>",methods=['POST','GET'])
def create_newpost(blog_id):
    if request.method == 'GET':
        return render_template("newpost.html",blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        blog = Blog.getOneBlog(blog_id)
        post = Post(blog_id=blog.id, title=title, content=content, author=blog.author, created_at=0,_id=0)
        post.save_database()

        return make_response(blog_posts(blog.id))

@app.route("/comments/new/<string:post_id>/<string:post_author>",methods=['POST'])
def create_post_comment(post_id,post_author):
    commenter = request.form['commenter']
    comment = Comment(commenter,post_author,post_id)
    comment.save_database()
    post = Post.findOnebyId(post_id)
    post.comments.append(comment.id)
    post.update_record(post.json())
    return make_response(blog_post(post_id))

if __name__ == "__main__":
    app.run(port=4995)
