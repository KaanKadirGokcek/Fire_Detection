from email.mime.text import MIMEText
import cv2
import pygame
from smtplib import SMTP


pygame.mixer.init()
alarm_sound = pygame.mixer.Sound("alarm.mp3")

fire_cascade = cv2.CascadeClassifier("fire_cascade.xml")
cap = cv2.VideoCapture(0)

fire_detected = False

try:
    subject = "Yangin Alarmi"
    message = "Ateş tespit edildi"
    content = "Subject: {0}\n\n{1}".format(subject,message)

    myMailAdress = "xxxxxxx@outlook.com"
    password ="xxxxxxx"

    sendTo = "zzzzzzz@hotmail.com"

    mail = SMTP("smtp.office365.com", 587)
    mail.ehlo()
    mail.starttls()
    mail.login(myMailAdress,password)
    #mail.sendmail(myMailAdress, sendTo, content)
    print("Mail Gonderme İslemi Basarili!")

    while True:
        ret,frame = cap.read()
        frame = cv2.resize(frame,(800,700))
        frame = cv2.flip(frame,1)
        
        if ret == False:
            break
    
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        fire = fire_cascade.detectMultiScale(frame, 1.2, 3)

        if len(fire) > 0 and not fire_detected:
            for (x,y,w,h) in fire:
                cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),3)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                print("Fire Detection")
            
                alarm_sound.play()
                fire_detected = True

                try:
                    msg = MIMEText(content, 'plain', 'utf-8')
                    msg['Subject'] = subject
                    msg['From'] = myMailAdress
                    msg['To'] = sendTo

                    if not mail.sock:
                        mail.connect(mail.host, mail.port)
                    
                    mail.sendmail(myMailAdress, sendTo, msg.as_string())
                    print("Mail Gonderme İslemi Basarili!")
                except Exception as e:
                    print("Mail gonderirken hata olustu!\n{0}".format(e))

        else:
            fire_detected = False

        cv2.imshow("Output", frame)
        if cv2.waitKey(1) & 0xFF==ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

except Exception as e:
    print("Hata Olustu!\n {0}".format(e))

finally:
    if hasattr(mail, 'sock') and mail.sock:
        mail.quit()