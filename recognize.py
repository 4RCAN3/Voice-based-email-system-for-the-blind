import speech_recognition as sr

def recognizeSpeech(engine, keywords : tuple = None, message: str = "Please speak into the microphone"):

    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=1)

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

        if message != None:
            engine.say(message)
            engine.runAndWait()
            engine.stop()

        audio = recognizer.listen(source)

        try:
            transcription = recognizer.recognize_google(audio)
            if 'upper' in transcription:
                transcription = transcription.split('upper')
                transcription = [i.title() for i in transcription]
                transcription = ''.join(transcription)

            print(transcription)
            if keywords != None:
                for key in keywords:
                    if key in transcription:
                        return transcription, key
                
                return recognizeSpeech(engine, keywords = keywords, message = "The message you spoke was not one of the desired choices. Please speak again." if message != None else None)
            
        except sr.RequestError:
        # API was unreachable or unresponsive
            return "Unable to reach the API"
        except sr.UnknownValueError:
            # speech was unintelligible
            return recognizeSpeech(engine, keywords = keywords, message = message)


        return transcription