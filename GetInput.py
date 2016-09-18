#!/usr/bin/python
def parse_xml(input):
	temp = []
	for user in input.iter('User'):
		fname = user[0].text
		lname = user[1].text
		email = user[2].text
		luser = User(fname,lname,email)
		temp.append(luser)
	return temp
import xml.etree.ElementTree as ET
import random
import smtplib
from User import User
from email.mime.text import MIMEText
#Get the list of users from xml file
finput = ET.parse('inputDataFile.xml').getroot()
senders = parse_xml(finput)
receivers = list(senders)
distinct = False
while (distinct == False):
	random.shuffle(receivers)
	check = zip(receivers,senders)
	for x in check:
		#if there is a match, then retry
		if((x[0] == x[1])):
			distinct = False
			break
		else:
			distinct = True
master_list = ""
#Print the list on-screen and create the text for the email you will receive
for pair in check:
	print(pair[0].first_name + " " + pair[0].last_name + " : " + pair[1].first_name + " " + pair[1].last_name)
	master_list += pair[0].first_name + " " + pair[0].last_name + " : " + pair[1].first_name + " " + pair[1].last_name + "\n"

#email code
#todo: add this to seperate file
#send list of everyone to me
msg = "\r\n".join([
  "From: your email address",
  "To: your email address",
  "Subject: Test",
  "",
  master_list
  ])
fromaddr = 'your email address'
toaddrs  = 'your email address'
username = 'your username'
password = 'your password'
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()

#send to everyone who their secret santa is
for user in check:
	msg = "\r\n".join([
	  "From: your email address",
	  "To: " + user[0].email,
	  "Subject: Test",
	  "",
	  "This is the secret santa .\nYou will give a gift to: " + user[1].first_name + " " + user[1].last_name
	  ])
	fromaddr = 'your email address'
	toaddrs  = user[0].email
	username = 'your username'
	password = 'your password'
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()
