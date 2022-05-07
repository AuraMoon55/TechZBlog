from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import pytz

auth = Blueprint('auth', __name__)


@auth.route("/admins")
async def admins():
  master_key = request.args.get("key")
  if master_key == "EybUA15T4oFFD67Kegl88N5Ba9C2rRZW9jQOnC0pL30XIv6iMhfEmtYsGHkPfb1SJx2DA3eV7ccBdwqa4zdu":
    pass
  else:
    return jsonify(status="fail", error="MASTER KEY IS WRONG PLEASE ENTER VALID MASTER KEY")
  admins = await get_admins()
  return jsonify(status="success", admins=admins)

@auth.route("/add_admin")
async def add_admi():
  key = request.args.get("user_id")
  name = request.args.get("name")
  sx = await add_admin(key, name)
  return jsonify(status="success", user=sx)

@auth.route("/post")
async def create_post():
  post_title = request.args.get("title")
  post_admin = request.args.get("api_key")
  post_content = request.args.get("content")
  post_img = request.args.get("img_url")
  post_time = str(datetime.datetime.now(pytz.timezone('Asia/Kolkata'))).split(".")[0]
  admeme = await get_admin(post_admin)
  post = {
    "title": post_time,
    "content": post_content,
    "img": post_img,
    "admin": admeme,
    "date": post_time
  }
  post = await add_post(post, post_admin)
  return jsonify(status="success", post_id=post)
