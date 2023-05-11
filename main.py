from dotenv import load_dotenv
import os
import pyttsx3
import voice, recognize
import csv, time
import creds
import mailing

class Commands():

    def __init__(self) -> None:
        """
        Loads the automated voice engine and the settings required for it
        Gets the user credentials if already stored, else, prompts the user to enter their credentials
        """ 

        load_dotenv()
        vSettings = dict(csv.reader(open('VoiceSettings.csv')))
        self.vSettings = vSettings
        self.engine = voice.voice(vSettings)

        credentials = creds.creds()
        self.myMail, self.myPass = credentials.getCreds()

    def SendMail(self):
        print('send mail')
        mailSys =  mailing.Mails(username=self.myMail, password=self.myPass)

        engine = self.engine
        engine.say('Would you like to enter the recipient mail using a keyboard or by voice?')
        transcript, key = recognize.recognizeSpeech(engine, keywords = ('voice', 'keyboard'), message = "Please speak your choice into the microphone")
            
        engine.say(f"Please enter your choice through: {key}")
        engine.runAndWait()
        
        if key == 'keyboard':
            engine.say("Please type the email address of the recipient")
            engine.runAndWait()
            receiverMail = input("Enter receiver mail")

        else:
            receiverMail = recognize.recognizeSpeech(engine, message = "Please speak your mail letter by letter now")
            receiverMail = ''.join(receiverMail.split())


        subjectMail = recognize.recognizeSpeech(engine, message = "Please speak the subject of your mail")
        mailBody = recognize.recognizeSpeech(engine, message = "Please speak the body of your mail")

        mailSys.SendMail(receiverMail=receiverMail, Subject=subjectMail, content=mailBody)
        engine.say("Your mail has been sent")
        engine.runAndWait()
        engine.stop()


    def ReadMail(self):
        mailSys =  mailing.Mails(username=self.myMail, password=self.myPass)
        engine = self.engine
        engine.say("Reading the latest mail from your inbox")
        engine.runAndWait()
        Subject, MailFrom, Body = mailSys.ReadMail()
        print("From:", MailFrom)
        engine.say(f"The mail is sent from {MailFrom}")
        engine.say(f"Subject of the mail is {Subject}")
        print("Subject:", Subject)
        engine.say(f"Content of the mail is {Body}")
        print("Mail Body:", Body)
        engine.runAndWait()
        engine.stop()


if __name__ == '__main__':
    commands = Commands()
    engine = commands.engine
    engine.say("Hello, I am functioning now, and I will be listening to your audio input. Please use the send mail and read mail commands to perform the respective functions")
    engine.runAndWait()
    while True:
        transcript, key = recognize.recognizeSpeech(engine, keywords = ('send mail', 'read mail'), message = None)
        
        if key.lower() == 'send mail':
            commands.SendMail()
        elif key.lower() == 'read mail':
            commands.ReadMail()