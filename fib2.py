n = int(input())
a = 0
b = 1
while n > 0:
    t = a + b
    a = b
    b = t
    n = n - 1

print(a)

"""
mathon
.ma

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
"""