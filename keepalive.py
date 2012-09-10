'''
Created on 2012-2-15

@author: hh
'''
import libgae,libthu

username='username'
password='password'

receiver="HeYeshuang <yeshuanghe@gmail.com>" #your mail address here
def main():

    print("Hello World!")

    opener = libthu.login(username, password)

    mycourses = libthu.MyCourses(opener)

    cids=[]
    for i in range(mycourses.numolist):
        cids.append(mycourses.GetCourseId(i))

    urls=[]
    for cid in cids:
        acourse=libthu.ACourse(opener, cid)
        for i in range(acourse.numolist):
            urls.append(acourse.GetUrl(i))

    for url in urls:
        anotice=libthu.ANotice(opener, url)
        if libgae.db_ifnew(url):
            libgae.sendmail(anotice.GetTitle(), receiver, anotice.GetContent()+'\n'+ url)

    return

if __name__=='__main__':
    main()
