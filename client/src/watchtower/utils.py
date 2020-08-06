from colorama import init, Fore, Back, Style
import sys


class Display(object):
    color = False

    def __init__(self, color=True):
        init()
        self.color = color

    def print(self, msg_type, msg):
        prefix = ""
        color = ""
        bgcolor = ""
        msg_color = ""
        style = ""
        msg_style = ""
        reset = ""
        if self.color is True:
            style = Style.BRIGHT
            reset = Style.RESET_ALL
            if msg_type == "FAIL" or msg_type == "ERROR":
                color = Fore.RED
            if msg_type == "INFO":
                color = Fore.BLUE
            if msg_type == "TITLE":
                msg_color = Fore.YELLOW
                msg_style = Style.BRIGHT
            if msg_type == "WARN":
                color = Fore.YELLOW
            if msg_type == "ERR!":
                color = Fore.RED
            if msg_type == "PASS":
                color = Fore.GREEN
                msg_color = Fore.GREEN
            if msg_type == "FAIL":
                color = Fore.RED
                msg_color = Fore.RED
                msg_style = Style.BRIGHT
            if msg_type == "SUCCESS":
                color = Fore.WHITE
                bgcolor = Back.GREEN
            if msg_type == "FAIL ":
                color = Fore.YELLOW
                bgcolor = Back.RED

        line = (
            style
            + color
            + bgcolor
            + prefix
            + reset
            + msg_style
            + msg_color
            + msg
            + reset
        )
        print(line)
        sys.stdout.flush()
        return line
