import pymongo
import smtplib
import datetime

url="<MongoDB url>"
client=pymongo.MongoClient(url)
db=client['birthdaywisher']
birthdays=db['birthdays']
sender=db['emailidpwd']
sender_email = sender.find()[0]['emailid']
sender_password=sender.find()[0]['password']
    
while True:
    current_date=datetime.date.today()
    current_time=datetime.datetime.now().time()
    bdays=birthdays.find()
    for row in bdays:
        username=row['username']
        name=row['name']
        receiver_email=row['receiver_email']
        date=row['date']
        time=row['time']
        message=row['message']
        message+='\n-- With regards '+name+'\n-- This message is sent by '+username+' using birthday wisher.'
        year,month,date=map(int,date.split('-'))
        hour,minute=map(int,time.split(':'))

        if current_date.day==date and current_date.month==month and current_date.year==year and current_time.hour==hour and current_time.minute==minute and row['sent']:
            mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
            mailServer.starttls() 
            mailServer.login(sender_email , sender_password)
            mailServer.sendmail(sender_email, receiver_email , message)
            mailServer.quit()
            birthdays.update_one({'bdayno':row['bdayno'],'username':username },{'$set':{'sent':0}})