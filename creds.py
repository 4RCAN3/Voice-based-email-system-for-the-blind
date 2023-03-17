from dotenv import load_dotenv
import os
import pyttsx3
import voice, recognize
import csv, time

class creds():

    def __init__(self) -> None:
        """
        Loads the automated voice engine and the settings required for it 
        """        

        load_dotenv()
        vSettings = dict(csv.reader(open('VoiceSettings.csv')))
        self.vSettings = vSettings
        pass


    def getCreds(self) -> tuple:
        """
        Returns the email-id and password entered by the user.
        Prompts the user to enter the mail and pass using voice or keyboard.


        Returns tuple:
        "myMail" (str) : Mail of the user
        "myPass" (str) : Password for the respective email id
        """        

        self.myMail = os.environ.get('EMAIL')
        self.myPass = os.environ.get('PASS')

        def keyCreds(engine: object) -> tuple:
            """
            Prompts the user to enter the credentials by typing.

            Args:
                engine (object): Automated voice engine

            Returns:
                tuple: returns the credentials
            """            

            engine.say("Please type your mail now")
            engine.runAndWait()
            myMail = input("Enter your mail: ")
            engine.say("Please type your password now")
            engine.runAndWait()
            myPass = input("Enter your password: ")
            engine.stop()
            
            return myMail, myPass

        def voiceCreds(engine: object) -> tuple:
            """
            Prompts the user to enter the credentials using their voice.
            It is suggested to speak the mail and password letter by letter 
            as mails and passwords can be different than how they are pronounced 
            
            Example: Hello can be written as H31L0 in a password.

            Usage: If a letter is intended to be a capital letter, speak "upper" before speaking that letter.

            It is suggested to use the keyboard in case the email id or password 
            is hard to speak and difficult to recognize through normal speech.

            Args:
                engine (object): Automated voice engine

            Returns:
                tuple: Returns the credentials
            """            

            myMail = recognize.recognizeSpeech(engine, message = "Please speak your mail letter by letter now")
            myPass = recognize.recognizeSpeech(engine, message = "Please speak your password letter by letter now")

            myPass = myPass.replace('capital', '')
            myMail, myPass = ''.join(myMail.split()), ''.join(myPass.split())

            return myMail, myPass

        def confirmation(engine: object, creds : tuple) -> tuple:
            """Asking the user toe confirm the credentials that they have entered

            Args:
                engine (object): Automated voice engine
                creds (tuple): Credential tuple
            """       

            myMail, myPass = creds
            engine.say(f"Your mail is {myMail}")
            engine.runAndWait()
            engine.say(f"Your password is {myPass}")
            engine.runAndWait()

            transcript, key = recognize.recognizeSpeech(engine, keywords = ('yes', 'no'), message = 'Please confirm your credentials by speaking yes or no')
            
            return creds if key == 'yes' else enterCreds(engine)



        def enterCreds(engine: object) -> tuple:
            """
            Prompts the user to speak a choice of entering the credentials through keyboard or voice.
            Speaking the word keyboard or voice in their speech will trigger the application to move forward accordingly.

            Args:
                engine (object): Automated voice engine

            Returns:
                tuple: Returns the credentials
            """            

            engine.say("Would you like to enter your credentials through the keyboard or voice?")
            engine.runAndWait()
            transcript, key = recognize.recognizeSpeech(engine, keywords = ('voice', 'keyboard'), message = "Please speak your choice into the microphone")
            
            engine.say(f"Please enter your choice through: {key}")
            engine.runAndWait()
            engine.stop()

            return confirmation(engine, keyCreds(engine)) if key == 'keyboard' else confirmation(engine, voiceCreds(engine))


        if ((self.myMail, self.myPass) != (None, None)):
            return (self.myMail, self.myPass)
        else:
            return enterCreds(voice.voice(self.vSettings))
    


creds = creds() 
print(creds.getCreds())