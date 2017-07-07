# -*- coding:utf-8 -*-
import webapp2
import sys
import urllib
import re

# 注册界面
form = """
<head>
    <meta charset="utf-8">
</head>
<div style="display:flex;">
<div style="width:600px;text-align:right;" >
    <form method="post" >
    <h1 style="text-align:center">Signup</h1>

    <br>
    <label>
        <b>Username:</b>
        <input type="text" name="username">
    </label>

    <br>
    <label>
        <b>Password:</b>
        <input type="password" name="password">
    </label>

    <br>
    <label>
        <b>Verify Password:</b>
        <input type="password" name="verify_password">

    </label>

    <br>
    <label>
        <b>Email(optional):</b>
        <input type="text" name="email">
    </label>

    <br>
    <input type="submit" style="text-align:center">
</form>
</div>

<div style="width:50%">
    <div></div>
</div>

</div>
"""

# 欢迎界面
welcome_form = """
<head>
    <meta charset="utf-8">
</head>
<form method="post">
    <b>欢迎,%(name)s</b>
</form>
"""
USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")  # \S 非空白字符


class MainPage(webapp2.RequestHandler):
    """docstring for MainPage"""
    def valid_username(self,username):
        return USERNAME_RE.match(username)
    def valid_password(self,password):
        return PASSWORD_RE.match(password)
    def valid_email(self,email):
        return EMAIL_RE.match(email)

    def get(self):
        self.response.out.write(form)

    def post(self):
        if sys.getdefaultencoding() != 'utf-8':
            reload(sys)
            sys.setdefaultencoding('utf-8')
        print sys.getdefaultencoding()
        print welcome_form

        # 用户名检查
        username = self.request.get('username')
        user_match = self.valid_username(username)
        if not user_match:
            print "username error"
        else:
            print "匹配:"+user_match.group(0)

        # 密码检查
        password = self.request.get('password')
        password_match = self.valid_password(password)
        if not password_match:
            print "password error"
        else:
            print "匹配:"+password_match.group(0)

        # 确认密码检查
        verify_password = self.request.get('verify_password')
        verify_password_match = self.valid_password(password)
        if not verify_password_match or verify_password!=password:
            print "verify_password error"
        else:
            print "匹配:"+password_match.group(0)

        # 邮箱检查
        email = self.request.get('email')
        email_match = self.valid_email(email)
        if not email_match:
            print "email error"
        else:
            print "匹配:"+email_match.group(0)

        print username,password,verify_password,email
        # print  urllib.quote(username.decode(sys.stdin.encoding).encode('utf8'))



        reurl = '/welcome?username=' + urllib.quote(username.decode('utf8').encode('utf8'))     #以utf8编码并以utf8解码
        self.redirect(reurl)        # 在webapp2.RequestHandler中的类中的方法

class Welcome(webapp2.RequestHandler):
    def get(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        username = self.request.get("username")

        self.response.out.write(welcome_form %{"name":username})

app = webapp2.WSGIApplication([('/',MainPage),('/welcome',Welcome)],debug=True)

