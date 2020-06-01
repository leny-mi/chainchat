
# chainchat
A [Markov chain](https://en.wikipedia.org/wiki/Markov_chain) based module to generate a chat from historical data.
Using chainchat you can take feed in chat data to generate a finite state Markov chain to generate following messages. Markov chains are limited and have no memory as do RNN or similar models. Therefore they are not able to react to previous messages as we humans do. 
What they can do is quickly establishing a model that leads to at least slightly (or more) amusing results. That said, don't expect it to fool anyone or to write a poem. 

## Installation
chainchat can be installed with pip by using 
 
     > pip install git+git://github.com/leny-mi/chainchat@master

## Quickstart

    >>> messages = [('Alice', 'Hey there!'),
                ('Bob', 'Hey, what's up?'),
                ('Charlie', 'Shuf is fantastic. I tried it on a 78 billion line text file.')]

    >>> cc = chainchat.Chat(messages, max_walk_length = 1000, enhance = True)

    # Generate 2 messages
    >>> gen = cc.generate('Alice')
    >>> for _ in range(2):
            tpl = next(gen)
            print(": ".join(tpl))

    Bob: Hey, what's up?
    Charlie: Shuf is fantastic. I tried it on a 78 billion line text file.

    # Generates an infinite amount of messages
    >>> for tpl in cc.generate('Alice')():
            print(": ".join(tpl))

    Bob: Hey, what's up?
    Charlie: Shuf is fantastic. I tried it on a 78 billion line text file.
    ...


## Docs
 To generate messages you need some data chainchat can feed on. This data should associate text messages with users. Your message data should be a list of 2-tuples where the first position of each tuple corresponds to a user and the second position to the respective text. For the user you may use any hashable data type.
#### Data Example

    messages = [('Alice', 'Hey there!'),
                ('Bob', 'Hey, what's up?'),
                ('Charlie', 'Shuf is fantastic. I tried it on a 78 billion line text file.')]
              
#### Chat Example
Using your data you can instantiate a Chat instance as follows
	
    cc = chainchat.Chat(messages, finite = False, max_walk_length = 1000, enhance = True)
  

Using finite = True you also may generate finite interactions. Since Markov chains wouldn't consider the current 'interaction' this won't create more meaningful interactions than the infinite version.
The max_walk_length parameter specifies the maximum word count of generated messages. This is needed since Markov chains may generate arbitrarily long walks.
The enhance parameter specifies if saveable calculations should be kept. By saving once calculated matrices they won't have to be calculated again and may produce messages at an increased speed (especially with a low amount of users). Consider that the needed space increases with the amount of users and historical messages. On large datasets this may put a burden on your system.

#### Generator Example
Using the Chat object a message generator can be obtained. This generator yields a tuple of a user and a text message. This result is a single generated message. 

The first example generates two messages.

    >>> gen = cc.generate('Alice')
    >>> for _ in range(2):
            tpl = next(gen)
            print(": ".join(tpl))

Which leads to the following result.        

    Bob: Hey, what's up?
    Charlie: Shuf is fantastic. I tried it on a 78 billion line text file.
The following example generates an infinite number of messages.

    >>> for tpl in cc.generate('Alice')():
            print(": ".join(tpl))

With infinitely repeating output: 
        

    Bob: Hey, what's up?
    Charlie: Shuf is fantastic. I tried it on a 78 billion line text file.
    ...



