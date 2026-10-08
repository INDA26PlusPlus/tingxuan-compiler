# mathon

welcome to the really! cool! programming language **mathon** \
(example file: fib.ma)

## what can this language do?
well... it can calculate fibonacci! (i hope)
it can also take input, output, create variables and those stuff... \
a list of everything is in the grammar, but i will also list it here: 

### define a variable:
py: `b = 1`\
ma: `!let b 1`\
(variable names are a-z and A-Z)

### calculate add or subtract variable:
py: `b = b + 5`\
ma: `!assign b !sum b 5`

py: `a = 4 - 2`\
ma: `!assign a !diff 4 2`

### loop
py: `while n > 0`\
ma: `!induct n > 0`\
and end loop with: `!qed`

### input
py: `a = input()`\
ma: `!given a`

### output
py: `print(a)`\
ma: `!show a`

* as you notice, all statements starts with ! followed by, give/show/induct/assign/let
* everything has to be seperated with spaces

## how does the compiler work?
the lexer and parser are in main.py\
run: `python3 main.py fib.ma`
and it will print out your tree! which basically looks like your code

### example
input
```
!given n
!let a 0
!let b 1
!induct n > 0
    !assign t !sum a b
    !let a b
    !let b t
    !assign n !diff n 1
!qed

!show a
```
output
```
GIVEN n
LET a 0
LET b 1
INDUCT n > 0
   ASSIGN t !sum a b
   LET a b
   LET b t
   ASSIGN n !diff n 1
QED
SHOW a
```