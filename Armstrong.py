number =int(input('Enter A Number : '))
temp=number
sum = 0
order=len(str(number))
while(number>0):
    digit = number % 10
    sum+=digit**order
    number=number//10
if(sum==number):
    print(temp,'is an Amstrong Number')
else:
    print(temp,'is not an Amstrong Number')
