n = int(input())
a = 0
b = 1
while n > 0:
    t = a + b
    a = b
    b = t
    n = n - 1

print(a)