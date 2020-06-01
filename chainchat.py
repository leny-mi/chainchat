"""A markov chains based module to quickly generate chat messages.

Use the Chat class to start generating messages.

Examples:
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

"""

import pykov
from typing import Any, Tuple, List, Generator

class Chat:
    """A markov chains based class to quickly generate chat messages.

    Use the initialization method to enter the data chat messages should be based on. For generation different user objects (may be strings) and their messages are needed.

    Examples:
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

    """

    word_matrices = {}

    def __init__(self, messages: List[Tuple[Any, str]], finite = False, max_walk_length: int = 100, enhance: bool = True):
        """Create a Chat object based on historical messages.

        Args:
            messages: List of tuples of sender and message. Sender may be of any type and may not be None. Messages should be in chronological order; otherwise results may be worse.
            max_walk_length: Limit on number of words in a generated message
            enhance: If set to true, repeated message generation for the same user may be faster at the cost of space. When dealing with a large amount of users on a system without much space this should be set to False

        Examples:
            >>> messages = [('Alice', 'Hey there!'),
                        ('Bob', 'Hey, what's up?'),
                        ('Charlie', 'Shuf is fantastic. I tried it on a 78 billion line text file.')]

            >>> cc = chainchat.Chat(messages, max_walk_length = 1000, enhance = True)

        """
        self.MAX_WALK_LENGTH = max_walk_length
        self.messages = messages
        self.Musers = pykov.Matrix()
        self.enhance_speed = enhance
        for mes, nxt in zip(messages[:-1], messages[1:]):
            assert(mes is not None)
            assert(nxt is not None)
            if (mes[0], nxt[0]) not in self.Musers: self.Musers[(mes[0], nxt[0])] = 0
            self.Musers[(mes[0], nxt[0])] = self.Musers[(mes[0], nxt[0])] + 1
        if finite: self.Musers[(messages[-1][0], None)] = 1
        elif self.Musers.succ(key=messages[-1][0]).sum() == 0: self.Musers[(messages[-1][0], messages[0][0])] = 1
        self.Musers.stochastic()

    def generate(self, head : Any = None) -> Generator[Tuple[Any, str], None, None] :
        """Return a generator that yields a new message on every next call.

        Args:
            head: User to start the interaction with. If no user supplied, the sender of the earliest message is used. Note, this user will not send a message but will be the user the first generated message responds to.

        Examples:
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
        """
        user = pykov.Vector({self.messages[0][0] if head is None else head:1}) # starting point for markov chain
        while True:
            choice = (user * self.Musers).choose() # choose next user to write a message
            if choice is None: return
            user = pykov.Vector({choice: 1}) # create pykov vector for future user calculation
            if choice in self.word_matrices:
                Mword = self.word_matrices[choice]
            else: # create word matrix
                Mword = pykov.Matrix({(1, 1) : 1}) # create matrix for word chain
                for mes in [m for m in self.messages if m[0] == choice]: # add every word to matrix
                    splt = mes[1].split(' ')
                    if (0, splt[0]) not in Mword: Mword[(0, splt[0])] = 0
                    Mword[(0, splt[0])] += 1
                    for word, nxt in zip(splt[:-1], splt[1:]):
                        if (word, nxt) not in Mword: Mword[(word, nxt)] = 0
                        Mword[(word, nxt)] += 1
                    if (splt[-1], 1) not in Mword: Mword[(splt[-1], 1)] = 0
                    Mword[(splt[-1], 1)] += 1
                Mword.stochastic()
                if not self.enhance_speed: self.word_matrices[choice] = Mword

            C = pykov.Chain(Mword)
            yield (choice, " ".join(C.walk(self.MAX_WALK_LENGTH, 0, 1)[1:-1]))
