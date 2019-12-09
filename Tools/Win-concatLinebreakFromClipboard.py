import pyperclip
text = pyperclip.paste()
pyperclip.copy("\""+text.replace("\r\n","\\n")+"\"")
print("Copied to clipboard")
print(pyperclip.paste())

