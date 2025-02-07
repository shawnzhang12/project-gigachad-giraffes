import os
from peewee import *
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv
from flask_mail import Message, Mail
import datetime
from playhouse.shortcuts import model_to_dict


load_dotenv()

app = Flask(__name__, static_folder='static')

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"), user=os.getenv("MYSQL_USER"), password=os.getenv("MYSQL_PASSWORD"), host=os.getenv("MYSQL_HOST"), port=3306)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])


userinfo = {'name': 'Alan Turing',
    'shortIntro': 'Aspiring Skynet Developer and Professional Programmer',
    'longIntro': 'Alan Turing is from Kansas City, Missouri. He obtained his PhD at Yale. He currently works as a Software Developer. He is a driven individual who plans to one day work as a for his dream company: "Epic Games", and work on his favorite game, "Fortnite". Alan Turing is from Kansas City, Missouri. He obtained his PhD at Yale. He currently works as a Software Developer. He is a driven individual who plans to one day work as a for his dream company: "Epic Games", and work on his favorite game, "Fortnite"',
    'work': [{'jobTitle': 'Software Engineer @ MLH', 'desc': "I created the backend of the LMS", "year": "1999", 'link':'./static/img/logo.jpg'},
        {'jobTitle': 'Software Engineer @ Meta', 'desc': "I created facebook mobile application", "year": "2004-2022", 'link':'./static/img/logo.jpg'}],
    'skills': ['./static/img/skillicons/c-.png','./static/img/skillicons/css-3.png', './static/img/skillicons/html-5.png',
    './static/img/skillicons/js.png','./static/img/skillicons/python.png'],
    'education': [{'type': 'PhD of Computer Science', 'from': 'Columbia University', 'when': '1984-1989', 'desc': 'I studied stuff', 'link': './static/img/logo.jpg'}],
    'email': '123fakemail@gmail.com',
    'hobbies':  [{'name': 'Basketball', 'caption': 'My Favorite Sport!', 'img': './static/img/hobbies_gallery/basketball.jpeg', 'active': 'active'},
     {'name': 'Fishing', 'caption': 'My favorite way to relax!', 'img': './static/img/hobbies_gallery/fishing.jpg', 'active': ''}, 
    {'name': 'Paddleboarding', 'caption': 'My favorite watersport!', 'img': './static/img/hobbies_gallery/paddleboarding.jpg', 'active': ''}],
    'project_rows': [[{'name': 'Mario', 'tag': 'Loving Recreation of Mario', 'tools': 'Unity, C#', 'link': 'github.com', 'img': './static/img/logo.jpg'},
    {'name': 'Mario', 'tag': 'Loving Recreation of Mario', 'tools': 'Unity, C#', 'link': 'github.com', 'img': './static/img/logo.jpg'},
    {'name': 'Mario', 'tag': 'Loving Recreation of Mario', 'tools': 'Unity, C#', 'link': 'github.com', 'img': './static/img/logo.jpg'}
    ],[{'name': 'Mario', 'tag': 'Loving Recreation of Mario', 'tools': 'Unity, C#', 'link': 'github.com', 'img': './static/img/logo.jpg'},
    {'name': 'Mario', 'tag': 'Loving Recreation of Mario', 'tools': 'Unity, C#', 'link': 'github.com', 'img': './static/img/logo.jpg'},
    {'name': 'Mario', 'tag': 'Loving Recreation of Mario', 'tools': 'Unity, C#', 'link': 'github.com', 'img': './static/img/logo.jpg'}
    ]],
    'facebook': 'facebook.com',
    'github': 'github.com',
    'instagram': 'instagram.com',
    'linkedin':'linkedin.com' ,
    'twitter':'twitter.com'
 }


@app.route('/')
def index():
    return render_template('index.html', title='MLH Fellow', url=os.getenv('URL'), name=userinfo['name'],
    shortIntro=userinfo['shortIntro'], longIntro = userinfo['longIntro'], work = userinfo['work'], skills = userinfo['skills'],
    education = userinfo['education'], email=userinfo['email'], facebook = userinfo['facebook'], instagram = userinfo['instagram'],
    github=userinfo['github'], linkedin=userinfo['linkedin'], twitter = userinfo['twitter'], profilepic='./static/img/profile.jpg')

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', 
    title="Hobbies", 
    url=os.getenv("URL"),
    hobbies = userinfo["hobbies"],
    email=userinfo['email'], 
    facebook = userinfo['facebook'], 
    instagram = userinfo['instagram'],
    github=userinfo['github'], 
    linkedin=userinfo['linkedin'], 
    twitter = userinfo['twitter']
    )

@app.route('/projects')
def projects():
    return render_template('projects.html', 
    title="Projects", 
    url=os.getenv("URL"),
    project_rows = userinfo['project_rows'],
    email=userinfo['email'], 
    facebook = userinfo['facebook'], 
    instagram = userinfo['instagram'],
    github=userinfo['github'], 
    linkedin=userinfo['linkedin'], 
    twitter = userinfo['twitter']
    )

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
            'timeline_posts': [
                model_to_dict(p)
                for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
                ]
            }
@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline", posts = get_time_line_post())


