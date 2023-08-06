import sys
from TokenType import TokenType
from Scanner import Scanner
from Static import Static

class Lox(Static):
    hadError = False
    @staticmethod
    def runLox():
        args = sys.argv
        if len(args) > 2:
            print("Usage: python Lox.py [script]")
            sys.exit(64)
        elif len(args) == 2:
            Lox.runFile(args[1])
        else:
            Lox.runPrompt()

    @staticmethod
    def runFile(fileName):
        with open(fileName, "r") as f:
            source = f.read()
            Lox.run(source)

            if (Lox.hadError):
                sys.exit(65)

    @staticmethod
    def runPrompt():
        while True:
            line = input("> ")
            if (line == "^Z"): break
            Lox.run(line)
            Lox.hadError = False

    @staticmethod
    def run(src: str) -> None:
        scanner = Scanner(src, Lox.error)
        tokens:list[TokenType] = scanner.scanTokens()

        for token in tokens:
            print(token)

    @staticmethod
    def error(line: int, message: str) -> None:
        Lox.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}")
        Lox.hadError = True

if __name__ == '__main__':
    Lox.runLox()