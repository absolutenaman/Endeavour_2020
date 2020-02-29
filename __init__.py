from flask import Flask,render_template,request,redirect,url_for,flash,session,send_file
import runp
from passlib.hash import sha256_crypt
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_mail import Mail,Message
import random
import string
from labsql import *
from functools import wraps

app=Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='example@gmail.com'
app.config['MAIL_PASSWORD']='*********'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:mom0511@localhost/groot"
app.config["SQLALCHEMY_BINDS"]={
									"Teachers":"mysql+pymysql://root:mom0511@localhost/teachers",
									"Students":"mysql+pymysql://root:mom0511@localhost/students"
								}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
db.app=app
#db.create_all()
db1.init_app(app)
db1.app=app
db2.init_app(app)
db2.app=app

migrate=Migrate(app,db2)
manager=Manager(app)

manager.add_command('db',Migrate)
c=False
def pass_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route("/")
def home():
    return render_template("home.html")


# rupam's code

list1=[]
list2=[]
with open('file.txt','r') as f:
    f_contents = f.readlines()
    for i in range(3,len(f_contents)-1,1):
        list1.append(f_contents[i])    
    hackerrank_discription=f_contents[-1]

with open('file_codeforces.txt','r') as f1:
    f1_contents = f1.readlines()
    status=f1_contents[0]
    for i in range(1,3,1):
        list2.append(f1_contents[i])    
    codeforces_contri=f1_contents[-1]

with open('file_hackerearth.txt','r') as f2:
    f2_contents = f2.readlines()
    hackerearth=f2_contents


@app.route('/user/Student/student_dashboard',methods=["GET","POST"])
def student_dashboard():
	client=session['username']
	user=StudentDetails.query.filter_by(username=client).all()[0]
	return user.codeforces
    # return render_template('student_dashboard.html',hackerrank_discription=hackerrank_discription,list1=list1,hackerearth=hackerearth,list2=list2,status=status,hack_rank=user.hacker_rank,hack_codeforces=user.codeforces,hacker_earth=user.hacker_earth)


# rupam's code ends here


@app.route("/run",methods=["GET","POST"])
# @login_required
def run(x):
    extention=request.form["ext"]
    name=request.form["filename"]
    code=request.form["code"]
    file_name=name+"."+extention
    f=open(file_name,"w")
    f.write(code)
    f.close()
	# a=Student_files(student_name=client)
    if extention == "java":
        output=runp.run_java(file_name)
        return render_template("output.html",output=output)
    elif extention == "cpp":
        output=runp.run_cpp(file_name)
        return render_template("output.html",output=output)
    elif extention == "c":
        output=runp.run_c(file_name)
        return render_template("output.html",output=output)
    elif extention == "python":
        output=runp.run_python(file_name)
        return render_template("output.html",output=output)
    elif extention == "sql":
        userdb="groot"
        password="mom0511"
        output=runp.run_mysql(code,userdb,password)
        return render_template("output.html",output=output)

@app.route("/login-sign-page")
def login_sign_page():
    return render_template("login.html")

@app.route("/signup-page")
def signup_page():
    return render_template("select.html")

@app.route("/signup-page/Teacher",methods=["GET","POST"])
def signupTeacher():
	if request.method=="POST":
		tecname=request.form["tecname"]
		username=request.form["username"]
		clgname=request.form["clgname"]
		a=TeachersCredentials(username=username,teacher_name=tecname,college_id=clgname)
		db1.session.add(a)
		db1.session.commit()
		return render_template("sign.html")
	else:
		return render_template("sign.html")

@app.route("/signup-page/Student",methods=["GET","POST"])
def signupStudent():
	name=request.form["stuname"]
	return render_template("signStu.html")
@app.route("/run-now")
def run_now():
	return render_template("editor.html")
@app.route("/user/<string:type>/<string:path>",methods=["GET","POST"])
def user_log(type,path):
	if session['username']!=None:
		c=True
		client=session['username']
		if type=="Teacher":
			if path=="home":
				user=TeacherDetails.query.filter_by(username=client).all()[0]
				return render_template("teacherdash.html",name=user.teacher_name)
			if path=="createlab":
				return render_template("createlab.html")
			if path=="create-lab":
				name=request.form["name"]
				sec=request.form["sec"]
				sem=request.form["sem"]
				lab=Labs(teacher_id=random.randrange(0,9),subject=random.randrange(0,9),sem=sem,sec=sec,date_created=random.randrange(0,9),lab_url=random.randrange(0,9),ref_no=random.randrange(0,9))
				db.session.add(lab)
				db.session.commit()
				return "Lab Created"
		if type=="Student":
			if path=="home":
				user=StudentDetails.query.filter_by(username=client).all()[0]
				return render_template("studentdash.html",name=user.student_name)
				# return user[0].student_name
				
			if path=="run-page":

				return render_template("editor.html",)

@app.route("/login/<string:type>",methods=["GET","POST"])
def login(type):
    if request.method=="POST":
        uname=request.form["username"]
        passwd=request.form["passwd"]
        if type=="Teacher":
			user=TeachersCredentials.query.filter_by(username=uname).all()
			if len(user)==0:
				flash("No such Teacher Present!!!")
				return redirect(url_for("login_sign_page"))
			if (passwd==user[0].password):
				session['logged_in']=True
				session['username']=uname
				return redirect("/user/Teacher/home")
			else:
				flash("Wrong Credentials")
				return redirect(url_for("login_sign_page"))
        else:
			user=StudentsCredentials.query.filter_by(username=uname).all()
			if len(user)==0:
				flash("No such Student Present!!!")
				return redirect(url_for("login_sign_page"))
			else:
				if(passwd==user[0].password):
					session['logged_in']=True
					session['username']=uname
					return redirect("/user/Student/home")

			# if sha256_crypt.verify(passwd,user[0].password):
			# 	session['logged_in']=True
			# 	session['username']=uname
			# 	return redirect("/user/Student/home")
    else:
        flash("Not Allowed")
        return redirect(url_for("login_sign_page"))


@app.route("/signup/<string:type>",methods=["GET","POST"])
def signup(type):
    if request.method=="POST":
        if type=="Teacher":
			clgname=request.form["clgname"]
			tecname=request.form["tecname"]
			uname=request.form["username"]
			passwd=random.randrange(0,9)
			# msg=Message('FROM Onlinelabs',sender='in.hodophile@gmail.com',recipients=[uname])
			# msg.body="your password for first login is "+str(passwd)
			# mail.send(msg)
			# passwd=sha256_crypt.encrypt(passwd)
			insert_techer_cred=TeachersCredentials(username=uname,password=passwd)
			db.session.add(insert_techer_cred)
			db.session.commit()
			user=TeachersCredentials.query.filter_by(username=uname).all()[0]
			insert_techer_detail=TeacherDetails(teacher_id=user.teacher_id,username=user.username,teacher_name=tecname,college_id=clgname.split("-")[-1])
			db1.session.add(insert_techer_detail)
			db1.session.commit()
			flash("Password for first login sent to your mail!!!")
			return redirect(url_for("login_sign_page"))
        if type=="Student":
			clgname=request.form["clgname"]
			stuname=request.form["stuname"]
			uname=request.form["username"]
			course=request.form["course"]
			sem=request.form["sem"]
			section=request.form["sec"]
			rollno=request.form["roll"]
			branch=request.form["branch"]
			passwd=random.randrange(0,9)
			msg=Message('FROM Onlinelabs',sender='in.hodophile@gmail.com',recipients=[uname])
			msg.body="your password for first login is "+passwd
			mail.send(msg)
			passwd=sha256_crypt.encrypt(passwd)
			insert_stu_cred=StudentsCredentials(username=uname,password=passwd)
			db.session.add(insert_stu_cred)
			db.session.commit()
			user=StudentsCredentials().query.all()[0]
			insert_stu_detail=StudentDetails(student_id=user.student_id,username=user.username,student_name=stuname,college_id=clgname.split("-")[-1],course=course,sem=sem,sec=section,rollno=rollno)
			db2.session.add(insert_stu_detail)
			db2.session.commit()
			flash("Password for first login sent to your mail!!!")
			return redirect(url_for("login_sign_page"))



def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			return redirect(url_for('home'))
	return wrap



@app.route("/logout")
@login_required
def logout():
	try:
		c=False
		client_email=session['username']
		session.pop('username',None)
		return redirect(url_for("main"))
	except:
		flash("ALREADY LOGGED OUT")
		return redirect(url_for("home"))
#teacher Access the file send by student
@app.route("/returnfile/")
def returnfile():
	return send_file("/home/naman/OnlineLabs/hello.py.python")

#student codes
@app.route("/user/Student/my_codes")
def my_codes():
	client=session['username']
	n=Student_files.query.filter_by(student_name=client).all()
	T=Teacher_notify.query.all()
	return render_template("studentcodes.html",n=n)
# @app.route("/user/Student/home")
# def home1():
# 	flash("Your code has been sent")
# 	return render_template("/user/Student/home")


		# if type=="Teacher":
		# 	if path=="home":
		# 		user=TeacherDetails.query.filter_by(username=client).all()[0]
		# 		return render_template("teacherdash.html",name=user.teacher_name)
		# 	if path=="createlab":
		# 		return render_template("createlab.html")
		# 	if path=="create-lab":
		# 		name=request.form["name"]
		# 		sec=request.form["sec"]
		# 		sem=request.form["sem"]
		# 		lab=Labs(teacher_id=random.randrange(0,9),subject=random.randrange(0,9),sem=sem,sec=sec,date_created=random.randrange(0,9),lab_url=random.randrange(0,9),ref_no=random.randrange(0,9))
		# 		db.session.add(lab)
		# 		db.session.commit()
		# 		return "Lab Created"
		# if type=="Student":
		# 	if path=="home":
		# 		user=StudentDetails.query.filter_by(username=client).all()[0]
		# 		return render_template("studentdash.html",name=user.student_name)
		# 		# return user[0].student_name
				
			# if path=="run-page":
			# 	return render_template("editor.html")


app.secret_key = "this is nothing but a secret key"
if __name__ == '__main__':
    app.run(debug="true",port=5000 )
