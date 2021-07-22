from flask import Flask,request,render_template,redirect,session
import pymongo
import smtplib


app=Flask(__name__)
app.secret_key='cloudcomputing'
url="<MongoDB url>"
client=pymongo.MongoClient(url)
db=client['birthdaywisher']
users=db['users']
birthdays=db['birthdays']
sender=db['emailidpwd']



@app.route('/')
def temp():
    return redirect('/login')

@app.route('/login',methods=['GET','POST'])
def login():
    if 'email' in session:
        return redirect('/home')
    else:
        if request.method=='GET':
            return render_template('login.html')
        else:
            email=request.form['email']
            password=request.form['password']
            if users.find({'email':email,'password':password}).count()==0:
                return render_template('login.html',result=0)
            else:
                session['email']=email
                session['username']=users.find_one({'email':email})['username']
                return redirect('/home')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if 'email' in session:
        return redirect('/home')
    else:
        if request.method=='GET':
            return render_template('signup.html')
        else:
            email=request.form['email']
            username=request.form['username']
            password=request.form['password']
        
            if users.find({'email':email}).count():
                return render_template('signup.html',result=2)
            else:
                if users.find({'username':username}).count():
                    return render_template('signup.html',result=3)
                else:
                    try:
                        document={'email':email,'username':username,'password':password}
                        users.insert_one(document)
                        return render_template('signup.html',result=1)
                    except:
                        return render_template('signup.html',result=0)

@app.route('/home')
def home():
    if 'email' in session:
        return render_template('home.html')
    else:
        return redirect('/login')

@app.route('/home/add',methods=['GET','POST'])
def add():
    if 'email' in session:
        if request.method=='GET':
            return render_template('add.html')
        else:
            name=request.form['name']
            receiver_email=request.form['email']
            message=request.form['message']
            date=request.form['date']
            time=request.form['time']
            bdayno=birthdays.find({'username':session['username']}).count()+1
            document={'bdayno':bdayno,'username':session['username'],'name':name,'receiver_email':receiver_email,'message':message,'date':date,'time':time,'sent':1}
            try:
                birthdays.insert_one(document)
                return render_template('add.html',result=1)
            except:
                return render_template('add.html',result=0)
    else:
        return redirect('/login')
            
@app.route('/home/view')
def view():
    if 'email' in session:
        bdays=birthdays.find({'username':session['username']})
        return render_template('view.html',bdays=bdays)
    else:
        return redirect('/login')

@app.route('/home/view/edit/<int:bdayno>',methods=['GET','POST'])
def edit(bdayno):
    if 'email' in session:
        if request.method=='GET':
            if birthdays.find({'bdayno':bdayno,'username':session['username']}).count():
                bday=birthdays.find_one({'bdayno':bdayno,'username':session['username']})
                return render_template('edit.html',bday=bday)
            else:
                return redirect('/home/view')    
        else:
            name=request.form['name']
            receiver_email=request.form['email']
            message=request.form['message']
            date=request.form['date']
            time=request.form['time']
            bday=birthdays.find_one({'bdayno':bdayno,'username':session['username']})
            try:
                birthdays.update_one({'bdayno':bdayno,'username':session['username']},{'$set':{'username':session['username'],'name':name,'receiver_email':receiver_email,'message':message,'date':date,'time':time,'sent':1}})
                return render_template('edit.html',result=1,bday=bday)
            except:
                return render_template('edit.html',result=0,bday=bday)
    else:
        return redirect('/login')

@app.route('/home/view/delete/<int:bdayno>')
def delete(bdayno):
    if 'email' in session:
        if birthdays.find({'bdayno':bdayno,'username':session['username']}).count():
            birthdays.delete_one({'bdayno':bdayno,'username':session['username']})
            bdays=birthdays.find({'username':session['username']})
            c=1
            for row in bdays:
                birthdays.update_one({'bdayno':row['bdayno'],'username':session['username']},{'$set':{'bdayno':c}})
                c+=1
        return redirect('/home/view')
    else:
        return redirect('/login')

@app.route('/forgotpassword',methods=['GET','POST'])
def forgotpassword():
    if request.method=='GET':
        return render_template('forgotpassword.html',result=1)
    else:
        receiver_email=request.form['email']
        if users.find({'email':receiver_email}).count():
            sender_email = sender.find()[0]['emailid']
            sender_password=sender.find()[0]['password']
                
            message='The requested password for your login is '+users.find_one({'email':receiver_email})['password']
            mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
            mailServer.starttls() 
            mailServer.login(sender_email , sender_password)
            mailServer.sendmail(sender_email, receiver_email , message)
            mailServer.quit()
            return render_template('forgotpassword.html',result=2)
        else:
            return render_template('forgotpassword.html',result=3)

@app.route('/logout')
def logout():
    session.pop('email',None)
    session.pop('username',None)   
    return redirect('/login')

app.run(debug=True)