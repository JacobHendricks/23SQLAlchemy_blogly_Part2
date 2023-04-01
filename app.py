"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "ihaveasecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


connect_db(app)
# db.create_all()


@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


##############################################################################
# User route


@app.route('/users')
def users_page():
    """Shows page with all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/users.html', users=users)


@app.route('/users/new')
def user_form():
    """New user form"""
    return render_template('users/add.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    """Submit form to add user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name,
                    image_url=image_url or None)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Show details about single user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id)
    return render_template('users/details.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    """Show edit user page"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Submit form to edit user data"""
    user = User.query.get_or_404(user_id)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.first_name} {user.last_name} deleted.")

    return redirect('/users')

##############################################################################
# Posts route


@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """New post form"""
    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_form_submit(user_id):
    """Submit form to add new post"""

    user = User.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user_id=user.id)
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def post(post_id):
    """Show details about single post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show form to edit details about single post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def Submit_edit(post_id):
    """Handle form submission for updating a single post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    flash(f"Post '{post.title}' edited.")

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete single post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")


# from flask import Flask, request, redirect, render_template, flash
# from flask_debugtoolbar import DebugToolbarExtension
# from models import db, connect_db, User, Post

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'ihaveasecret'

# # Having the Debug Toolbar show redirects explicitly is often useful;
# # however, if you want to turn it off, you can uncomment this line:
# #
# # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# toolbar = DebugToolbarExtension(app)

# connect_db(app)
# db.create_all()


# @app.route('/')
# def root():
#     """Show recent list of posts, most-recent first."""

#     posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
#     return render_template("posts/homepage.html", posts=posts)


# @app.errorhandler(404)
# def page_not_found(e):
#     """Show 404 NOT FOUND page."""

#     return render_template('404.html'), 404


# ##############################################################################
# # User route

# @app.route('/users')
# def users_index():
#     """Show a page with info on all users"""

#     users = User.query.order_by(User.last_name, User.first_name).all()
#     return render_template('users/index.html', users=users)


# @app.route('/users/new', methods=["GET"])
# def users_new_form():
#     """Show a form to create a new user"""

#     return render_template('users/new.html')


# @app.route("/users/new", methods=["POST"])
# def users_new():
#     """Handle form submission for creating a new user"""

#     new_user = User(
#         first_name=request.form['first_name'],
#         last_name=request.form['last_name'],
#         image_url=request.form['image_url'] or None)

#     db.session.add(new_user)
#     db.session.commit()
#     flash(f"User {new_user.full_name} added.")

#     return redirect("/users")


# @app.route('/users/<int:user_id>')
# def users_show(user_id):
#     """Show a page with info on a specific user"""

#     user = User.query.get_or_404(user_id)
#     return render_template('users/show.html', user=user)


# @app.route('/users/<int:user_id>/edit')
# def users_edit(user_id):
#     """Show a form to edit an existing user"""

#     user = User.query.get_or_404(user_id)
#     return render_template('users/edit.html', user=user)


# @app.route('/users/<int:user_id>/edit', methods=["POST"])
# def users_update(user_id):
#     """Handle form submission for updating an existing user"""

#     user = User.query.get_or_404(user_id)
#     user.first_name = request.form['first_name']
#     user.last_name = request.form['last_name']
#     user.image_url = request.form['image_url']

#     db.session.add(user)
#     db.session.commit()
#     flash(f"User {user.full_name} edited.")

#     return redirect("/users")


# @app.route('/users/<int:user_id>/delete', methods=["POST"])
# def users_destroy(user_id):
#     """Handle form submission for deleting an existing user"""

#     user = User.query.get_or_404(user_id)
#     db.session.delete(user)
#     db.session.commit()
#     flash(f"User {user.full_name} deleted.")

#     return redirect("/users")


# ##############################################################################
# # Posts route


# @app.route('/users/<int:user_id>/posts/new')
# def posts_new_form(user_id):
#     """Show a form to create a new post for a specific user"""

#     user = User.query.get_or_404(user_id)
#     return render_template('posts/new.html', user=user)


# @app.route('/users/<int:user_id>/posts/new', methods=["POST"])
# def posts_new(user_id):
#     """Handle form submission for creating a new post for a specific user"""

#     user = User.query.get_or_404(user_id)
#     new_post = Post(title=request.form['title'],
#                     content=request.form['content'],
#                     user=user)

#     db.session.add(new_post)
#     db.session.commit()
#     flash(f"Post '{new_post.title}' added.")

#     return redirect(f"/users/{user_id}")


# @app.route('/posts/<int:post_id>')
# def posts_show(post_id):
#     """Show a page with info on a specific post"""

#     post = Post.query.get_or_404(post_id)
#     return render_template('posts/show.html', post=post)


# @app.route('/posts/<int:post_id>/edit')
# def posts_edit(post_id):
#     """Show a form to edit an existing post"""

#     post = Post.query.get_or_404(post_id)
#     return render_template('posts/edit.html', post=post)


# @app.route('/posts/<int:post_id>/edit', methods=["POST"])
# def posts_update(post_id):
#     """Handle form submission for updating an existing post"""

#     post = Post.query.get_or_404(post_id)
#     post.title = request.form['title']
#     post.content = request.form['content']

#     db.session.add(post)
#     db.session.commit()
#     flash(f"Post '{post.title}' edited.")

#     return redirect(f"/users/{post.user_id}")


# @app.route('/posts/<int:post_id>/delete', methods=["POST"])
# def posts_destroy(post_id):
#     """Handle form submission for deleting an existing post"""

#     post = Post.query.get_or_404(post_id)

#     db.session.delete(post)
#     db.session.commit()
#     flash(f"Post '{post.title} deleted.")

#     return redirect(f"/users/{post.user_id}")
