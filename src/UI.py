import os
import platform

if platform.system() == "Windows":
    os.system("color")


class UI:

    def __init__(self):
        self.text_style = {
            "*": "\033[1m",
            "~": "\033[4m",
            "r": "\033[91m",
            "g": "\033[92m",
            "t": "\033[32m",
            "b": "\033[94m",
            "y": "\033[93m",
            "c": "\033[96m"
        }

        self.end_style = "\033[0m"

    def style_print(self, msg, style=""):
        for char in style:
            print(self.text_style[char], end="")
        print(msg, end="\r")
        print(self.end_style)

    def style_input(self, msg, style=""):
        for char in style:
            print(self.text_style[char], end="")
        user_input = input(msg+self.end_style)
        return user_input
