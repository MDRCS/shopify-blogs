import os

from flask import Flask, render_template, request, session, make_response
from src.models.blog import Blog
from src.models.post import Post
from src.models.user import User
from src.common.database import Database

# user = User(email="mdr.ga99@gmail.com",password="lalamama123")
# # user.save_database()
# #print(Database.find_one('users',{}))
# blog = Blog(author="mdr.ga99@gmail.com", title="Technology", description="TechCrunch Disrupt", author_id="f86dee8d047545e5b711423f480dc294")
# for bl in Database.find('blogs',{}):
#     print(bl)
#
# blog.new_post("AGI","Artificiel Intelligence will conquer the world one day ? ..")


app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

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
    else:
        session['email'] = None

    return render_template("profile.html", email=session['email'])

@app.route("/auth/register",methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email,password)
    return render_template("profile.html", email=session['email'])

@app.route("/blogs/<string:user_id>")
@app.route("/blogs")
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.getById(user_id)
    else:
        user = User.getByEmail(session['email'])

    blogs = user.getBlogs()
    return render_template("user_blogs.html",blogs=blogs,email=user.email)

@app.route("/posts/<string:blog_id>")
def blog_posts(blog_id):
    blog = Blog.getOneBlog(blog_id)
    posts = blog.get_posts()
    return render_template("posts_listing.html",posts=posts,blog_name=blog.title,blog_id=blog_id )

@app.route("/post/<string:post_id>")
def blog_post(post_id):
    post = Post.findOnebyId(post_id)
    return render_template("post.html",post=post)

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


if __name__ == "__main__":
    app.run(port=4995)
