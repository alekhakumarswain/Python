n=int(input("Enter A number : "))
for i in range(2,n):
    if(n%i==0):
        print("Not a Prime Number")
        break
    else:
        print("Prime Number")
        break