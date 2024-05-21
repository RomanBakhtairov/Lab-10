import json, time, pyttsx3, pyaudio, vosk, requests, os, cv2, webbrowser
from main import Recognize, AloudSpeaker



COMMANDS = [{"id":0, "trig": "find", "func":lambda : speak('Please say the word you`re looking for',rec ) },
            {"id":1, "trig": "save", "func": lambda: beginner.ReturnExecutor().save()},
            {"id":2, "trig": "meaning", "func": lambda: beginner.ReturnExecutor().meaning() },
            {"id":3, "trig": "example", "func": lambda: beginner.ReturnExecutor().example() },
            {"id":4, "trig": "link", "func": lambda: beginner.ReturnExecutor().link()  }
            ]

class Listener:
    def __init__(self,rec) -> None:
        self.rec = rec
        self.executor = Executor('dog',rec, False)
        

    def SetTextReciver(self, rec_text_gen):
        self.text_gen = rec_text_gen

    def ReturnExecutor(self):
        return self.executor

    def StartDetecting(self):
        command = COMMANDS[0]
        preparingToFind = False
 #       self.executor.do(COMMANDS[4]) - There you can try some test commands
        for text in self.text_gen:
            gotten_command = self.executor.check(text)
            print(text)
            if gotten_command!= None:
                self.executor.do(gotten_command)
            elif text.startswith(command['trig']):
                command['func']()
                preparingToFind = True
            elif preparingToFind:
                preparingToFind =False
                self.executor = Executor(text.split()[0], self.rec)
            
class Executor:

    def __init__(self, wordname, rec, need_we_write= True):
        self.path = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        self.path += wordname
        self.myData =  requests.get(self.path).content
        if need_we_write:
            speak("I find information about word "+ wordname + 
                  "I can show you meaning, save the date, show example or give you link to the word", rec)
            print( str(self.myData))

    def check(self, text):
        for command in COMMANDS[1:]:
            if text.startswith(command['trig']):
                return command
        return None
    
    def do(self, command):
        b = command['func']
        b()

    #
    #
    #
    def save(self):
        f = open("notions.txt", "a")
        f.write('\n' + str(self.myData))
        f.close()
        speak("we saved it!",rec )
    #
    #
    #
    def meaning(self):
         data = json.loads(self.myData)
         data = data[0]
         means  =  data['meanings']
         means = means[0]
         means = means["definitions"]
         means = means[0]
         means = means["definition"]
         speak("Of corse! The word" + str(data["word"]) + ' mean ' + means ,rec )
    #
    #
    # 
    def link(self):
        speak("Of course. I am opening for you link in browser" ,rec )
        webbrowser.open(self.path, new=2)
    #
    #
    #
    def example(self):
         data = json.loads(self.myData)
         data = data[0]
         example  =  data['meanings']
         example = example[0]
         example = example["definitions"]
         example = example[0]
         try:
            example = example["example"]
            speak("Of course! There is example of the word " + str(data["word"]) + ': ' + example ,rec )
         except:
            speak("Sorry, there are not any examples of the word " + str(data["word"]),rec)





    
            
    

def speak(text, rec):
    speech = AloudSpeaker()
    rec.stream.stop_stream()
    speech.TextToSpeach(speaker=1, text=text)
    time.sleep(0.5)
    rec.stream.start_stream()
          




rec = Recognize()
beginner = Listener(rec)
text_gen = rec.listen()
beginner.SetTextReciver(text_gen)
beginner.StartDetecting()

# req =  requests.get("https://rickandmortyapi.com/api/character/avatar/108.jpeg")
# with open('img.jpeg','wb') as f:
#     f.write(req.content)


# img = cv2.imread('img.jpeg')
# cv2.imshow('name', img)
# cv2.waitKey(0)
# del('/')