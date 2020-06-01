from distutils.core import setup

setup(
    name='chainchat',
    version='1.0',
    description='chainchat is a simple Markov chain based way to generate chats from historical data.',
    author='Lennart Mischnaewski',
    author_email='lenmisch@gmail.com',
    url='https://github.com/leny-mi/chainchat',
    py_modules=['chainchat'],
    install_requires=['scipy', 'numpy', 'six',
    'pykov @ git+git://git@github.com/riccardoscalco/Pykov@master#egg=pykov']

    #https://github.com/riccardoscalco/Pykov
)
