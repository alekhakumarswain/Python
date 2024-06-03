f=1
a=int(input("Enter A Number : "))
if a<0:
    print("Factorial Can't Be Find")
elif a==0:
    print("Factorial of 0 is 1")
else:
    for i  in range(1,a+1):
        f = f*i
    print("The actorial of ",a,"is = ",f)
