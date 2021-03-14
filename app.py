from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import datetime
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/blog"
mongo = PyMongo(app)

@app.route('/')
def index():
    #Show all the blog posts in a timeline
    all_posts = []
    for post in mongo.db.posts.find():
        all_posts.insert(0, post)
    print(all_posts)
    return render_template('home.html', result=all_posts)

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    #Add logic to create post
    if request.method == 'GET':
        return render_template('admin.html')
    username = request.form['username']
    password = request.form['password']

    if username == 'krshubham' and password == 'shubham':
        return render_template('create_post.html')
    else:
        return 'Wrong login credentials'

@app.route('/create_post', methods=['POST'])
def createPost():
    title = request.form['blog-title']
    content = request.form['blog-content']
    current_date = datetime.date.today().strftime("%d/%m/%Y")
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    data = {'title': title, 'content': content, 'date': current_date, 'time': current_time}
    mongo.db.posts.insert_one(data)
    return redirect('/')


app.run(host='0.0.0.0', port=8081)