import smtplib

def send_mail(to,validator):
  #TO = 'a.angelov83y@gmail.com'
  #SUBJECT = 'TEST MAIL'
  #TEXT = 'Here is a message from python.'
  subject='Thank you for your registration. Please submit the verification \
  code we provide below to complete your registration'
  # Gmail Sign In
  text=validator
  gmail_sender = 'takser.test@gmail.com'
  gmail_passwd = 'tasker_test'

  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.login(gmail_sender, gmail_passwd)

  BODY = '\r\n'.join(['To: %s' % to,'From: %s' % gmail_sender,'Subject: %s' % subject,'', text])

  try:
    server.sendmail(gmail_sender, to, BODY)
    server.quit()
  except:
    server.quit()
    raise cherrypy.HTTPRedirect("mail_send_error")
