#coding=UTF8
'''
Created on 2012-2-5

@author: hh
@license: BSD
'''
import urllib,urllib2 , Cookie, re, os, time
from google.appengine.api import urlfetch
from BeautifulSoup import BeautifulSoup

class URLOpener:
    def __init__(self):
        self.cookie = Cookie.SimpleCookie()
    
    def open(self, url, data=None):
        if data is None:
            method = urlfetch.GET
        else:
            method = urlfetch.POST
    
        while url is not None:
            response = urlfetch.fetch(url=url,
                                      payload=data,
                                      method=method,
                                      headers=self._getHeaders(self.cookie),
                                      allow_truncated=False,
                                      follow_redirects=False,
                                      deadline=25
                                      )
            data = None # Next request will be a get, so no need to send the data again. 
            method = urlfetch.GET
            self.cookie.load(response.headers.get('set-cookie', '')) # Load the cookies from the response
            url = response.headers.get('location')

        return response
        
    def _getHeaders(self, cookie):
        headers = {
                   'User-Agent' : 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.46 Safari/535.11',
                   'Cookie' : self._makeCookieHeader(cookie)
                   }
        return headers

    def _makeCookieHeader(self, cookie):
        cookieHeader = ""
        for value in cookie.values():
            cookieHeader += "%s=%s; " % (value.key, value.value)
        return cookieHeader



def login(usr, pwd):
    'login function'
    opener = URLOpener()
    url_login = 'http://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp'
    body = (('userid', usr),
        ('userpass', pwd),)

    print 'login to get cookies'
    opener.open(url_login, urllib.urlencode(body))
    return opener

class MyCourses:
    '''
    finally there is some OOP feeling
    '''
    def __init__(self, opener, url="http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/MyCourse.jsp?language=cn"):
        self.CSSClass = '^info_tr'
        self.url = url
        self.opener = opener
        self.data = self.opener.open(self.url).content
        self.list = self.GetList()
        self.numolist = self.CountList()
        
    def GetList(self):
        'get a list,or,everything'
        soup = BeautifulSoup(self.data)
        return soup(attrs={'class' : re.compile(self.CSSClass)})
    
    def CountList(self):
        'return how many lines the list have'
        return len(self.list)
    
    def GetLine(self, num):
        '''start from 0 to NumOfList-1
        how to get error?
        just for title and url
        '''
        return self.list[num].a
    
    def GetTitle(self, num):
        return self.GetLine(num).string.strip()
    
    def GetUrl(self, num):
        'start from 0 to NumOfList-1,too'
        return 'http://learn.tsinghua.edu.cn' + self.GetLine(num)['href'] 
    
    def GetCourseId(self, num):
        '''
        nothing to say...
        get "88807" in http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/course_locate.jsp?course_id=88807
        '''
        return self.GetLine(num)['href'].split("course_id=")[1]
    
class ACourse(MyCourses):
    'write for course notices'
    def __init__(self, opener, cid):
        self.CSSClass = '^tr'
        self.cid = cid
        self.url()
        self.opener = opener
        self.data = self.opener.open(self.url).content
        self.list = self.GetList()
        self.numolist = self.CountList()
        self.coursename = self.GetMyCourseName()       
    
    def url(self):
        self.url = 'http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/getnoteid_student.jsp?course_id=' + self.cid
        
    def GetCourseId(self, num):
        'an penguin cannot fly'
        return
    
    def GetDate(self, num):
        x = str(self.list[num])
        return time.strptime(re.findall('\\d\\d\\d\\d-\\d\\d-\\d\\d', x)[0], '%Y-%m-%d')

    def GetUrl(self, num):
        'start from 0 to NumOfList-1,too'
        return 'http://learn.tsinghua.edu.cn/MultiLanguage/public/bbs/' + self.GetLine(num)['href'] 
    
    def GetMyCourseName(self):
        soup2 = BeautifulSoup(self.data)
        nm = soup2.find(attrs={'class' : re.compile('^info_title')}).text.split('&nbsp;')[1]
        return nm
    
class ANotice():
    def __init__(self, opener, url):
        data = opener.open(url).content
        self.soup = BeautifulSoup(data)
    def GetTitle(self):
        return self.soup(attrs={'class' : re.compile('tr_l2')})[0].text
    def GetContent(self):
        return self.soup(attrs={'class' : re.compile('tr_l2')})[1].text.replace('&nbsp;', '\n')
        
class Document(ACourse):
    
    def url(self):
        self.url = 'http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/download.jsp?course_id=' + self.cid
    
    def download(self, num):
        d_url = self.GetUrl(num)
        root_menu = 'tmp'
        try:
            os.makedirs(root_menu + os.sep + self.coursename)
        except:
            pass
        
        d_file = self.opener.open(d_url)
        d_data = d_file.read()        
        d_name = d_file.info()['Content-Disposition'].decode('gbk').encode("UTF-8").split('"')[1]
        
        open(root_menu + os.sep + self.coursename + os.sep + d_name, 'wb').write(d_data)
        return d_name

    
