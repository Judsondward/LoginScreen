#!/usr/bin/python3
def caesar(text, s):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            result += chr((ord(char) + s-65) % 26 + 97)
        else:
            result += chr((ord(char) + s-97) % 26 + 97)
    return result