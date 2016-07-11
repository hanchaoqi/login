# -*- coding: utf-8 -*-
import re
import rsa
import json
import urllib
import urllib2
import base64
import cookielib
import binascii

class LoginWeibo(object):
    def __init__(self,username,password):
        self.username = username 
        self.password = password
        self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

    def login(self):
        self.enableCookie()
        login_args = self.getPreLoginArgs()
        post_data = self.getPostData(login_args)
        try: 
            #login 1
            login_url1 = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
            req = urllib2.Request(login_url1,post_data,self.headers)
            res = urllib2.urlopen(req)
            htm = res.read()
            #login 2
            login_url2 = re.search('replace\([\'"](.*?)[\'"]\);',htm).group(1)
            res = urllib2.urlopen(login_url2)
            htm = res.read()
            #login 3
            login_url3 = 'http://weibo.com/' + re.search('userdomain":"(.*)"',htm).group(1)
            res = urllib2.urlopen(login_url3)
        except:
            print "Login Error!"
            return

        print "Login Success!" 
        #shua~weibo
        url = 'http://account.weibo.com/set/index?topnav=1&wvr=6'
        res = urllib2.urlopen(url)
        htm = res.read()
        nick_name = re.search('nick\':\'(.*)\',',htm).group(1)
        print nick_name

    def enableCookie(self):
        cookiejar = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cookiejar)
        opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
        urllib2.install_opener(opener)

    def getPreLoginArgs(self):
	prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)&_=1468032103227'        
        res_data = urllib2.urlopen(prelogin_url).read()
        server_data_json = re.search('\((.*)\)',res_data).group(1)
        server_data = json.loads(server_data_json)
        return server_data

    def getCryptedUserName(self):
        urlencode_username = urllib.quote(self.username)
        data = base64.b64encode(urlencode_username)
        return data

    def getCryptedPassWord(self,serverTime,nonce,pubkey):
        raw_password = str(serverTime) + '\t' + str(nonce) + '\n' + str(self.password)
        pubkey = int(pubkey,16)
        key = rsa.PublicKey(pubkey,int("10001",16))
        encrypted_password = rsa.encrypt(raw_password,key)
        password_hex = binascii.b2a_hex(encrypted_password)
        return password_hex
  
    def getPostData(self,serverData):
        servertime = serverData['servertime']
        nonce = serverData['nonce']
        pubkey = serverData['pubkey']
        rsakv = serverData['rsakv']
        encrypted_username = self.getCryptedUserName()
        encrypted_password = self.getCryptedPassWord(servertime,nonce,pubkey)
        post_data = {
            'entry':'weibo',
            'from':'',
            'gateway':'1',
            'savestate':'7',
            'useticket':'1',
            'ssosimplelogin':'1',
            'pagerefer':'',
            'vsnf':'1',
            'vsnval':'',
            'su':str(encrypted_username),
            'service':'miniblog',
            'servertime':servertime,
            'nonce':nonce,
            'pwencode':'rsa2',
            'rsakv':rsakv,
            'sp':encrypted_password,
            'sr':'1920*1080',
            'encoding':'UTF-8',
            'cdult':'2',
            'domain':'weibo.com',
            'prelt':'140',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype':'META'
        }
        post_data = urllib.urlencode(post_data)
        return post_data

if __name__ == '__main__':
    username = "username"
    password = "password"
    
    lw = LoginWeibo(username,password)
    lw.login()
