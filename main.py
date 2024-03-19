from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, send_from_directory, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from Forms.create_post_form import CreatePostForm
from flask_login import UserMixin, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


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


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

    def get_id(self):
        return str(self.id)  # Convert id to string since Flask-Login expects unicode strings

    @staticmethod
    def get(user_id):
        return User.query.get(int(user_id))  # Convert user_id to integer before querying the database

    def is_authenticated(self):
        # Define your authentication logic here
        return True  # For simplicity, always return True. Implement your logic accordingly.

    def is_active(self):
        # Define your activation logic here
        return True  # For simplicity, always return True. Implement your logic accordingly.

    def is_anonymous(self):
        return False  # Since we don't support anonymous users, always return False


# db.create_all()


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


@app.route('/user')
def all_user():
    results = db.session.query(User).all()
    for result in results:
        print(result.password)
    return "user"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect(url_for('secrets', name=user.name, logged_in=current_user.is_authenticated()))
        if not check_password_hash(user.password, password):
            flash("password is incorrect")
            return redirect(url_for('login'))
        else:
            flash(f"{request.form['email']} isn't found in the database")
            return redirect(url_for('login'))

    return render_template('login.html', logged_in=current_user.is_authenticated)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == "POST":
        # Check if the email already exists in the database

        if User.query.filter_by(email=request.form["email"]).first():
            flash(f'You Have already signed up using {request.form["email"]} ,Log in instead!')
            return redirect(url_for('login'))
        else:
            # If the email does not exist, hash the password and create a new user
            hashed_password = generate_password_hash(request.form["password"], method='pbkdf2:sha256', salt_length=8)
            print(hashed_password)
            new_user = User(
                email=request.form["email"],
                password=hashed_password,
                name=request.form["name"]
            )

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            # Log in the new user
            login_user(new_user)

            # Redirect to a page for authenticated users, passing the user's name as a parameter
            return redirect(url_for('secrets', name=request.form["name"]))

    # If the request method is GET, render the registration template
    return render_template('register.html', logged_in=current_user.is_authenticated)


@app.route('/download', methods=['GET'])
@login_required
def download_file():
    """This route will download a file """
    # downloading file dynamically
    return send_from_directory('static/files', filename='cheat_sheet.pdf', as_attachment=True)


@app.route('/secrets/<name>', methods=["GET"])
@login_required
def secrets(name):
    return render_template('secrets.html', name=name, logged_in=current_user.is_authenticated)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
