# -*- coding: utf-8 -*-
import requests
from lxml import etree
from urllib import urlretrieve
import time

class ZhihuLogin(object):

    def __init__(self):
        self.email='yoursemailaddress'
        self.password='yourspassword'
        self.headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36'}

    def Get_captcha(self):
        urlretrieve('http://www.zhihu.com/captcha.gif?r=%d' % (time.time()*1000),'captcha.gif')
        return raw_input('captcha:')

    def login(self):

        requests.packages.urllib3.disable_warnings()
        session=requests.session()

        login_url='https://www.zhihu.com/login/email'

        _xsrf=etree.HTML(requests.get('https://www.zhihu.com/#signin',headers=self.headers,verify=False).text).xpath('/html/body/input/@value')[0]
        data={
            '_xsrf':_xsrf,
            'password':self.password,
            'remember_me':True,
            'email':self.email,
#            'captcha':self.Get_captcha()
        }

        res=session.post(login_url,data=data,headers=self.headers,verify=False)
        
 
        if '\\u767b\\u5f55\\u6210\\u529f' in res.text:
            print "Successfully login in."
            self.headers['Cookie']=res.headers['Set-Cookie']
            return True
        else:
            print "Login in failed."
            return False

    def getName(self):

        if self.login():
            res=requests.get('https://www.zhihu.com/settings/profile',headers=self.headers,verify=False)
            selector=etree.HTML(res.text)
            print str(selector.xpath('//*[@class="top-nav-profile"]/a/@href')[0])
            homepage_url='https://www.zhihu.com'+str(selector.xpath('//*[@class="top-nav-profile"]/a/@href')[0])
            home_selector=etree.HTML(requests.get(homepage_url,headers=self.headers,verify=False).text)
            name=home_selector.xpath('//*[@class="title-section ellipsis"]/span/text()')[0]
            print name.encode('utf-8')



a=ZhihuLogin()
a.getName()
