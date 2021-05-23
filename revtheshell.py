#!/usr/bin/env python3
# coding=utf-8
import os
import urllib.parse
from string import Template
from typing import List
import netifaces as ni
import readchar
from colorama import Fore, Style
from netifaces import *
from pyperclip import copy

banner = '''
 ███████████                           ███████████ █████                   █████████  █████               ████  ████ 
░░███░░░░░███                         ░█░░░███░░░█░░███                   ███░░░░░███░░███               ░░███ ░░███ 
 ░███    ░███   ██████  █████ █████   ░   ░███  ░  ░███████    ██████    ░███    ░░░  ░███████    ██████  ░███  ░███ 
 ░██████████   ███░░███░░███ ░░███        ░███     ░███░░███  ███░░███   ░░█████████  ░███░░███  ███░░███ ░███  ░███ 
 ░███░░░░░███ ░███████  ░███  ░███        ░███     ░███ ░███ ░███████     ░░░░░░░░███ ░███ ░███ ░███████  ░███  ░███ 
 ░███    ░███ ░███░░░   ░░███ ███         ░███     ░███ ░███ ░███░░░      ███    ░███ ░███ ░███ ░███░░░   ░███  ░███ 
 █████   █████░░██████   ░░█████          █████    ████ █████░░██████    ░░█████████  ████ █████░░██████  █████ █████
░░░░░   ░░░░░  ░░░░░░     ░░░░░          ░░░░░    ░░░░ ░░░░░  ░░░░░░      ░░░░░░░░░  ░░░░ ░░░░░  ░░░░░░  ░░░░░ ░░░░░ 
                                                                                                                     
 Made with <3 by 0xGamer (gamerboy181#3893 on discord). Inspired by t0thkr1s's reverse shell generator.                                                                                                                     
                                                                                                                      
'''

header = Template(
    '\n' + Style.BRIGHT + '---------- [ ' + Fore.CYAN + '$text' + Fore.RESET + ' ] ----------' + Style.RESET_ALL + '\n'
)
prompt = Template(
    Style.BRIGHT + '[' + Fore.BLUE + ' # ' + Fore.RESET + '] ' + Style.RESET_ALL + '$text : ' + Style.BRIGHT
)
code = Template(Style.BRIGHT + Fore.GREEN + '$code' + Style.RESET_ALL)
success = Template(Style.BRIGHT + '[' + Fore.GREEN + ' + ' + Fore.RESET + '] ' + Style.RESET_ALL + '$text')
info = Template(Style.BRIGHT + '[' + Fore.YELLOW + ' ! ' + Fore.RESET + '] ' + Style.RESET_ALL + '$text')
fail = Template(Style.BRIGHT + '[' + Fore.RED + ' - ' + Fore.RESET + '] ' + Style.RESET_ALL + '$text')
import os

ip = port = shell = command = ''

choices = ['no', 'yes']
shells = ['/bin/sh', '/bin/bash', '/bin/zsh', '/bin/ksh', '/bin/tcsh', '/bin/dash']
commands = sorted([command for command in os.listdir('commands')])


def print_banner():
    print(banner)


def exit_program():
    print('\n' + success.safe_substitute(text='My necessaries are embark\'d: farewell.'))
    exit(0)


def select(
        options: List[str],
        selected_index: int = 0) -> int:
    print('\n' * (len(options) - 1))
    while True:
        print(f'\033[{len(options) + 1}A')
        for i, option in enumerate(options):
            print('\033[K{}{}'.format(
                '\033[1m[\033[32;1m x \033[0;1m]\033[0m ' if i == selected_index else
                '\033[1m[   ]\033[0m ', option))
        keypress = readchar.readkey()
        if keypress == readchar.key.UP:
            new_index = selected_index
            while new_index > 0:
                new_index -= 1
                selected_index = new_index
                break
        elif keypress == readchar.key.DOWN:
            new_index = selected_index
            while new_index < len(options) - 1:
                new_index += 1
                selected_index = new_index
                break
        elif keypress == readchar.key.ENTER:
            break
       
        elif keypress == readchar.key.CTRL_C:
            raise KeyboardInterrupt
    return selected_index


def specify_ip():
    print(header.safe_substitute(text='SELECT IP'))
    global ip
    try:
      ni.ifaddresses('tun0')
      ip_address = ni.ifaddresses('tun0')[ni.AF_INET][0]['addr']
      if ip_address != '127.0.0.1':
          ip = ip_address
          print(ip_address + ' on tun0')
      else:
          ip = input(prompt.safe_substitute(text='Not able to detect a valid IP. Please enter the IP manually'))
    except ValueError:
      ip = input(prompt.safe_substitute(text='Not able to detect tun0. Please enter the IP manually'))


def specify_port():
    print(header.safe_substitute(text='SPECIFY PORT'))
    while True:
        try:
            input_port = input(prompt.safe_substitute(text='Enter port number'))
            if int(input_port) in range(1, 65535):
                global port
                port = input_port
                break
            else:
                raise ValueError
        except ValueError:
            print(fail.safe_substitute(text='Please, choose a valid port number!'))


def select_command():
    print(header.safe_substitute(text='SELECT COMMAND'))
    global command
    command = commands[select(commands)]


def select_shell():
    if command != 'windows_powershell' and command != 'unix_bash_tcp' and command != 'unix_telnet' and command != 'unix_bash_udp' and command != 'windows_perl' and command != 'windows_python' and command != 'windows_ruby' and command != 'windows_dart' and command != 'z) None of the Above':
        print(header.safe_substitute(text='SELECT SHELL'))
        global shell
        shell = shells[(select(shells))]


def build_command():
    global command
    with open('commands/' + command) as f:
        command = Template(f.read())
    command = command.safe_substitute(ip=ip, port=port, shell=shell)
    print(header.safe_substitute(text='Do you want to URL Encode the command?'))
    if select(choices) == 1:
        command = urllib.parse.quote_plus(command)
        print(info.safe_substitute(text='Command is now URL encoded!'))

    print(header.safe_substitute(text='FINISHED COMMAND'))
    print(code.safe_substitute(code=command) + '\n')

    if 'SSH_CLIENT' not in os.environ or 'SSH_TTY' not in os.environ:
        copy(command)
        print(info.safe_substitute(text='Reverse shell command copied to clipboard!'))

    print(success.safe_substitute(text='In case you want to upgrade your shell, you can use this:\n'))
    print(code.safe_substitute(code="python -c 'import pty;pty.spawn(\"/bin/bash\")'"))


def setup_listener():
    if os.name != 'nt':
        print(header.safe_substitute(text='Do you want to start a listener too?'))
        if select(choices) == 1:
            os.system('\n$(which ncat || which nc) -nlvp ' + port)
        else:
            exit_program()


if __name__ == '__main__':
    print_banner()
    try:
        specify_ip()
        specify_port()
        select_command()
        select_shell()
        build_command()
        setup_listener()
    except KeyboardInterrupt:
        exit_program()