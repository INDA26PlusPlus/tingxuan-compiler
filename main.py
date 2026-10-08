import sys

KEYWORD = ["!let", "!assign", "!given", "!show", "!sum", "!diff", "!induct", "!qed"]
CMP = ["<", ">", "="]

"""
scanning/lexing 
takes text/characters and put together to words/tokens
"""
def lexer(lines):
    row = 0            # so we know which row the token is at
    tokens = []         # stores the tokens
    # KEYWORD, VAR, NUM, CMP
    for line in lines:
        row+=1          # increase row on new row
        for word in line.split():
            if word in KEYWORD:
                tokens.append(("KEYWORD", row, word))
            elif word in CMP:
                tokens.append(("CMP", row, word))
            elif word.isdigit():
                tokens.append(("NUM", row, word))
            elif word.isalpha():
                tokens.append(("VAR", row, word))
            else:
                raise ValueError(f"unknown token {word} at row {row}")
    tokens.append(("EOF", row, ""))
    return tokens

"""
parsing
the syntax gets a grammar
takes tokens and builds a tree, show nested nature of grammar
"""
class Parse:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    #look at current token, it should be type expected, go to next
    def consume(self, kind, value=None):
        ckind, crow, cvalue = self.peek()
        if self.position<len(self.tokens) and ckind==kind and (cvalue==value or value==None):
            self.position+=1
            return self.tokens[self.position-1]
        else:
            raise SyntaxError(f"error at row {crow}: expected type and value ({kind}, {value}), got ({ckind},{cvalue})")

    def peek(self):
        return self.tokens[self.position]
    """
    <program> ::= <action>*
    <action> ::= <let> | <assign> | <input> | <output> | <loop>

    <loop> ::= "!induct" (<var> | <num>) ("<" | ">" | "=") (<var> | <num>) <action>* "!qed"
    """

    # KEYWORD, VAR, NUM, CMP
    # def program(self):
    #     if self.tokens[self.position]:
    #         if self.peek() in KEYWORD:
    #             pass

    # def action(self):
    #     pass

    # helper function to see if (<var> | <num>)
    def val_or_num(self):
        kind, row, value = self.peek()
        if kind == 'VAR':
            kind, row, value = self.consume('VAR')
        elif kind == 'NUM':
            kind, row, value = self.consume('NUM')
        else:
            raise SyntaxError(f"error at row {row}, expected VAR or NUM, got {kind} '{value}'")
        return value

    def let(self):
            # <let> ::= "!let" <var> (<num> | <var>)
            self.consume('KEYWORD','!let')
            kind, row, value1 = self.consume('VAR')
            value2 = self.val_or_num()
            return ("LET", value1, value2)
    
    def assign(self):
        # <assign> ::= "!assign" <var> ("!sum" | "!diff") (<var> | <num>) (<var> | <num>) 
        self.consume('KEYWORD','!assign')
        kind, row, value1 = self.consume('VAR')

        kind, row, value = self.peek()
        if value == '!sum':
            kind, row, keyword = self.consume('KEYWORD','!sum')
        elif value == '!diff':
            kind, row, keyword = self.consume('KEYWORD','!diff')
        else:
            raise SyntaxError(f"error at row {row}, expected !sum or !diff, got {value}")
        
        value2 = self.val_or_num()
        value3 = self.val_or_num()
        return ("ASSIGN", value1, keyword, value2, value3)

    def given(self):
        # <input> ::= "!given" <var>
        self.consume('KEYWORD','!given')
        kind, row, value = self.consume('VAR')
        return("GIVEN", value)

    def show(self):
        # <output> ::= "!show" (<var> | <num>)
        self.consume('KEYWORD','!show')
        value = self.val_or_num()
        return ("SHOW", value)

    

    

if __name__ == "__main__":
    #python3 main.py input.txt 
    if len(sys.argv) != 2:
        print("error: the format should be 'python3 main.py input.txt'")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    print(lexer(lines))


# TODO: add comments to my language?