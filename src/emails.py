# email related methods here

def send_email(email_address, message):
	import smtplib
	
	FROM = 'msisengali@gmail.com' 
	TO = [email_address]
	SUBJECT = "Notification"
	TEXT = message
	message = """\
	From: %s
	To: %s
	Subject: %s

	%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login('msisengali@gmail.com','margosha777')
	server.sendmail(FROM, TO, message)
	server.quit()
