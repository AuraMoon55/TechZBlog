from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, Contact
from . import db, mail
import json
import math


views = Blueprint('views', __name__)

@views.route('/')
def home():
  posts = Post.query.filter_by().all()
  last = math.ceil(len(posts)/5)
  page = request.args.get('page')
  if(not str(page).isnumeric()):
    page = 1
  page= int(page)
  posts = posts[(page-1)*int(5): (page-1)*int(5)+ int(5)]
  #Pagination Logic
  #First
  if (page==1):
    prev = "#"
    next = "/?page="+ str(page+1)
  elif(page==last):
    prev = "/?page=" + str(page - 1)
    next = "#"
  else:
    prev = "/?page=" + str(page - 1)
    next = "/?page=" + str(page + 1)

  return render_template('home.html', posts=posts, prev=prev, next=next, user=current_user)

@views.route('/delete-post', methods=['POST'])
def delete_note():
    post = json.loads(request.data)
    postId = post['postId']
    post = Post.query.get(postId)
    if post:
        if post.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit()

    return jsonify({})


@views.route('/contact', methods=['GET','POST'])
def contact():
  if request.method == 'POST':
    name = request.form.get('name')
    email = request.form.get('email')
    mess = request.form.get('message')
    entry = Contact(name=name, email=email, message=mess[:150])
    db.session.add(entry)
    db.session.commit()
    mail.send_message(
      'New message from ' + name,
      sender=email,
      recipients = ["hentaivillains55@gmail.com"],
      body = message
    )
  return render_template('contact.html', user=current_user)

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
  if request.method == 'POST':
    post_title = request.form.get('post-title')
    post_content = request.form.get('post-content')
    post_bg = request.form.get('post-bg')
    
    if len(post_title) < 1:
      flash('Title For Post Is Too Short!', category='error')
    elif len(post_content) < 1:
      flash('Content For Post Is Too Short!', category='error')
    elif len(post_bg) < 1:
      post_bg = "h.png"
    else:
      new_post = Post(title=post_title, content=post_content, user_id=current_user.id, user_name=current_user.first_name, img_file=post_bg)
      db.session.add(new_post)
      db.session.commit()
      flash('Post Added Successfully!', category='success')
      
  return render_template('dashboard.html', user=current_user)

@views.route('/post/<post_id>')
def post(post_id):
  post = Post.query.filter_by(id=post_id).first()
  return render_template('post.html', post=post, user=current_user)
