from flask import Flask, abort, render_template, redirect, url_for, flash, send_from_directory,request,session,jsonify
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from flask_wtf.file import FileField, FileRequired, FileAllowed, MultipleFileField
from wtforms.validators import DataRequired, URL, Email, Length
from flask_ckeditor import CKEditor,CKEditorField
from datetime import date
import random
import time
import base64


app = Flask(__name__)
app.secret_key = 'dsgzdfshdfhdgxhghdfhdf'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ckeditor = CKEditor(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dukan.db"
db = SQLAlchemy()
db.init_app(app)
app.config["TEMPLATES_AUTO_RELOAD"] = True
login_manager = LoginManager()
login_manager.init_app(app)

gravatar = Gravatar(app,
                    size=80,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Details, user_id)

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")    

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(),Email(message="incorrect email")])
    password = PasswordField('password', validators=[DataRequired(), Length(min=7, message="should be greater than 7")])
    submit = SubmitField('Submit')

class Form(FlaskForm):
    product = StringField('product', validators=[DataRequired()])
    price = StringField('price', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    data_file = FileField(validators=[FileRequired(), FileAllowed(['jpg','jpeg'], 'jpg files only')])
    company_logo = FileField(validators=[FileRequired(), FileAllowed(['jpg','jpeg'], 'jpg files only')])
    promotion_video_file = FileField(validators=[FileRequired(), FileAllowed(['mp4','mp3'], 'mp4 and mp3 files only')])
    category =  StringField('category', validators=[DataRequired()])
    url =  StringField('url', validators=[])
    enter = SubmitField('enter')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")

class Details(UserMixin, db.Model):
    __tablename__ = 'manager'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    chips = relationship("Book", back_populates="ate")
    kurkure = relationship("Description", back_populates="eat")
    posts = relationship("BlogPost", back_populates="author")
   
    comments = relationship("Comment", back_populates="comment_author")
       

class Description(db.Model):
    __tablename__ = 'product_imf'
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(250), nullable=False)
    picture = relationship("Book", back_populates="author")
    eat = relationship("Details", back_populates="kurkure")
    eat_id = db.Column(db.Integer, db.ForeignKey("manager.id"))
    url = db.Column(db.String(250), nullable=True)
    option = db.Column(db.String(250), nullable=True)
    blog_child = relationship("BlogPost", back_populates="blog_parent")


class Book(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    my_blob = db.Column(db.LargeBinary, nullable=False)
    product_blob = db.Column(db.LargeBinary, nullable=True)
    video_blob = db.Column(db.LargeBinary, nullable=True)
    author = relationship("Description", back_populates="picture")
    ate = relationship("Details", back_populates="chips") 
    author_id = db.Column(db.Integer, db.ForeignKey("product_imf.id"))
    ate_id = db.Column(db.Integer, db.ForeignKey("manager.id"))

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
   
    author_id = db.Column(db.Integer, db.ForeignKey("manager.id"))
    
    author = relationship("Details", back_populates="posts")
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    blog_parent = relationship("Description", back_populates="blog_child")
    comments = relationship("Comment", back_populates="parent_post")
    source_id = db.Column(db.Integer, db.ForeignKey("product_imf.id"))


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
  
    author_id = db.Column(db.Integer, db.ForeignKey("manager.id"))
    comment_author = relationship("Details", back_populates="comments")
   
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")    



class Follow(db.Model):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(
        db.Integer,nullable=False)
 
    following_to = db.Column(
        db.Integer,nullable=False)

with app.app_context():
    db.create_all()    


@app.route('/button',  methods=['GET', 'POST'])
def button():
    return render_template("button.html")


@app.route('/forgot_password',  methods=['GET', 'POST'])
def forgot_password():
    if request.method == "GET":
    
        session['start_time'] = time.time()
        session['otpe'] = random.randint(0,100)

    if request.method == "POST":
        start_time = session.get('start_time')
        new_time = int(time.time()) - int(start_time)  # Calculate the time difference in seconds     
        if request.form.get('enter') == 'enter':
            if new_time >= 10:
                flash("Time limit exceeded.")
                return redirect(url_for('forgot_password'))
            elif int(request.form['otp']) == session.get('otpe'):
                    return redirect(url_for('bhoot'))
            else:
               flash('wrong password')
               return redirect(url_for('forgot_password'))

        if  request.form.get('enter') == 'resend':
            
            return redirect(url_for('forgot_password'))
    return render_template('otp.html', generate_number=session.get('otpe'))        


@app.route('/my_listed', methods=['GET', 'POST'])
def home():
    result = db.session.execute(db.select(Description).order_by(Description.id)).scalars()
    all_images = db.session.execute(db.select(Book).order_by(Book.id)).scalars()
    change = {}
    for i in result:
        change[i.id] = []
    for j in all_images:
        corrected_blob = base64.b64encode(j.my_blob).decode('utf-8')
        change[j.author.id].append(corrected_blob)
    all_books =  db.session.execute(db.select(Description).order_by(Description.id)).scalars()
    return render_template("admin.html", all_books=all_books, check=current_user, change=change)

@app.route('/', methods=['GET', 'POST'])
def registration():
    regs = MyForm()
    if regs.validate_on_submit():

        meow = regs.email.data
        book = db.session.execute(db.select(Details).where(Details.email == meow)).scalar()
        
        if book:
            flash("Email already exists. Please log in.")
            return redirect(url_for('login'))

        new_password = generate_password_hash(regs.password.data, method='pbkdf2:sha256:260000', salt_length=16)
        
        new_book = Details(
            name=regs.name.data,
            email=regs.email.data,
            password=new_password,
            followers=0
        )
        db.session.add(new_book)
        db.session.commit()

        login_user(new_book)

        flash("Registration successful!")
        return redirect(url_for('button'))

    return render_template("Regs.html", regs=regs)


@app.route('/profile/<index>',  methods=['GET', 'POST'])
def profile(index):
   
   if request.method == "POST":
        
        follow_record = db.session.execute(
        db.select(Follow).where(
        Follow.follower_id == current_user.id,
        Follow.following_to == index
        )).scalar()
        if(follow_record == None): 
            follow = Follow(follower_id=current_user.id, following_to=index)
            db.session.add(follow)
            db.session.commit()

            followed_user = db.session.execute(
                db.select(Details).where(Details.id == index)
            ).scalar_one_or_none()

            if followed_user is not None:
                followed_user.followers = (followed_user.followers or 0) + 1
                db.session.commit()

   if request.method == "GET":
      
      result1 = db.session.execute(db.select(Description).order_by(Description.id)).scalars()
      all_images = db.session.execute(db.select(Book).order_by(Book.id)).scalars()
      listing = {}
      imp_list = []
      for i in result1:
        listing[i.id] = []
      for j in all_images:
        corrected_blob = base64.b64encode(j.my_blob).decode('utf-8')
        listing[j.author.id].append(corrected_blob)
      all_books = db.session.execute(db.select(Description).order_by(Description.id)).scalars()
      imp_list = [book.category for book in all_books]
      unique_category = list(set(imp_list))
      new_list = []
      for unique in unique_category:
        book_to_update = db.session.execute(db.select(Description).where(Description.category == unique )).scalars()
        new_list.append(book_to_update)    
      result= db.get_or_404(Details, index)
      followed_user = db.session.execute(
                db.select(Details).where(Details.id == index)
            ).scalar_one_or_none()
      size = followed_user.followers
      follow_record = db.session.execute(
        db.select(Follow).where(
        Follow.follower_id == current_user.id,
        Follow.following_to == index
        )).scalar()
      return render_template('profile.html', result=result, all_books=all_books, listing=listing, golang=new_list, current_user=current_user, size=size, thakan=follow_record)
    
@app.route('/unfollow/<index>',  methods=['GET', 'POST'])
def check(index):
    follow_record = db.session.execute(
        db.select(Follow).where(
        Follow.follower_id == current_user.id,
        Follow.following_to == index
        )).scalar()
    db.session.delete(follow_record) 
    db.session.commit()
    followed_user = db.session.execute(db.select(Details).where(Details.id == index)).scalar()

    if followed_user is not None:
            followed_user.followers = (followed_user.followers or 0) - 1
            db.session.commit()

@app.route('/login',  methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        password = loginform.password.data
        result = db.session.execute(db.select(Details).where(Details.email == loginform.email.data))
        
        user = result.scalar()
      
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
     
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('button'))
        
        
    return render_template("login.html", loginform=loginform, current_user=current_user)
    
@login_required
@app.route('/product_registration',  methods=['GET', 'POST'])
def product_registration():
    series =  Form()
    if series.validate_on_submit():

      list = Description(product=series.product.data, price=series.price.data, description=series.description.data, eat_id=current_user.id, category=series.category.data, url=series.url.data)
      db.session.add(list)
      db.session.commit()
      
      meow = series.data_file.data
      company = series.company_logo.data    
      promotion = series.promotion_video_file.data    
      list2 = Book(my_blob=meow.read(), author_id=list.id, ate_id=current_user.id, product_blob=company.read(), video_blob=promotion.read())
      db.session.add(list2)
          
      db.session.commit()
      
          
      return redirect(url_for('home'))

      
    return render_template("pregs.html", series=series)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/promotional_site/<index>',  methods=['GET', 'POST'])
def promotional(index):
  if "-" in index:  
    text = index
    numbers = text.split('-')
    first_number = int(numbers[0])
    second_number = int(numbers[1]) 
    all_images = db.session.execute(db.select(Book).order_by(Book.id)).scalars()
    list=[]
    for images in all_images:
      if first_number <= images.ate.followers <= second_number:
        list_dic = {}
        encoded_img_data = base64.b64encode(images.product_blob).decode('utf-8')
        base64_video_data = base64.b64encode(images.video_blob).decode('utf-8')
        list_dic["pics"] = encoded_img_data
        list_dic["video"] = base64_video_data
        list_dic["id"] = images.ate.id
        list.append(list_dic)
    return render_template("video.html", list=list)
  else:
    all_images = db.session.execute(db.select(Book).order_by(Book.id)).scalars()
    list=[]
    for images in all_images:
      if images.ate.followers >= index:
        list_dic = {}
        encoded_img_data = base64.b64encode(images.product_blob).decode('utf-8')
        base64_video_data = base64.b64encode(images.video_blob).decode('utf-8')
        list_dic["pics"] = encoded_img_data
        list_dic["video"] = base64_video_data
        list_dic["id"] = images.ate.id
        list.append(list_dic)
    return render_template("video.html", list=list)    


@app.route('/delete/<index>',  methods=['GET', 'POST'])
def delete(index):
    # Retrieve the description to delete
    # have to make it delete the blog post
    book_to_delete = db.get_or_404(Description, index)

    media_to_delete = db.session.execute(
        db.select(Book).where(Book.author_id == book_to_delete.id)
    ).scalars().all()

    db.session.delete(book_to_delete)

    for media in media_to_delete:
        db.session.delete(media)

    db.session.commit()

    return redirect(url_for('button'))

@app.route('/blog/<index>', methods=['GET', 'POST'])
def blog(index):
    requested_product = db.get_or_404(Description, index)
    blog_record = db.session.execute(
        db.select(BlogPost).where(
        BlogPost.source_id == current_user.id
        )).scalar()
    if current_user.id == requested_product.eat.id:
        if blog_record == None:
            form = CreatePostForm()
            if form.validate_on_submit():
                new_post = BlogPost(
                    title=form.title.data,
                    source_id = index,
                    subtitle=form.subtitle.data,
                    body=form.body.data,
                    img_url=form.img_url.data,
                    author=current_user,
                    date=date.today().strftime("%B %d, %Y")
                )
                db.session.add(new_post)
                db.session.commit()
                return redirect(url_for("button"))
            return render_template("make-post.html", form=form, current_user=current_user)
    if blog_record != None:
        requested_post = db.get_or_404(BlogPost, blog_record.id)
        comment_form = CommentForm()
   
        if comment_form.validate_on_submit():
            if not current_user.is_authenticated:
                flash("You need to login or register to comment.")
                return redirect(url_for("login"))
            new_comment = Comment(
                text=comment_form.comment_text.data,
                comment_author=current_user,
                parent_post=requested_post
                )
            db.session.add(new_comment)
            db.session.commit()    
        return render_template("post.html", post=requested_post, current_user=current_user, form=comment_form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get("search")
    source = db.session.execute(db.select(Description).where(Description.url == query )).scalars()
    return render_template("product.html", source=source)

             
# Create an admin-only decorator
# def admin_only(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         If id is not 1 then return abort with 403 error
#         if current_user.id != 1:
#             return abort(403)
#         Otherwise continue with the route function
#         return f(*args, **kwargs)

#     return decorated_function
    

if __name__ == '__main__':
   app.run(debug=True,port=8000)

