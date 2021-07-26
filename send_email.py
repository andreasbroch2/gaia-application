from smtplib import SMTP

smtp = SMTP()
try:
    smtp.set_debuglevel(1)
    smtp.connect('mail.dandomain.dk', 366)
    print('Connect')
    try:
        smtp.login('andreas@gaiamadservice.dk', '17129223Ab')
        print('Login')
    except:
        print('Error: Unable to login')
    from_addr = "Andreas Broch <andreas@gaiamadservice.dk>"
    to_addr = "test-0vrix5uz6@srv1.mail-tester.com"
    message_subject = "disturbance in sector 7"
    message_text = "Three are dead in an attack in the sewers below sector 7."
    message = """From: Andreas Broch <andreas@gaiamadservice.dk> To: <test-0vrix5uz6@srv1.mail-tester.com> Subject: Test af Python\n
    Hej med dig din smukke satan
    """
    print('Sending...')
    smtp.sendmail(from_addr, to_addr, message)
    smtp.quit()     
    print("Successfully sent email")
except:
   print ("Error: unable to connect")