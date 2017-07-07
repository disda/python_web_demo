# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#conding =utf-8
import webapp2
import sys
import os
form="""
<form method="post">
	<input name="wb" type="radio" ">
	<input name="wc" type="radio" ">
	<input name="wd" type="radio" ">
<div>
	what is your birthday?
	<br>
	<label>
		Month
		<input type="text" name="month" value="%(month)s">
	</label>

	<lable>
		Day
		<input type="text" name="day"   value="%(day)s">
	</lable>

	<lable>
		Year
		<input type="text" name="year"  value="%(year)s">
	</lable>

	<div style="color: red">%(error)s</div>
</div>
	<input type="submit" >
</form>
"""
months = ['January',
	   'February',
	   'March',
	   'April',
	   'May',
	   'June',
	   'July',
	   'August',
	   'September',
	   'October',
	   'November',
	   'December']

class MainPage(webapp2.RequestHandler):
	def valid_month(self,month):
		month = month.capitalize()
		if month in months:
			return month

	def valid_day(self,day):
		if day and day.isdigit():
			day = int(day)
			if day >0 and day <=31:
				return day

	def valid_year(self,year):
		if year and year.isdigit():
			year = int(year)
			if year > 1900 and year < 2020:
				return year

	def escape_html(self,s):
		tmp = s
		if '&' in s:
			tmp = tmp.replace('&','&amp;')
		if '>' in s:
			tmp = tmp.replace('>','&gt;')
		if '<' in s:
			tmp = tmp.replace('<','&lt;')
		if '"' in s:
			tmp = tmp.replace('"','&quot;')
		return tmp

	def write_form(self,error="",month="",day="",year=""):
		self.response.out.write(form % {"error":error,
										"month":self.escape_html(month),
										"day":self.escape_html(day),
										"year":self.escape_html(year)})


	def get(self):
		self.write_form()
		#self.response.headers['Content-Type'] = 'text/plain'
		# self.response.out.write(form)

	def post(self):
		#self.response.out.write(self.request.get('month'))
		user_month = self.request.get('month')
		user_day = self.request.get('day')
		user_year = self.request.get('year')

		month = self.valid_month(user_month)
		day = self.valid_day(user_day)
		year = self.valid_year(user_year)

		if not ( month and day and year):
			print form % {"error":"The doesn't look valid to me,friend","month":user_month,"day":user_day,"year":user_year}

			self.write_form("The doesn't look valid to me,friend",user_month,user_day,user_year)
		else:

			# self.response.out.write("\nThanks")
			self.redirect("/thanks")


class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		birthday = ""+"month:"+str(month)+"day:"+str(day)+"user_year:"+str(year);
		self.response.out.write(birthday)
		self.response.out.write("/nThanks! That's a totally valid day!")

rot13_form = """
<form method="post">
	<h1>Enter some text to ROT13:</h1>
	<input  type="text" name="rot13" style="width:250px; height:100px;" value="%(rot)s">
	<input type="submit">
</form>
"""

class Rot13(webapp2.RequestHandler):
	"""docstring for Rot13"""
	def Rot(self,rot):
		tmp =""
		for i in rot:
			if ord(i) >= ord('a') and ord(i) < ord('n'):
				tmp+=chr(ord(i)+13)

			if ord(i) >= ord('A') and ord(i) < ord('N'):
				tmp+=chr(ord(i)+13)

			if ord(i) >= ord('n') and ord(i) <= ord('z'):
				tmp+=chr(ord(i)-13)

			if ord(i) >= ord('A') and ord(i) <= ord('Z'):
				tmp+=chr(ord(i)-13)
		return tmp


	def get(self):
		self.response.out.write(rot13_form)

	def post(self):
		rot = self.request.get("rot13")
		to_rot13 = self.Rot(rot)
		self.response.out.write(rot13_form % {"rot":to_rot13})

app = webapp2.WSGIApplication([('/', MainPage),('/thanks',ThanksHandler),('/rot13',Rot13)], debug=True)