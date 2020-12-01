from flask import Flask, render_template,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from forms import Form,Container
import subprocess
import random
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY']='hello'
#####################
#SQL DATABASE SECTION
#####################
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///relation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)
Migrate(app,db)

class DB(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text)
    email=db.Column(db.Text)
    mobile=db.Column(db.Integer)
    def __init__(self,name,email,mobile):
        self.name=name
        self.email=email
        self.mobile=mobile
@app.route('/',methods=['GET','POST'])
def index():
    form=Form()
    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data
        mobile=form.mobile.data
        new_list=DB(name,email,mobile)
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('container_details'))
    return render_template('home.html',form=form)

@app.route('/container_details',methods=['GET','POST'])
def container_details():
    form=Container()
    name=form.name.data
    if form.validate_on_submit():
        return redirect(url_for('container'))
    return render_template('cmmand.html',form=form)

@app.route('/live_container',methods=['GET','POST'])
def container():
    form=Container()
    name='ghfuhjvjhvj'
    port=random.randrange(2000,65535)
    port=str(port)
    docker='docker run -itd --name '+name+' -p ' +port+ ':8888 jupyter/all-spark-notebook'
    #cmd="ssh 192.168.43.40 netstat -tunlep | grep LISTEN | awk '{print $4}'"
    p=subprocess.Popen(docker,stdout=subprocess.PIPE,shell=True,universal_newlines=True)
    stdout,stderr=p.communicate()
    # lst=[]
    # for num in stdout.split('\n'):
    #     for n in num.split(':'):
    #         if n!='':
    #             lst.append(n)
    # if port not in lst:
    return render_template('container.html',form=form,port=port)
if __name__ == '__main__':
    app.run(host='0.0.0.0')
