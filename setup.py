from setuptools import setup

setup(
    name='RevTheShell',
    version='1.0',
    author='https://github.com/0xGamer',
    author_email='0xGamerhtb@gmail.com',
    description='Python script to generate reverse shells quickly.'
                'URL encoding the command and setting up a listener.',
    install_requires=['pyperclip', 'colorama', 'readchar', 'netifaces']
)
