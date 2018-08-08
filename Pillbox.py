#import st7565
#import xglcd_font as font
import os
import sys
import RPi.GPIO as GPIO
import time
import random
import requests

map = [8,5,23,17,2,13,15,9,21,1,0,19,11,27,22,4,14,3,25,7,16,6,10,24,18,20,10,26] #For the pillboxID to 28bit scrambling

pillboxID = 134854781
pillboxKey = "TestingKey99823" #Must consist of ASCII chars between 32 and 126
seedMaster = 'xMW59kR4JvFf9iW3djWxIPubljc2Up8FTkjL3TWJHGO1eXQ9oeC7EEd8haSC08kmlbaKC4MeoGz9ET5zksMYBI9f9a9Ne1gB0LMx'
seedCounter = 0
holdCounter = seedCounter
startIndex = 0
endIndex = 10
seedCurrent = seedMaster[startIndex:endIndex]

GPIO.setup(32, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setmode(GPIO.BOARD)
buzzerPin = 0
GPIO.setup(buzzerPin, GPIO.OUT) 
pinOuts = [31,11,37,15,29,13]
combos = [0,4,0,5,0,3,0,1,2,1,4,1,5,1,4,0,5,0,3,0,1,0,1,2,1,4,1,5,0,2,4,2,5,2,3,2,3,4,3,5,3,1,2,0,2,4,2,5,2,3,4,3,5,3,1,3]

#neato = font.XglcdFont('/home/pi/Pi-ST7565/fonts/Neato5x7.c', 5, 7) #5, 7 refers to the pixel size of each character. This file must exist
#glcd = st7565.Glcd(rgb=[21, 20, 16]) #Don't change these numbers
#glcd.init()

menuState = [1,0,0] #[First Item in Top Level, Not in Second Level, Not in Third Level]

sceduled
scheduledTimes = dict("pillID1": "green", "pillID2": "yellow")

menuData =  [[['ERBuddy Main Menu']],\
            [['Pill Schedule'],\
                ['Sunday'],\
                ['Monday'],\
                ['Tuesday'],\
                ['Wednesday'],\
                ['Thursday'],\
                ['Friday'],\
                ['Saturday'],\
                ['Back']], \
            [['Set Alarm']],\
            [['Emergency Contacts'],\
                ['Mary Stieber','212-435-2398','mary@example.com','123 Madeline Way','Back'],\
                ['John Adams','800-342-7734','adams@apples.org','77 High St','Back'],\
                ['Back']], \
            [['Change Contacts'],\
                ['New Contact','Back'],\
                ['Delete Contact','Back'],\
                ['Back']], \
            [['Settings'],\
                ['Screen Color','White','Cyan','Yellow','Orange','Purple','Blue','Back'],\
                ['Volume:   0','Increase','Lower','Silent','Back'],\
                ['Vibration','On','Off','Back'],['Back']], \
            [['Back']]]

volume = 0
newContact = [0]*5

def buzzerOn(): GPIO.output(buzzerPin, 1)
def buzzerOff(): GPIO.output(buzzerPin, 0)

def getMenuItem(L,i):
    if L == 0: return menuData[i][0][0]
    if L == 1: return menuData[menuState[0]][i][0]
    if L == 2: return menuData[menuState[0]][menuState[1]][i]

def printMenu():
    glcd.clear_display() #os.system('cls')
    i = 0
    while getMenuItem(level, i - 1) != 'Back' or i == 0:
        glcd.draw_string(getMenuItem(level, i), neato, i*8, 24,spacing=1,invert=1) #if menuState[level] == i: sys.stdout.write('#')
        else: glcd.draw_string(getMenuItem(level, i), neato, i*8, 24,spacing=1,invert=0) #print(getMenuItem(level, i))
        i += 1
        glcd.flip()

'''def textInput(str,alphabet,length):
    alphabet = alphabet + '>'
    output = ''
    inside = 0
    pos = 0
    while True:
        os.system('cls')
        print(str)
        print(output)
        i = 0
        while i < len(alphabet):
            if i == pos: sys.stdout.write('#')
            else: sys.stdout.write(alphabet[i])
            if i % length == length-1: sys.stdout.write('\n')
            i += 1
        ask = input()
        if ask == 'q' and inside:
            if pos % length == length-1: pos -= length-1 ; inside = 0
            else: pos += 1
        if ask == 'q' and not inside:
            pos += length
            if pos > len(alphabet): pos = 0
        if ask == 'w' and inside:
            if alphabet[pos] == '>': break
            else: output = output + alphabet[pos]
        if ask == 'w' and not inside: inside = 1
    return output'''

'''def addContact():
    newContact[0] = textInput('Name',' ABCDEFGHIJKLMNOPQRSTUVWXYZ',8)
    newContact[1] = textInput('Phone Number', '1234567890',3)
    newContact[2] = textInput('Email',' ABCDEFGHIJKLMNOPQRSTUVWXYZ@,.-',8)
    newContact[3] = textInput('Address',' ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',8)
    newContact[4] = 'Back'
    menuData[3].insert(1,newContact)'''

'''def updateDelContacts():
    menuData[4][2] = ['Delete Contact']
    i = 1
    while not menuData[3][i][0] == 'Back':
        menuData[4][2].append(menuData[3][i][0])
        i += 1
    menuData[4][2].append('Back')'''

'''def deleteContact(i):
    del menuData[3][i]
    updateDelContacts()'''    

def setColor(c):
    colorArray = [[100,50,50],[0,100,100],[100,50,0],[100,25,0],[100,0,50],[0,0,100]] #'White','Cyan','Yellow','Orange','Purple','Blue'
    r = colorArray[c][0]
    g = colorArray[c][1]
    b = colorArray[c][2]
    glcd = set_backlight_color(r,g,b) #print(r,g,b)

def getLevel():
    if menuState[2] != 0: return 2 
    elif menuState[1] != 0: return 1
    elif menuState[0] != 0: return 0
    else: return -1

def arrowButton():
    global level
    level = getLevel()
    if getMenuItem(2, menuState[2]) == 'Back': menuState[level] = 1
    else: menuState[level] += 1
    printMenu()

def enterButton():
    global level
    global volume
    level = getLevel()
    if getMenuItem(2, menuState[2]) == 'Back': menuState[level] = 0 ; level -= 1 #Exit a submenu
    #Put all the functions here
    elif menuState[0] == 5 and menuState[1] == 1 and not menuState[2] == 0: setColor(menuState[2])
    #elif menuState == [4,1,0]: addContact()
    #elif menuState[0] == 4 and menuState[1] == 2 and not menuState[2] == 0: deleteContact(menuState[2])
    elif menuState == [5,2,1] and volume < 100: volume += 10 ; menuData[5][2][0] = 'Volume:   ' + str(volume) #example changing volume
    elif menuState == [5,2,2] and volume > 0: volume -= 10 ; menuData[5][2][0] = 'Volume:   ' + str(volume)
    elif level < 2: level += 1 ; menuState[level] = 1 #Enter a submenu
    if menuState == [0,0,0]: os.system('cls') ; print('Idling...')
    else: printMenu()

def EncryptData(data, seed):
    random.seed(seed)
    c = 0
    while c != seedCounter:
        random.randrange(0,94)
        c += 1
    edata = ""
    c = 0
    while c < len(data):
        edata = edata + chr( ( ( ord(data[c]) - 32 + random.randrange(0,94) ) % 94 ) + 32 )
        seedCounter += 1
        c += 1
    return edata
    
def DecryptData(edata, seed):
    random.seed(seed)
    c = 0
    while c != seedCounter:
        random.randrange(0,94)
        c += 1
    data = ""
    c = 0
    while c < len(edata):
        data = data + chr( ( ( ord(edata[c]) + 62 - random.randrange(0,94) ) % 94 ) + 32 )
        seedCounter += 1
        c += 1
    return data
    
#updateDelContacts()

def ledWrite(pinOuts): #Display the leds until the enter button is pressed
    while True:
        for outLED in outLEDs:
            GPIO.setup(pinOuts, GPIO.IN)
            GPIO.setup(pinOuts[combos[outLED*2]], GPIO.OUT)
            GPIO.setup(pinOuts[combos[outLED*2+1]], GPIO.OUT)
            GPIO.output(pinOuts[combos[outLED*2]], GPIO.HIGH)
            GPIO.output(pinOuts[combos[outLED*2+1]], GPIO.LOW)
            time.sleep(0.002 / len(outLEDs)) #The total time it takes to cycle through the outLEDs array should always be ~2 milliseconds
            GPIO.output(pinOuts[combos[outLED*2]], GPIO.LOW) #Prevents voltage spikes from causing unintentional activations
            tally += 1
        if GPIO.input(12): break

def registerPillbox():
    r = requests.put('http://myerbuddy.com/erbuddyapi/register-phone-case/' + str(pillboxID), data = EncryptData(pillboxKey, seedCurrent))
    bits = ""
    while ID != 0:
        if ID & 1: bits = "1" + bits
        else: bits = "0" + bits
        ID = ID >> 1
        if len(bits) <= 28:
    while len(bits) < 28:
        bits = "0" + bits
    count = 0
    code = [0]*28
    while count < 28:
        code[count] = bits[map[count]]
        count += 1
    ledWrite(code)

while True:
    
    #if ask == 'q' and menuState != [0,0,0]:arrowButton()
        
    if GPIO.input(12): enterButton()

#glcd.draw_string('abcdefghijklmnopqrstu', neato, 0, 24,spacing=1,invert=1)
#glcd.flip()

