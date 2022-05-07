from . import db

postsdb = db.posts
admindb = db.admins


async def get_admins():
  users = adminsdb.find()
  return users

async def check_admin(key):
  x = await admindb.find_one({"key": key})
  if x['name']:
    return True
  else:
    return False

async def get_admin(key):
  x = await admindb.find_one({"key": key})
  if x['name']:
    return x['name']
  else:
    return None

async def add_admin(key, name):
  keyt = int_to_str(key)
  check = await check_admin(keyt)
  while check:
    keyt = int_to_str(key)
    check = await check_admin(keyt)
  key = keyt
  user = await adminsdb.insert_one({'key': key, 'name': name})
  return user
  
def int_to_str(key):
  alpha = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
  key1 = ""
  for key in str(key):
    key = random.choice(alpha)
    key1 += key
  key2 = key1[::-1]
  key3 = key1 + key2
  lim = int(len(key3)/4)
  key = []
  for x in range(lim):
    x = x*4
    key.append(key3[int(x):int(x+4)])
  key = "-".join(key for key in key)
  return key


async def get_posts(lim=None):
  posts = await postsdb.find()
  if lim:
    return posts[:int(lim)]
  else:
    return posts

async def check_post(post: dict):
  post = await postsdb.find_one({"post": post})
  if post:
    return True
  else:
    return False


async def add_post(post: dict, admin_key):
  check = await check_post(post)
  if check:
    return
  else:
    admin = await get_admin(admin_key)
    return await postsdb.insert_one({"post": post, "admin": admin}).insert_id


async def get_post(post_id=None, admin_key=None):
  if post_id:
    post = await postsdb.find_one({"_id": post_id})
    if post:
      return post
    else:
      return None
  else:
    admin = await get_admin(admin_key)
    posts = await postsdb.find({"admin": admin})
    return posts


async def del_post(post_id):
  post = await get_post(post_id)
  if post:
    await postsdb.delete_one({"_id": post_id})
    return True
  else:
    return True
