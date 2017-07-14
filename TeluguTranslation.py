# -*- coding: utf-8 -*-
import numpy as np
import sys
import os
import bs4
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from gtts import gTTS
import re
import pyaudio
import speech_recognition as sr

r = sr.Recognizer() 
r = sr.Recognizer()
r.energy_threshold = 2000

def RemoveRepeitions(Text):
	Text = re.sub(r'(\d)\1+', r'\1', Text)
	return Text

def RemoveSymbols(Text):
	Text = Text.strip()
	Text = Text.replace('ā', 'a')
	Text = Text.replace('ō', 'oo')
	Text = Text.replace('ē', 'e')
	Text = Text.replace('ṁ', 'm')
	Text = Text.replace('ṅ', 'n')
	Text = Text.replace('ṣ', 's')
	Text = Text.replace('ṇ', 'n')
	Text = Text.replace('ṭ', 't')
	Text = Text.replace('ī', 'i')
	Text = Text.replace('n̄', 'n')
	Text = Text.replace('ḍ', 'd')
	Text = Text.replace('ū', 'u')
	Text = Text.replace('ḷ', 'l')
	Text = Text.replace('Ṭ', 'ta')
	Text = Text.replace('c', 'ch')
	Text = Text.replace('g', 'g')
	Text = Text.strip()
	return Text

def Run():
	inputType = raw_input('Would you like to use voice recognition or enter in the text manunally?[v/m]: ')
	if inputType == 'v':
		with sr.Microphone() as source:
		    print("Say the sentence which you want annunciated!")
		    audio = r.listen(source)
		try: 
		    print("You Said: " + r.recognize_google(audio))
		    userInput = r.recognize_google(audio)
		except LookupError:
		    print("Could not understand audio")
	else:
		userInput = raw_input('Enter what you want aununciated: ')

	userInput = userInput.replace(" ", "%20")
	url = 'https://translate.google.com/#en/te/' + userInput
	driver = webdriver.PhantomJS()
	driver.get(url)
	Pagehtml = driver.page_source
	parseredPage = soup(Pagehtml, "html.parser")
	Aununciation = parseredPage.find("div",{"id":"res-translit"}).text
	Aununciation = Aununciation.encode('utf8')
	Aununciation = RemoveSymbols(Aununciation)
	Aununciation = RemoveRepeitions(Aununciation)
	print("_______________________________________________________")
	print("Pronunciation of Input: " + Aununciation + '\n')
	tts = gTTS(text=Aununciation, lang='es')
	tts.save("output.mp3")
	os.system("mpg321 output.mp3")
	print("_______________________________________________________")
	os.remove("output.mp3")
	Con = raw_input('Would you us like to annunciate another phrase?[y/n:] ')
	if Con == 'n':
		sys.exit()


while(True):
	Run()