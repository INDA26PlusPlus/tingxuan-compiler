n = int(input())-1
dp = [-1]*(n+1)
def fib(n):
    if n < 2:
        return 1
    if dp[n-1] != -1:
        a = dp[n-1]
    else:
        a = fib(n-1)
    if dp[n-2] != -1:
        b = dp[n-2]
    else:
        b = fib(n-2)

    dp[n] = a+b
    return dp[n]

print(fib(n))