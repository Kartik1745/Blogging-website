from logging import log
from os import abort
from packages.models import User,Post
from flask import render_template,redirect,flash,url_for,request,abort
from packages.forms import RegistrationForm,LoginForm,NewPost
from packages import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required

db.create_all()


@app.route("/")
@app.route("/home")
def home():
    posts=Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hash_pass=bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
        us=User(username=form.Username.data,email=form.Email.data,password=hash_pass)
        db.session.add(us)
        db.session.commit()
        flash(f'Account Created for {form.Username.data}!','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='register',form=form)



@app.route("/Login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.Email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.Password.data):
            login_user(user,remember=form.Remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:    
            flash('Login Unsuccessful. Please check Email and password', 'danger')
    return render_template('Login.html',title='Login',form=form)


@app.route("/Logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def user_account():
    return render_template('account.html',title='Account')

@app.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form=NewPost()
    if form.validate_on_submit():
            post=Post(title=form.title.data,content=form.content.data,author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created','success')
            return redirect(url_for('home'))
    return render_template('create_post.html',title='New Post',form=form,legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404 (post_id)
    return render_template('post.html',title='post.title',post=post)

@app.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404 (post_id)
    if post.author != current_user:
        abort(403)
    form=NewPost()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method =='GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template('create_post.html',title='Update Post',form=form,legend='Update')    

@app.route("/post/<int:post_id>/delete",methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404 (post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit() 
    flash('Your post has been deleted!','success') 
    return redirect(url_for('home')) 

