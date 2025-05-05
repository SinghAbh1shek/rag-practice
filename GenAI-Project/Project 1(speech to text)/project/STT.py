import speech_recognition as sr


filename = "harvard.wav"

# initialize the recognizer
r = sr.Recognizer()

# open the fileimport speech_recognition as sr

filename = "harvard.wav"
r = sr.Recognizer()
def speech_recognizer():
    try:
        with sr.AudioFile(filename) as source:
            r.adjust_for_ambient_noise(source)
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            print("Transcription:", text)
            return text

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# speech_recognizer()