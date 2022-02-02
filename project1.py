# author Mackenzie Myers
# CMPSC 461 Project 1
# simplified HTML lexer / parser 

STRING, KEYWORD, EOI, INVALID = 1, 2, 3, 4

def typeToString (tp):
    if (tp == STRING): return "String"
    elif (tp == KEYWORD): return "Keyword"
    elif (tp == EOI): return "EOI"
    return "Invalid"

class Token:
    "A class for representing Tokens"

    # a Token object has two fields: the token's type and its value
    def __init__ (self, tokenType, tokenVal):
        self.type = tokenType
        self.val = tokenVal

    def getTokenType(self):
        return self.type

    def getTokenValue(self):
        return self.val

    def __repr__(self):
        if (self.type == STRING): 
            return self.val
        elif (self.type == KEYWORD):
            return self.val
        elif (self.type == EOI):
            return ""
        else:
            return "invalid"

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
KEYWORDS = ["<body>", "</body>", "<b>", "</b>", "<i>", "</i>", "<ul>", "</ul>", "<li>", "</li>"]

class Lexer:

    # stmt is the current statement to perform the lexing;
    # index is the index of the next char in the statement
    def __init__ (self, s):
        self.stmt = s
        self.index = 0
        self.nextChar()

    def nextToken(self):
        while True:
            if self.ch.isalpha(): # is a letter
                id = self.consumeChars(LETTERS+DIGITS)
                return Token(STRING, id)
            elif self.ch.isdigit():
                num = self.consumeChars(LETTERS+DIGITS)
                return Token(STRING, id)
            elif self.ch==' ': self.nextChar()
            elif self.ch=='<': 
                self.nextChar()
                id = self.consumeChars(LETTERS)
                keyword = "<" + id + ">"
                # print("char: " + self.ch)
                # print("keyword: " + str(keyword))
                if self.checkChar(">"):
                    if keyword in KEYWORDS:
                        return Token(KEYWORD, "<" + id + ">")
                return Token(INVALID, self.ch)
            elif self.index >= len(self.stmt) or self.ch == "$":
                return Token(EOI, "$")
            else:
                self.nextChar()
                return Token(INVALID, self.ch)

    def nextChar(self):
        # print("index: " + str(self.index))
        if self.index >= (len(self.stmt)):
            self.ch = "$"
        else: 
            self.ch = self.stmt[self.index] 
            self.index = self.index + 1

    def consumeChars (self, charSet):
        r = self.ch
        self.nextChar()
        while (self.ch in charSet):
            r = r + self.ch
            self.nextChar()
        return r

    def checkChar(self, c):
        if (self.ch==c):
            self.nextChar()
            return True
        else: return False

import sys


class Parser:
    def __init__(self, s):
        self.lexer = Lexer(s+"$")
        self.token = self.lexer.nextToken()
        self.indent = ""

    def check (self, stri):
        val = self.token.getTokenValue()
        if (val == stri):
            return True
        else: 
            return False
    
    def error(self, tp):
        print ("Syntax error: expecting: " + str(tp) \
               + "; saw: " + self.token.getTokenValue())
        sys.exit(1)

    def run(self):
        while not self.check("$"):
            if self.check("<body>"):
                self.webpage()
            elif self.check("<b>") or self.check("<i>") or self.check("<ul>") or self.token.getTokenType() == STRING:
                self.text()
            elif self.check("<li>"):
                self.listitem()


    def webpage(self):
        print(self.indent + self.token.getTokenValue())
        self.token = self.lexer.nextToken()
        self.indent = self.indent + "  "

        self.text()

        if self.check("</body>"):
            self.indent = self.indent[0:-2]
            print(self.indent + self.token.getTokenValue())
            self.token = self.lexer.nextToken()
            
        else:
            self.error("</body>")

    def text(self):
        # the while loop allows it to keep repeating checking for text - represents the {} in the grammar
        while self.check("<b>") or self.check("<i>") or self.check("<ul>") or self.token.getTokenType() == STRING:
            if self.token.getTokenType() == STRING:
                while self.token.getTokenType() == STRING:
                    print(self.indent + self.token.getTokenValue())
                    self.token = self.lexer.nextToken()

            elif self.check("<b>"):
                print(self.indent + self.token.getTokenValue())
                self.indent = self.indent + "  "
                self.token = self.lexer.nextToken()

                self.text() #recursively call text() 

                if self.check("</b>"):
                    self.indent = self.indent[0:-2]
                    print(self.indent + self.token.getTokenValue())
                    self.token = self.lexer.nextToken()
                else:
                    self.error("</b>")
                
            elif self.check("<i>"):
                print(self.indent + self.token.getTokenValue())
                self.indent = self.indent + "  "
                self.token = self.lexer.nextToken()

                self.text()

                if self.check("</i>"):
                    self.indent = self.indent[0:-2]
                    print(self.indent + self.token.getTokenValue())
                    self.token = self.lexer.nextToken()
                else:
                    self.error("</i>")

            elif self.check("<ul>"):
                print(self.indent + self.token.getTokenValue())
                self.indent = self.indent + "  "
                self.token = self.lexer.nextToken()

                if not self.check("<li>"):
                    self.error("<li>")
                else:
                    while self.check("<li>"):
                        self.listitem()

                if self.check("</ul>"):
                    self.indent = self.indent[0:-2]
                    print(self.indent + self.token.getTokenValue())
                    self.token = self.lexer.nextToken()
                else:
                    self.error("</ul>")

    def listitem(self):
        print(self.indent + self.token.getTokenValue())
        self.indent = self.indent + "  "
        self.token = self.lexer.nextToken()

        self.text()

        if self.check("</li>"):
            self.indent = self.indent[0:-2]
            print(self.indent + self.token.getTokenValue())
            self.token = self.lexer.nextToken()
        else:
            self.error("</li>")


# print("Testing the lexer: test 1")
# lex = Lexer("string")
# tk = lex.nextToken()
# while (tk.getTokenType() != EOI):
#     print(tk)
#     tk = lex.nextToken()
# print("")

# print("Testing the lexer: test 2")
# lex = Lexer ("<b> hello </b>")
# tk = lex.nextToken()
# while (tk.getTokenType() != EOI):
#     print(tk)
#     tk = lex.nextToken()
# print("")

# print("Testing the lexer: test 3")
# lex = Lexer("<body> google <b><i><b> yahoo</b></i></b></body>")
# tk = lex.nextToken()
# while (tk.getTokenType() != EOI):
#     print(tk)
#     tk = lex.nextToken()
# print("")

####################
### PARSER TESTS ###
####################
# parser = Parser("<body> dog <ul> <li> hi </li> </ul> </body>")
# parser.run()
# PASSED 

# parser = Parser("<body> <b> purple </b> <ul> <li> hi </li> </ul> </body>")
# parser.run()
# PASSED 

# parser = Parser("<body> dog <ul> <li> hi </li> </ul> ")
# parser.run()
# PASSED

# parser = Parser("<i> hello there </i> <ul> we are </ul>")
# parser.run()
# PASSED: THIS SHOULD RAISE AN ERROR BECAUSE WHEN <UL> IS USED <LI> MUST COME RIGHT AFTER IT 

# parser = Parser("<body> <ul> <li> apple </li> <li> windows </li> </body>")
# parser.run()
# PASSED 

# parser = Parser("<body> <ul> <li> apple </li> <li> windows </li> </ul> </body>")
# parser.run()
# PASSED: CAN DO MULTIPLE LI'S IN THE UL ! 