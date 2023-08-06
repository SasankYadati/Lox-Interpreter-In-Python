from TokenType import TokenType
from Token import Token

class Scanner:
    def __init__(self, source:str, error_fn):
        self.source = source
        self.tokens : list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.error_fn = error_fn

    def scanTokens(self) -> "list[Token]":
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
               
    def isAtEnd(self):
        return self.current >= len(self.source)
    
    def scanToken(self):
        c = self.advance()
        if c == '(':
            self.addToken(TokenType.LEFT_PAREN)
        elif c == ')':
            self.addToken(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.addToken(TokenType.LEFT_BRACE)
        elif c == '}':
            self.addToken(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.addToken(TokenType.COMMA)
        elif c == '.':
            self.addToken(TokenType.DOT)
        elif c == '-':
            self.addToken(TokenType.MINUS)
        elif c == '+':
            self.addToken(TokenType.PLUS)
        elif c == ';':
            self.addToken(TokenType.SEMICOLON)
        elif c == '*':
            self.addToken(TokenType.STAR)
        elif c == '!':
            self.addToken(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            self.addToken(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<':
            self.addToken(TokenType.LESSER_EQUAL if self.match('=') else TokenType.LESSER)
        elif c == '>':
            self.addToken(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif c == '/':
            if self.match('/'): # single line comment
                while (self.peek() != '\n' and not self.isAtEnd()):
                    self.advance()
            elif self.match('*'): #multi line comment
                while not self.isAtEnd() and not (self.match('*') and self.match('/')):
                    self.advance()
            else:
                self.addToken(TokenType.SLASH)
        elif c in (' ', '\t', '\r'):
            return
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        else:
            if (Scanner.isDigit(c)):
                self.number()
            elif (Scanner.isAlpha(c)):
                self.identifier()
            else:
                self.error_fn(self.line, f"Unexpected char {c}")

    def match(self, expected):
        if self.isAtEnd(): return False
        if self.source[self.current] != expected: return False

        self.current += 1
        return True
    
    def string(self):
        while (self.peek() != '"' and not self.isAtEnd()):
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        
        if self.isAtEnd():
            self.error_fn(self.line, "Unterminated string.")
            return
        self.advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.addToken_(TokenType.STRING, value)

    def number(self):
        while Scanner.isDigit(self.peek()):
            self.advance()
        
        # look for fractions
        if self.peek() == '.' and Scanner.isDigit(self.peekNext()):
            self.advance() # consume the decimal point
        
            while Scanner.isDigit(self.peek()):
                self.advance()

        self.addToken_(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def identifier(self):
        while (Scanner.isAlphaNumeric(self.peek())):
            self.advance()
        lexeme = self.source[self.start : self.current]
        keywords = getKeyWords()
        if lexeme in keywords:
            self.addToken(keywords[lexeme])
        else:
            self.addToken(TokenType.IDENTIFIER)

    '''
    Returns char at current and increments current.
    '''
    def advance(self):
        self.current += 1
        return self.source[self.current - 1]
    
    '''
    Returns char at current.
    '''
    def peek(self):
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]

    '''
    Returns char at current + 1
    '''
    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return '\0'    
        return self.source[self.current + 1]
    
    def addToken(self, type: TokenType):
        self.addToken_(type, None)

    def addToken_(self, type: TokenType, literal):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    @staticmethod
    def isAlpha(c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c == '_')
    
    @staticmethod
    def isAlphaNumeric(c):
        return Scanner.isAlpha(c) or Scanner.isDigit(c)
    
    @staticmethod
    def isDigit(c):
        return c >= '0' and c <= '9'
    

def getKeyWords():
    KEYWORDS = dict()
    KEYWORDS["and"] = TokenType.AND
    KEYWORDS["class"] = TokenType.CLASS
    KEYWORDS["else"] = TokenType.ELSE
    KEYWORDS["false"] = TokenType.FALSE
    KEYWORDS["for"] = TokenType.FOR
    KEYWORDS["fun"] = TokenType.FUN
    KEYWORDS["if"] = TokenType.IF
    KEYWORDS["nul"] = TokenType.NIL
    KEYWORDS["or"] = TokenType.OR
    KEYWORDS["print"] = TokenType.PRINT
    KEYWORDS["return"] = TokenType.RETURN
    KEYWORDS["super"] = TokenType.SUPER
    KEYWORDS["this"] = TokenType.THIS
    KEYWORDS["true"] = TokenType.TRUE
    KEYWORDS["var"] = TokenType.VAR
    KEYWORDS["while"] = TokenType.WHILE
    return KEYWORDS

        
