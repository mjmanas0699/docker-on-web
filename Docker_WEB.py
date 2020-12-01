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
    docker='ssh 192.168.43.40 docker run -itd --name '+name+' -p ' +port+ ':4200 docker_on_flask'
    #cmd="ssh 192.168.43.40 netstat -tunlep | grep LISTEN | awk '{print $4}'"
    p=subprocess.Popen(docker,stdout=subprocess.PIPE,shell=False,universal_newlines=True)
    stdout,stderr=p.communicate()
    # lst=[]
    # for num in stdout.split('\n'):
    #     for n in num.split(':'):
    #         if n!='':
    #             lst.append(n)
    # if port not in lst:
    return render_template('container.html',form=form,port=port)
if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/run',methods=['GET','POST'])
# def command():
#     form=Command()
#     if form.validate_on_submit():
#         cmd=form.command.data
#         cmd= 'ssh 192.168.43.40'+' '+cmd
#         cmd=cmd.split()
#         process = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True,universal_newlines=True)
#         stdout,stderr=process.communicate()
#         return render_template('cmmand.html',form=form,stdout=stdout)
#     return render_template('cmmand.html',form=form)
# @app.route('/list',methods=['GET','POST'])
# def data_list():
#     all_records=DB.query.all()
#     db.session.commit()
#     return render_template('list.html',all_records=all_records)

# # @app.route('/drop',methods=['GET','POST'])
# # def drop():
# #     db.drop_all()
# #     db.create_all()
# #     return render_template('list.html')   

    ##############   
    #VIEW FUNCTION
    ##############
# @app.route('/')
# def index():
#     return render_template('home.html')

# @app.route('/add',methods=['GET','POST'])
# def add_pup():
#     form=Addform()
#     if form.validate_on_submit():
#         name=form.name.data
#         new_pup=Puppy(name)
#         db.session.add(new_pup)
#         db.session.commit()
#         return redirect(url_for('list_pup'))
#     return render_template('add.html',form=form)
# @app.route('/list')
# def list_pup():
#     puppies=Puppy.query.all()
#     return render_template('list.html',puppies=puppies)

# @app.route('/delete',methods=['GET','POST'])
# def del_pup():
#     form=Delform()
#     if form.validate_on_submit():
#         id = form.id.data
#         pup= Puppy.query.get(id)
#         db.session.delete(pup)
#         db.session.commit()
#         return redirect(url_for('list_pup'))
#     return render_template('delete.html',form=form)

# if __name__ == '__main__':
#     app.run(debug=True)



kubeadm join 172.31.0.135:6443 --token dv6mpx.y0948nqx5iaz5dwn \
    --discovery-token-ca-cert-hash sha256:cd92aca60229875763a8ceb9eafd5ef5b64b412607337e2a49e9e11d3af7a888