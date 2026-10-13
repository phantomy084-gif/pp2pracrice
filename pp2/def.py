n=int(input())
n1=list(map(int,input().split()))
m=10000
for i in range(n):
    if n1[i]<m and n1[i]>0:
        m=n1[i]
if m==10000:
    print(-1)
else:
    print(m)