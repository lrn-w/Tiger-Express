# -*- coding: utf-8 -*-
import smtplib

class TEMessage:


    def __init__(self, SMS_Notifications):
        self.SMS_Notifications = SMS_Notifications
        print("Loading message class")
        # modify email 

    def sendMessage(self, msgSub, msgBody):
        if self.SMS_Notifications:
            print("Sending message")
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.ehlo()
            session.starttls()
            session.login("xxx@gmail.com", "xxx")
            headers = "\r\n".join(["from: Tiger Express",
                           "subject: " + msgSub,
                           "to: " + "xxx@tmomail.net",
                           "mime-version: 1.0",
                           "content-type: text/html"])
            content = headers + "\r\n\r\n" + msgBody
            session.sendmail("xxx@gmail.com","xxx@tmomail.net",content)
            session.close()
#Alltel
#[10-digit phone number]@message.alltel.com
#Example: 1234567890@message.alltel.com

#AT&T (formerly Cingular)
#[10-digit phone number]@txt.att.net
#[10-digit phone number]@mms.att.net (MMS)
#[10-digit phone number]@cingularme.com
#Example: 1234567890@txt.att.net

#Boost Mobile
#[10-digit phone number]@myboostmobile.com
#Example: 1234567890@myboostmobile.com

#Nextel (now Sprint Nextel)
#[10-digit telephone number]@messaging.nextel.com
#Example: 1234567890@messaging.nextel.com

#Sprint PCS (now Sprint Nextel)
#[10-digit phone number]@messaging.sprintpcs.com
#[10-digit phone number]@pm.sprint.com (MMS)
#Example: 1234567890@messaging.sprintpcs.com

#T-Mobile
#[10-digit phone number]@tmomail.net
#Example: 1234567890@tmomail.net

#US Cellular
#[10-digit phone number]email.uscc.net (SMS)
#[10-digit phone number]@mms.uscc.net (MMS)
#Example: 1234567890@email.uscc.net

#Verizon
#[10-digit phone number]@vtext.com
#[10-digit phone number]@vzwpix.com (MMS)
#Example: 1234567890@vtext.com

#Virgin Mobile USA
#[10-digit phone number]@vmobl.com
#Example: 1234567890@vmobl.com
