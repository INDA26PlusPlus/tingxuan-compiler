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

    # KEYWORD, VAR, NUM, CMP
    def program(self):
        # <program> ::= <action>*
        actions = []
        while True:
            kind, row, value = self.peek()
            if kind != 'EOF':
                actions.append(self.action())
            else:
                break
        return actions

    def action(self):
        # <action> ::= <let> | <assign> | <input> | <output> | <loop>
        kind, row, value = self.peek()
        if value == '!let':
            res = self.let()
        elif value == '!assign':
            res = self.assign()
        elif value == '!given':
            res = self.given()
        elif value == '!show':
            res = self.show()
        elif value == '!induct':
            res = self.loop()
        else:
            raise SyntaxError(f"error at row {row}: expected KEYWORD, found {value}")
        return res

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

    def loop(self):
        # <loop> ::= "!induct" (<var> | <num>) ("<" | ">" | "=") (<var> | <num>) <action>* "!qed"
        pass
        self.consume('KEYWORD','!induct')
        value1 = self.val_or_num()

        kind, row, value = self.peek()
        if value == '<':
            kind, row, value2 = self.consume('CMP','<')
        elif value == '>':
            kind, row, value2 = self.consume('CMP','>')
        elif value == '=':
            kind, row, value2 = self.consume('CMP','=')
        else:
            raise SyntaxError(f"error at row {row}, expected VAR or NUM, got {kind} '{value}'")

        value3 = self.val_or_num()
        actions = []
        while True:
            kind, row, value = self.peek()
            if value == '!qed':
                self.consume('KEYWORD','!qed')
                break
            else:
                actions.append(self.action())
    
        return ("INDUCT", value1, value2, value3, actions, "QED")

"""
print my cool tree!
[('GIVEN', 'n'), ('LET', 'a', '0'), ('LET', 'b', '1'), ('INDUCT', 'n', '>', '0', [('ASSIGN', 't', '!sum', 'a', 'b'), ('LET', 'a', 'b'), ('LET', 'b', 't'), ('ASSIGN', 'n', '!diff', 'n', '1')]), ('SHOW', 'a')]
"""
 
def print_tree(nodes, deep):
    for j in nodes:
        for k in range(len(j)):
            i = j[k]
            if isinstance(i, list):
                print()
                print_tree(i, deep+1)
            else:
                if k==0 or isinstance(j[k-1], list):
                    print("   "*(deep), end="")
                print(i, end=" ")
        print()

if __name__ == "__main__":
    #python3 main.py input.txt 
    if len(sys.argv) != 2:
        print("error: the format should be 'python3 main.py input.txt'")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    tree = Parse(lexer(lines)).program()
    print_tree(tree, 0)


# TODO: add comments to my language?