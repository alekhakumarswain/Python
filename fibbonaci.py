f1=0
f2=1
print(f1)
print(f2)
n= int(input("Enter Number of fibbonaci u want : "))
for i in range(2,n):
    f=f1+f2
    print(f)
    f1=f2
    f2=f
    print(f)