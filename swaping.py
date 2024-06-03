#swapping of two variable without 3rd variable
a=int(input("Enter A Number : "))
b=int(input("Enter A Number : "))
print("before swapping a=",a,"b=",b)

a,b=b,a

print("after swapping a=",a,"b=",b)


#swapping of two variable without 3rd variable
a=int(input("Enter A Number : "))
b=int(input("Enter A Number : "))
print("before swapping a=",a,"b=",b)

a=a+b
b=a-b
a=a-b
print("after swapping a=",a,"b=",b)


#swapping of two variable useing 3rd variable
a=int(input("Enter A Number : "))
b=int(input("Enter A Number : "))
print("before swapping a=",a,"b=",b)   
c=a
a=b
b=c

print("after swapping a=",a,"b=",b)