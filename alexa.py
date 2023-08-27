
from re import search
from gtts import gTTS
import os
from playsound import playsound
import datetime
import speech_recognition as sr
import random
import requests
from bs4 import BeautifulSoup
import pywhatkit
import wikipedia
import pyjokes
from googletrans import Translator, constants
import webbrowser
import time

LANG="ar"
wikipedia.set_lang(LANG)  
translator = Translator()

preReponses = [' .حسنا.',' .تحت أمرِكْ.',' .أمركَ مُطاعْ.',' .أوكي',' .أنا مشغولةٌ الآنْ. لكنْ سأجيبكْ.',' .لا أريدُ الإجابةَ على سؤالكْ. لاتقلقْ. فقطْ أمزحُ معكْ.']
preReponses2 = [' ابشر',' .من عيوني.',' .انت تامرني.',' الان',' .حسنا انا تحت امرك.',' .ساخدمك بكل تاكيد']
presorry = [' امم لا استطيع المساعدة','لم استطيع فهم طلبك',' .لا اعرف ذلك',' انا اسفة لم افهمك',' .امم حاول مره ثانيه ',' .انا اواجه مشكلة حاول مره ثانية']
linux = 'clear'
windows = 'cls'
headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
}

def speak(text):
    tts=gTTS(text=text,lang=LANG)
    tts.save("hello.mp3")
    playsound("hello.mp3",True)
    os.remove("hello.mp3")
listener = sr.Recognizer()

def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def get_date():
    return datetime.datetime.now().strftime("%A %d/%m/%Y")

def listen():
    try:
        with sr.Microphone() as source:
            print("..انا في الاستماع") # جاري الاستماع من المايك 
            os.system([linux, windows][os.name == 'nt'])
            time.sleep(0.3)
            voice=listener.listen(source)
            command=listener.recognize_google(voice, language=LANG)
            if 'اليكسا' in command: # اختار اسم للمساعد الرقمي الخاص بك
                print(command)
                return command
            else:
                return ""
    except:
        i=random.randint(0,5)
        intro = presorry[i]
        speak(intro) 
        


def run():
    v=True
    while v:
        command= listen()
        if not command is None:
            r=random.randint(0,5)
            i=random.randint(0,5)
            intro = preReponses[i]
            intro2 = preReponses2[r]
            if 'اغلاق' in command:
                v=False
            elif 'كم الساعه' in command:
                speak(intro + ".الساعة الان هي ." +get_time())
            elif 'تاريخ' in command:
                speak(intro + ".التاريخ الان هو ." +get_date())
            elif 'كيف حالك' in command:
                speak(".بخير الحمد لله .")
            elif 'هل تحبني' in command:
                speak("نعم اكثر من نفسي")
            elif 'عنوانك' in command:
                speak("انا مساعد شخصي اسكن عبر سحابة اكترونية") 
            elif 'انا رجعت' in command:
                speak("نورت المكان") 
            elif 'اخبار' in command:
                URL = "https://www.alarabiya.net/saudi-today"
                page = requests.get(URL, headers=headers)   
                soup = BeautifulSoup(page.content, 'html.parser')
                l = [a.text for a in soup.select('div li a h4')]
                for a in l:
                    print(a)
                    speak(a)
            elif 'لدي سؤال' in command or 'ابحث عن' in command or 'لدي سوال' in command or 'ابحث في المتصفح' in command:
                question = command.replace('لدي سؤال', '')
                question = question.replace('اليكسا', '')
                speak(intro + " ها هي " + command) 
                pywhatkit.search(command)

            elif 'اغلق الجهاز' in command or 'قفل الجهاز' in command or 'اغلاق الجهاز' in command or 'وقف الجهاز' in command:
                pywhatkit.shutdown(time=100)
            elif 'اغنيه' in command or 'موسيقى' in command or 'سوره' in command or 'صوره' in command:
                command = command.replace('اليكسا', '')   
                speak(intro or intro2 + " ها هي " + command)         
                pywhatkit.playonyt(command)
            elif 'كلميني عن' in command or 'كلمني عن' in command:   
                try:
                    command = command.replace('كلميني عن', '')  
                    command = command.replace('كلمني عن', '')        
                    command = command.replace('اليكسا', '')    
                    info = wikipedia.summary(command,1)
                    speak(info)     
                except:
                    speak("لم أستطع فهم طلبكم")
                    
            elif 'افتح اليوتيوب' in command:
                webbrowser.open_new_tab("https://youtube.com")
                speak(intro2 or intro) 
                time.sleep(3)

            elif 'افتح تويتر' in command:
                webbrowser.open_new_tab("https://twitter.com")
                speak(intro2 or intro) 
                time.sleep(3)

            elif 'افتح قوقل' in command or 'افتح جوجل' in command:
                webbrowser.open_new_tab("https://www.google.com")
                speak(intro2 or intro) 
                time.sleep(3)

            elif 'افتح البريد' in command:
                webbrowser.open_new_tab("https://mail.google.com/mail")
                speak(intro2 or intro) 
                time.sleep(3)

            elif "موقع" in command:
                speak(intro2 or intro) 
                webbrowser.open(f"https://www.google.com/maps/place/" + command)
                time.sleep(3)

    speak("مع السلامة")
        
run()