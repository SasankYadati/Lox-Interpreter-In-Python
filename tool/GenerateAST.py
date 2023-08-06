import sys
from Static import Static

class GenerateAst(Static):
    indent = "   " # tab
    @staticmethod
    def run():
        args = sys.argv
        if len(args) != 2:
            print("Usage: python GenerateAST.py [script]")
            sys.exit(64)
        outputDir = args[1]
        GenerateAst.defineAst(outputDir, "Expr", [
           "Binary   : Expr left, Token operator, Expr right",
           "Grouping : Expr expression",
           "Literal  : Object value",
           "Unary    : Token operator, Expr right"
        ])

    @staticmethod
    def defineAst(outputDir, baseName, types):
       path = f"{outputDir}/{baseName}.py"
       with open(path, 'w+') as f:
          f.write(f"class {baseName}:")
          for t in types:
             className = t.split(":")[0].strip()
             fields = t.split(":")[1].strip()
             GenerateAst.defineType(f, baseName, className, fields)

    @staticmethod
    def defineType(f, baseName, className, fields):
       f.write

if __name__ == '__main__':
    GenerateAst.run()