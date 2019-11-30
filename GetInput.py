#!/usr/bin/python

import xml.etree.ElementTree as ET
import random
import smtplib
from User import User
from Credentials import cred_username
from Credentials import cred_password
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def parse_xml(input):
	temp = []
	for user in input.iter('User'):
		fname = user[0].text
		lname = user[1].text
		email = user[2].text
		luser = User(fname,lname,email)
		temp.append(luser)
	return temp

def send_mail(strTo,strFrom,subject,body):
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = subject
	msgRoot['From'] = strFrom
	msgRoot['To'] = strTo

	#Create alternative message with images using Multipart
	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)

	msgText = MIMEText( body, 'html')
	msgAlternative.attach(msgText)

	fp = open('SecretSanta.jpg', 'rb')
	msgImage = MIMEImage(fp.read())
	fp.close()

	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)

	#TODO: don't hardcode credentials, find another way
	username = cred_username
	password = cred_password
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(strFrom, strTo, msgRoot.as_string())
	server.quit()

#Get the list of users from xml file
finput = ET.parse('inputDataFile.xml').getroot()
senders = parse_xml(finput)
receivers = list(senders)
#print(senders)
#print(receivers)
distinct = False
while (distinct == False):
	random.shuffle(receivers)
	check = list(zip(receivers,senders))
	for x in check:
		#If we get a matching pair, try again
		if((x[0] == x[1])
				distinct = False
				break
		else:
			distinct = True

master_list = ""
for pair in check:
	print(pair[0].first_name + " " + pair[0].last_name + " : " + pair[1].first_name + " " + pair[1].last_name)
	master_list += pair[0].first_name + " " + pair[0].last_name + " : " + pair[1].first_name + " " + pair[1].last_name + "\n"

#email code
#send list of everyone to me
strFrom = 'your email address'
strTo = 'your email address'
subject = 'Secret Santa Master List 2019'
body = """<br>
		    <b>Merry Christmas everyone!</b>
			<br>
			<p>Secret Santa is back by popular demand.</p>
			<b>This is the master list for all participants. Don't share this with anyone!</b>
			<br>
			""" + str(master_list) + """
			<img src="cid:image1">
			<br> """

send_mail(strTo,strFrom,subject,body)

#send to everyone who their secret santa is
for user in check:
	strFrom = 'your email addres'
	strTo = user[0].email
	subject = 'Secret Santa 2019'

	body = """<br>
			    <b>Merry Christmas everyone!</b>
				<br>
				<p>Secret Santa is back by popular demand.</p>
				<p>This year, you will give a gift to:<b> """ + user[1].first_name + """ """ + user[1].last_name + """</b></p>
				<p>I'm looking forward to seeing you all again soon!</p>
				<img src="cid:image1">
				<br> """

	send_mail(strTo,strFrom,subject,body)
