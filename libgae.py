'''
Created on 2012-2-11

@author: hh
'''
from google.appengine.api import mail
from google.appengine.ext import db

def sendmail(title,receiver,content):
    message = mail.EmailMessage(sender="robot <not-a-real-person@amailformyself.appspotmail.com>",
                                subject = title)
    message.to = receiver
    message.body = content
    message.send()  
    return 

class DBNotices(db.Model):
    urlnotice=db.LinkProperty()
    #notice id that has been updated last
    utime=db.DateTimeProperty(auto_now=True)

def db_update(url):
    notice=DBNotices()
    notice.urlnotice=url
    notice.put()
    return

def db_ifnew(url):
    q=DBNotices.all()
    p=q.filter('urlnotice =', url).count()
    if p==0:
        db_update(url)
        return True
    else:
        return False
    





