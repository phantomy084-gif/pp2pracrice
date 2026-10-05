n ,m =map(int,input().split())
m1 =0
m2 =0
if n < m or n == m:
    m1 = n
    m2 = m
else:
    m1 = m
    m2 = n

print(int(m2*(int(m1/2))+(m1%2)*(int(m2/2))))

    