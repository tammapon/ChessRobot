import threading
from turtle import goto
 
 
def task1():
    # function to print cube of given num
    global x
    while True:
        x = input('x :')
 
 
def task2():
    # function to print square of given num
    global x
    print(x)
    x = 20
    
        
 
 
if __name__ =="__main__":
    # creating thread
    global x
    x=0
    print(x)
    x = input('x :')
    if x == 'xxx':
    # t1 = threading.Thread(target=task1)
        t2 = threading.Thread(target=task2)
 
    # starting thread 1
    # t1.start()
    # starting thread 2
        t2.start()
    
    t2.join()
    print(x)
 