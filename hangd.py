import random

from twisted.application import service, internet
from twisted.internet import protocol, reactor
from twisted.protocols import basic

class Hangman():
    def __init__(self):
        self.newgame         = True
        self.solved          = False
        self.guesses         = 20
        self.word            = self.getWord()
        self.board           = self.getInitialBoard()  
        self.bit_bucket      = list()
        self.correct_guesses = list()

    def getWord(self):
        w = open('words')        
        return list(random.choice(w.readlines()).strip())

    def getInitialBoard(self):
        board = list()
        for i in self.word:
            if i in ['-', " "]:
                board.append(i)
            else:
                board.append("_")
           
        return board

    def updateBoard(self, line):
        if (line in self.word):
            self.correct_guesses.append(line)
        else:
            self.bit_bucket.append(line)
            
        for i,j in enumerate(self.word):
            if j == line:
                self.board[i] = j

        if self.board == self.word:
            self.solved = True

        return self.board

    def mkstr(self, alist):
        return "".join(alist)

    def sendHelp(self):
        return "Guess a letter"

    def play(self, line):
        retval = self.board
        
        if len(line) != 1:
            retval = "Send one letter and one letter only.  Sheesh."
        else:
            if self.newgame:
                self.guesses = self.guesses - 1
                self.updateBoard(line)
                self.newgame = False
                retval = self.board
            else:
                self.guesses = self.guesses - 1
                self.updateBoard(line)
                retval = self.board

        return retval

class HangProtocol(basic.LineReceiver):    
    def __init__(self):
        self.hangman = Hangman()

    def lineReceived(self, line):
        line = line.lower().strip()
        if line == "help":
            self.sendLine(self.hangman.sendHelp())
        elif line == "quit":
            self.transport.loseConnection()
        else:
            self.sendLine(self.hangman.mkstr(self.hangman.play(line)))
            if self.hangman.solved:
                self.sendLine("WINNAH WINNAH CHICKEN DINNAH!!!!!!!!!!!!!!!!!")
                self.transport.loseConnection()
            elif self.hangman.guesses == 0:
                self.sendLine("Ouch.  Sucks.")
                self.transport.loseConnection()
            else:
                self.sendLine("\nNumber of guesses remaining: " + 
                              str(self.hangman.guesses))


class HangFactory(protocol.ServerFactory):
    protocol = HangProtocol

class HangService(internet.TCPServer):
    def __init__(self):
        internet.TCPServer.__init__(self, 2323, HangFactory())
