from setuptools import setup
import subprocess

subprocess.call(["pip","install", "git+git://github.com/riccardoscalco/Pykov@master"])


setup(
    name='chainchat',
    version='1.0',
    description='chainchat is a simple Markov chain based way to generate chats from historical data.',
    author='Lennart Mischnaewski',
    author_email='lenmisch@gmail.com',
    url='https://github.com/leny-mi/chainchat',
    py_modules=['chainchat'],
    setup_requires=['wheel'],
    install_requires=['scipy', 'numpy', 'six', 'pykov==1.1']
)
