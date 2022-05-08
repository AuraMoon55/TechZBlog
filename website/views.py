from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from . import db, mail
import json
import math


views = Blueprint('views', __name__)

@views.route('/')
async def home():
  posts = await get_posts()
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
  return render_template('home.html', posts=posts, prev=prev, next=next)




@views.route('/contact', methods=['GET','POST'])
async def contact():
  if request.method == 'POST':
    name = request.form.get('name')
    email = request.form.get('email')
    mess = request.form.get('message')
    mail.send_message(
      'New message from ' + name,
      sender=email,
      recipients = ["hentaivillains55@gmail.com"],
      body = mess
    )
  return render_template('contact.html')



@views.route('/post/<post_id>')
async def post(post_id):
  post = await get_post(post_id)
  return render_template('post.html', post=post)
