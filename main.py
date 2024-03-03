from datetime import datetime

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy

from Forms.create_post_form import CreatePostForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = db.session.query(BlogPost).get(index)
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/edit/<int:post_id>", methods=["GET", 'POST'])
def edit_post(post_id):
    """This route will edit the post"""
    post = db.session.query(BlogPost).get(post_id)
    edit_form = CreatePostForm(
        title=post.title, subtitle=post.subtitle, author=post.author, img_url=post.img_url, body=post.body
    )
    if edit_form.validate_on_submit():
        # modifying the post
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.author = edit_form.author.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for('show_post', index=post_id))
    return render_template('make-post.html', form=edit_form, editing=True)


@app.route("/create_post", methods=["GET", "POST"])
def create_new_post():
    """This route is used to create a new post"""

    # creating post
    create_form = CreatePostForm()
    if create_form.validate_on_submit():
        title = create_form.title.data
        subtitle = create_form.subtitle.data
        body = create_form.body.data
        img_url = create_form.img_url.data
        author = create_form.author.data
        modified_date = datetime.now().strftime("%B %d,%Y")
        # making a new post in the db
        new_post = BlogPost(title=title, subtitle=subtitle, body=body, author=author, date=modified_date,
                            img_url=img_url)
        db.session.add(new_post)
        try:
            db.session.commit()
            return redirect(url_for('get_all_posts'))
        except Exception as e:
            db.session.rollback()
            print(e)

    return render_template('make-post.html', form=CreatePostForm())


@app.route('/delete/<int:post_id>', methods=['GET'])
def delete_post(post_id):
    """This route will delete a certain post"""
    deleted_post = BlogPost.query.get(post_id)
    db.session.delete(deleted_post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
