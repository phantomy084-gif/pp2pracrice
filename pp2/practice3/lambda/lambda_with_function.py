def my_func(n):
    return lambda a: a * n
ans = my_func(5)
print(ans(3))