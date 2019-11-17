#!/usr/bin/env python3


from multiprocessing import Process
import speech_recognition as sr


__author__ = "Siddhartha Pradhan (drunkenmaster)"
__version__ = "1.0"

r = sr.Recognizer()
mic = sr.Microphone()

testSpeechRecognizer = False  # Change to true to debug the speech_recognizer()


# recognize_houndify() maybe use to compare for accuracy?


def speech_recognizer(recognizer, raw_audio):
    # received audio data, now use Google API
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance.")

    try:
        speech = recognizer.recognize_google(raw_audio)
        print(speech)
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio.\n"
              "Try again with a clearer voice.")
    except sr.RequestError as re:
        print("Could not request results from Google Speech Recognition services; {0}".format(re))


# Just for testing move along...
def speechRecognizerSimpleTest():
    harvard_test = sr.AudioFile("harvard.wav")
    with harvard_test as source:
        test_audio = r.record(source)
    speech_recognizer(r, test_audio)


def listenerProcess():
    global voiceRec2, voiceRec, notFlipped
    with mic as source:
        print("Adjusting to ambient noise levels. Please wait.")
        r.adjust_for_ambient_noise(source, duration=2)  # Calibrating noise levels
        print("P1: Ready to listen.")
        # start_time = time.time()
        print("P1: Listening.....")
        audio2 = r.listen(source)
        print("P1 done listening")
        # print(time.time()-start_time)
        if notFlipped:
            voiceRec2 = audio2
        else:
            voiceRec = audio2


def startingListener():
    with mic as source:
        print("Initial adjustment to ambient noise levels. Please wait.")
        r.adjust_for_ambient_noise(source, duration=10)  # Calibrating noise levels
        print("Ready to listen.")
        print("Listening.....")
        audio1 = r.listen(source)
        print("Done Listening")
        return audio1


if __name__ == "__main__":
    notFlipped = True
    voiceRec = startingListener()
    voiceRec = sr.AudioData()

    while True:
        if notFlipped:
            p1 = Process(target=listenerProcess())
            p2 = Process(target=speech_recognizer(voiceRec))
            p1.start()
            p2.start()
            notFlipped = False
        else:
            p1 = Process(target=speech_recognizer(voiceRec2))
            p2 = Process(target=listenerProcess())
            p1.start()
            p2.start()
            notFlipped = True
