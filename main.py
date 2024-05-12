import json, time, pyttsx3, pyaudio, vosk
class AloudSpeaker(): # I took english model
    def __init__(self) -> None:
        self.speaker = 0
        self.tts = pyttsx3.init('sapi5')
    def SetVoice(self, speaker):
        self.voices = self.tts.getProperty('voices')
        for count, voice in enumerate(self.voices):
            if count == 0:
                print('0')
                id = voice.id
            if speaker == count:
                id = voice.id
        return id
    def TextToSpeach(self,text = 'meow',speaker = 0):
        self.tts.setProperty('voice', self.SetVoice(speaker))
        self.tts.say(text)
        self.tts.runAndWait()
class Recognize:
    def __init__(self):
        model = vosk.Model('model_small')
        self.record = vosk.KaldiRecognizer(model, 16000)
        self.stream()

    def stream(self):
        pa = pyaudio.PyAudio()
        self.stream = pa.open(format=pyaudio.paInt16,
                         channels=1,
                         rate=16000,
                         input=True,
                         frames_per_buffer=8000)


    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.record.Result())
                if answer['text']:
                    yield answer['text']
def speak(text):
    speech = AloudSpeaker()
    speech.TextToSpeach(speaker=0, text=text)

if __name__ == "__main__":
    rec = Recognize()
    text_gen = rec.listen()
    rec.stream.stop_stream()
    speak('Starting')
    time.sleep(0.5)
    rec.stream.start_stream()
    for text in text_gen:
        if text == 'close':
            speak('Goodbuy, ihtiender')
            quit()
        else:
            print(text)
