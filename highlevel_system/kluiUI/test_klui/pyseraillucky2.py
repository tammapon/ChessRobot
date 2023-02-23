from asyncio import protocols
import keyboard
import serial
import time
import math
port = 'COM4'
port2 = 'COM5'
baudrate = 115200
robotconnect = False
gripperconnect = False
try:
    serialPort = serial.Serial(port=port, baudrate=baudrate,
                                    bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE)
    robotconnect = True
except:
    robotconnect = False
try:
    serialPort2 = serial.Serial(port=port2, baudrate=baudrate,
                                 timeout=1, stopbits=serial.STOPBITS_ONE)
    gripperconnect = True
except:
    gripperconnect = False
serialString = ""
chessboardDEG = 0
chessboard = []

chess_board_position = [[[175,175],[175,125],[175,75],[175,25],[175,-25],[175,-75],[175,-125],[175,-175]],
                        [[125,175],[125,125],[125,75],[125,25],[125,-25],[125,-75],[125,-125],[125,-175]],
                        [[75,175],[75,125],[75,75],[75,25],[75,-25],[75,-75],[75,-125],[75,-175]],
                        [[25,175],[25,125],[25,75],[25,25],[25,-25],[25,-75],[25,-125],[25,-175]],
                        [[-25,175],[-25,125],[-25,75],[-25,25],[-25,-25],[-25,-75],[-25,-125],[-25,-175]],
                        [[-75,175],[-75,125],[-75,75],[-75,25],[-75,-25],[-75,-75],[-75,-125],[-75,-175]],
                        [[-125,175],[-125,125],[-125,75],[-125,25],[-125,-25],[-125,-75],[-125,-125],[-125,-175]],
                        [[-175,175],[-175,125],[-175,75],[-175,25],[-175,-25],[-175,-75],[-175,-125],[-175,-175]]]
rz=0
x=0
y=0
z=0

def get_chess_board_position2(X,N,angle):
    angle_rad = math.radians(angle)
    L=400
    l=295
    s=math.sin(angle_rad)
    # print(s)
    c=math.cos(angle_rad)
    # print(c)
    A=(L*X/8)-(9*L/16)
    B=(L*N/8)-(9*L/16)
    x=(s*A) + (c*B) + l + (L/2)
    y=-(c*A) + (s*B)
    if X==1:
        return [x,y+8]
    else:
        return [x,y]

def get_chess_board_position(y_box_now,x_box_now,y_box_go,x_box_go,angle):
    pos1=get_chess_board_position2(x_box_now+1,8-y_box_now,angle)
    pos2=get_chess_board_position2(x_box_go+1,8-y_box_go,angle)
    return [pos1[0],pos1[1],pos2[0],pos2[1]]

def CheckSumCal(sum):
    out = sum%256
    return out

def acknowledge():
    arr = []
    # wait = 0
    arr = serialPort.read(4)
    # if arr != None:
    #     wait = 1
    # print('1')
    while arr == bytearray():
        arr = serialPort.read(4)
        # print(arr)
    if len(arr)>0:
        print('arr',arr[0],arr[1],arr[2],arr[3])
        if(arr[0] == 255):
            if(arr[1] == 1):
                print('jog')
                if(arr[2] == 1):
                    if(arr[3] == 1):
                        print('time',time.time())
                    else:
                        print('error')
                        arr = []
                else:
                    print('error')
                    arr = []
            else:
                print('error')
                arr = []
        else:
            print('error')
            arr = []
        arr = []
    else:
        arr = []

def jogProtocol(Instruction):
    a = [255,1,1,0,0,0,0,0,0,0,Instruction]
    sum=0
    for i in a[1:]:
        sum = sum+i
    ck = CheckSumCal(sum)
    a.append(ck)
    serialPort.write(a)

def sethomeProtocol():
    a = [255,1,5,0,0,0,0,0,0,0,0]
    sum=0
    for i in a[1:]:
        sum = sum+i
    ck = CheckSumCal(sum)
    a.append(ck)
    serialPort.write(a)
def event():
    text = str(keyboard.read_event())[-2]
    if text == 'p':
        print('z')
        jogProtocol(255)
        acknowledge()
def KeyPressSerial():
    while True:
        if keyboard.is_pressed('r'): #j1+
            print('r')
            jogProtocol(5)
            acknowledge()
            event()
        elif keyboard.is_pressed('f'): #j1-
            print('f')
            jogProtocol(6)
            acknowledge()
            event()
        elif keyboard.is_pressed('t'): #j2+
            print('t')
            jogProtocol(7)
            acknowledge()
            event()
        elif keyboard.is_pressed('g'): #j2-
            print('g')
            jogProtocol(8)
            acknowledge()
            event()
        elif keyboard.is_pressed('y'): #j3+
            print('y')
            jogProtocol(9)
            acknowledge()
            event()
        elif keyboard.is_pressed('h'): #j3-
            print('h')
            jogProtocol(10)
            acknowledge()
            event()
        elif keyboard.is_pressed('u'): #j4+
            print('u')
            jogProtocol(11)
            acknowledge()
            event()
        elif keyboard.is_pressed('j'): #j4-
            print('j')
            jogProtocol(12)
            acknowledge()
            event()
        elif keyboard.is_pressed('w'): #x+
            print('w')
            jogProtocol(1)
            acknowledge()
            event()
        elif keyboard.is_pressed('s'): #x-
            print('s')
            jogProtocol(2)
            acknowledge()
            event()
        elif keyboard.is_pressed('a'): #y+
            print('a')
            jogProtocol(3)
            acknowledge()
            event() 
        elif keyboard.is_pressed('d'): #y-
            print('d')
            jogProtocol(4)
            acknowledge()
            event()
        elif keyboard.is_pressed('p'): #y-
            print('p')
        elif keyboard.is_pressed('o'): #70
            print('break')
            break
        # event()
        # print(serialPort.in_waiting)
        # while(serialPort.in_waiting):
        #     print(serialPort.in_waiting)
        #     pass    
        # acknowledge()
def to2byte(x):
    x2h = (x>>8) & 0xFF
    x2l = x & 0xFF
    return [x2h,x2l]

def to_position_task(rz,x,y,z): #(rad,mm,mm,mm) #rz*1000,xyz*10000
    a = [255,1,2]
    a = a+to2byte(rz)+to2byte(x)+to2byte(y)+to2byte(z)
    sum=0
    for i in a[1:]:
        sum = sum+i
    # print(sum)
    ck = CheckSumCal(sum)
    a.append(ck)
    print(a)
    serialPort.write(a)

def to_position_joint(j1,j2,j3,j4): #(rad) #*1000
    a = [255,1,3]
    a = a+to2byte(j1)+to2byte(j2)+to2byte(j3)+to2byte(j4)
    sum=0
    for i in a[1:]:
        sum = sum+i
    # print(sum)
    ck = CheckSumCal(sum)
    a.append(ck)
    print(a)
    serialPort.write(a)

def to_position_z(z): #(mm) #rz*1000,xyz*10000
    a = [255,1,7,0,0,0,0,0,0]
    a = a+to2byte(z)
    sum=0
    for i in a[1:]:
        sum = sum+i
    # print(sum)
    ck = CheckSumCal(sum)
    a.append(ck)
    print(a)
    serialPort.write(a)

def GripperProtocol(Instruction): #1 close 0 open
    # a = [255,1,6,0,0,0,0,0,0,0,Instruction]
    # sum=0
    # for i in a[1:]:
    #     sum = sum+i
    # ck = CheckSumCal(sum)
    # a.append(ck)
    # serialPort.write(a)
    if Instruction==1:
        print('B')
        serialPort2.write(bytes('A','utf-8'))
    else:
        print('C')
        serialPort2.write(bytes('B','utf-8'))
    time.sleep(0.05)
    arr = []
    arr = serialPort2.read(1)
    print(arr)
    # while arr == bytearray():
    #     arr = serialPort2.read(1)
    #     print(arr)
def move_chess_1(box_now,box_go) :
    chess_start = box_now
    chess_final = box_go
    # enc()
    print(int(chess_start[0]),int(chess_start[1]),int(chess_final[0]),int(chess_final[1]))
    pos = get_chess_board_position(int(chess_start[0]),int(chess_start[1]),int(chess_final[0]),int(chess_final[1]),0)
    print(pos)
    #1
    to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(300*10))
    acknowledge()
    #2
    to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(200*10))
    acknowledge()
    #3 gripper close
    GripperProtocol(1)
    #4
    to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(300*10))
    acknowledge()
    #5
    to_position_task(0,int(pos[2]*10),int((pos[3])*10),int(300*10))
    acknowledge()
    #6
    to_position_task(0,int(pos[2]*10),int(pos[3]*10),int(200*10))
    acknowledge()
    #7 gripper open
    GripperProtocol(0)
    #8
    to_position_task(0,int(pos[2]*10),int(pos[3]*10),int(300*10))
    acknowledge()
    #9
    sethomeProtocol()
    acknowledge()

def move_chess_2(box_now,box_go,status) :
    chess_start = box_now
    chess_final = box_go
    # enc()
    chess_mode = status
    print(int(chess_start[0]),int(chess_start[1]),int(chess_final[0]),int(chess_final[1]))
    pos = get_chess_board_position(int(chess_start[0]),int(chess_start[1]),int(chess_final[0]),int(chess_final[1]),0)
    print(pos)
    if chess_mode == False :
        #1
        to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(300*10))
        acknowledge()
        #2
        to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(200*10))
        acknowledge()
        #3 gripper close
        GripperProtocol(1)
        #4
        to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(300*10))
        acknowledge()
        #5
        to_position_task(0,int(pos[2]*10),int((pos[3])*10),int(300*10))
        acknowledge()
        #6
        to_position_task(0,int(pos[2]*10),int(pos[3]*10),int(200*10))
        acknowledge()
        #7 gripper open
        GripperProtocol(0)
        #8
        to_position_task(0,int(pos[2]*10),int(pos[3]*10),int(300*10))
        acknowledge()
        #9
        sethomeProtocol()
        acknowledge()
    elif chess_mode == True:
        #1
        to_position_task(0,int(pos[2]*10),int((pos[3])*10),int(300*10))
        acknowledge()
        #2
        to_position_task(0,int(pos[2]*10),int(pos[3]*10),int(200*10))
        acknowledge()
        #3 gripper close
        GripperProtocol(1)
        #4
        to_position_task(0,int(pos[2]*10),int((pos[3])*10),int(300*10))
        acknowledge()
        #5
        to_position_task(0,int(350*10),int(-485*10),int(300*10))
        acknowledge()
        #6 gripper open
        GripperProtocol(0)
        # enc()
        #1
        to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(300*10))
        acknowledge()
        #2
        to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(200*10))
        acknowledge()
        #3 gripper close
        GripperProtocol(1)
        #4
        to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(300*10))
        acknowledge()
        #5
        to_position_task(0,int(pos[2]*10),int((pos[3])*10),int(300*10))
        acknowledge()
        #6
        to_position_task(0,int(pos[2]*10),int(pos[3]*10),int(200*10))
        acknowledge()
        #7 gripper open
        GripperProtocol(0)
        #8
        to_position_task(0,int(pos[2]*10),int(pos[3]*10),int(300*10))
        acknowledge()
        #9
        sethomeProtocol()
        acknowledge()
# def enc():
#     serialPort2.write(bytes('A','utf-8'))
#     time.sleep(0.05)
#     arr = []
#     arr = serialPort2.read(3)
#     # print(arr)
#     while arr == bytearray():
#         arr = serialPort2.read(3)
#         # print(arr)
#     print(int(arr))
#     chessboardDEG = int(arr)+1
#     real_DEG = chessboardDEG-chessboardDEG_old
#     if(real_DEG<-180):
#         real_DEG=360+real_DEG
#     elif(real_DEG>180):
#         real_DEG=real_DEG-360
#     real_DEG=-real_DEG
#     print('real =',real_DEG)
    
# while True:
#     KeyPressSerial()
#     # acknowledge()
#     # time.sleep(0.1)
#     # serialPort.reset_input_buffer()
#     # serialPort.reset_output_buffer()
#     # serialString = serialPort.read().hex()
#     # serialString = serialPort.read()
#     # print(serialString)
#     # if serialString != "":
#         # print(serialString)
#         # break
# key=0
# while True:
#     if key == 0:
#         key = input('input mode: ')
#     elif key == 'jog':
#         KeyPressSerial()
#         # test=acknowledge()
#         # while test==None:
#         #     test=acknowledge()
#         key = 0
#     elif key == 'sethome': #j1=-1.57 j2=0 j3=2.35 j4=0
#         sethomeProtocol()
#         acknowledge()
#         key = 0
#     elif key == 'topos':
#         rz = input('rz: ')
#         x = input('x: ')
#         y = input('y: ')
#         z = input('z: ')
#         to_position_task(int(float(rz)*1000),int(float(x)*10),int(float(y)*10),int(float(z)*10))
#         acknowledge()
#         key = 0
#     elif key == 'tojoint': #radian
#         j1 = input('j1: ')
#         j2 = input('j2: ')
#         j3 = input('j3: ')
#         j4 = input('j4: ')
#         to_position_joint(int(float(j1)*1000),int(float(j2)*100),int(float(j3)*1000),int(float(j4)*1000))
#         acknowledge()
#         key = 0
#     elif key == 'toz':
#         z = input('z: ')
#         to_position_z(int(float(z)*10))
#         acknowledge()
#         key = 0
#     elif key == 'griper':
#         mode = input('Grip0/1 : ')
#         GripperProtocol(int(mode))
#         # acknowledge()
#         key = 0
#     elif key == 'encoder0':
#         # chessboardDEG_old = chessboardDEG
#         serialPort2.write(bytes('A','utf-8'))
#         time.sleep(0.05)
#         arr = []
#         arr = serialPort2.read(3)
#         # print(arr)
#         while arr == bytearray():
#             arr = serialPort2.read(3)
#             # print(arr)
#         print(int(arr))
#         chessboardDEG_old = int(arr)+1
#         key=0
#     elif key == 'encoder1':
#         # chessboardDEG_old = chessboardDEG
#         serialPort2.write(bytes('A','utf-8'))
#         time.sleep(0.05)
#         arr = []
#         arr = serialPort2.read(3)
#         # print(arr)
#         while arr == bytearray():
#             arr = serialPort2.read(3)
#             # print(arr)
#         print(int(arr))
#         chessboardDEG = int(arr)+1
#         real_DEG = chessboardDEG-chessboardDEG_old
#         if(real_DEG<-180):
#             real_DEG=360+real_DEG
#         elif(real_DEG>180):
#             real_DEG=real_DEG-360
#         real_DEG=-real_DEG
#         print('real =',real_DEG)
#         key = 0
#     elif key == 'encoder':
#         # chessboardDEG_old = chessboardDEG
#         serialPort2.write(bytes('A','utf-8'))
#         time.sleep(0.05)
#         arr = []
#         arr = serialPort2.read(3)
#         # print(arr)
#         while arr == bytearray():
#             arr = serialPort2.read(3)
#             # print(arr)
#         print(int(arr))
#         chessboardDEG_old = int(arr)+1
#         waitting = 'n'
#         while waitting!='Y' and waitting!='y':
#             waitting = input('start(Y/n):')
#             print(waitting)
#         serialPort2.write(bytes('A','utf-8'))
#         time.sleep(0.05)
#         arr = []
#         arr = serialPort2.read(3)
#         # print(arr)
#         while arr == bytearray():
#             arr = serialPort2.read(3)
#             # print(arr)
#         print(int(arr))
#         chessboardDEG = int(arr)+1
#         real_DEG = chessboardDEG-chessboardDEG_old
#         if(real_DEG<-180):
#             real_DEG=360+real_DEG
#         elif(real_DEG>180):
#             real_DEG=real_DEG-360
#         print('real =',real_DEG)
#         key = 0
#     elif key == 'calibrate':
#         calibrateX=495
#         to_position_task(0,int(calibrateX*10),int(0*10),int(200*10))
#         acknowledge()
#         key=0
#     elif key == 'tochess':
#         chess_start = input('chess_start: ')
#         chess_final = input('chess_final: ')
#         real_DEG=0
#         print(int(chess_start[0]),int(chess_start[1]),int(chess_final[0]),int(chess_final[1]))
#         pos = get_chess_board_position(int(chess_start[0]),int(chess_start[1]),int(chess_final[0]),int(chess_final[1]),real_DEG)
#         print(pos)
#         st = 'n'
#         while st!='Y' and st!='y':
#             st = input('start(Y/n):')
#             print(st)
#         # enc()
#         #1
#         to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(300*10))
#         acknowledge()
#         #2
#         to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(192*10))
#         acknowledge()
#         #3 gripper close
#         GripperProtocol(1)
#         #4
#         to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(300*10))
#         acknowledge()
#         #5
#         to_position_task(0,int(pos[2]*10),int((pos[3]-1)*10),int(300*10))
#         acknowledge()
#         #6
#         to_position_task(0,int(pos[2]*10),int(pos[3]*10),int(192*10))
#         acknowledge()
#         #7 gripper open
#         GripperProtocol(0)
#         #8
#         to_position_task(0,int(pos[2]*10),int(pos[3]*10),int(300*10))
#         acknowledge()
#         #9
#         sethomeProtocol()
#         acknowledge()
#         key = 0
#     elif key == 'playchess':
#         chess_start = input('chess_start: ')
#         chess_final = input('chess_final: ')
#         chess_mode = input('chess_mode: ')
#         # real_DEG=0

#         print(int(chess_start[0]),int(chess_start[1]),int(chess_final[0]),int(chess_final[1]))
#         pos = get_chess_board_position(int(chess_start[0]),int(chess_start[1]),int(chess_final[0]),int(chess_final[1]),real_DEG)
#         print(pos)
#         st = 'n'
#         while st!='Y' and st!='y':
#             st = input('start(Y/n):')
#             print(st)
#         # enc()
#         if chess_mode=='1':
#             #1
#             to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(300*10))
#             acknowledge()
#             #2
#             to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(200*10))
#             acknowledge()
#             #3 gripper close
#             GripperProtocol(1)
#             #4
#             to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(300*10))
#             acknowledge()
#             #5
#             to_position_task(0,int(pos[2]*10),int((pos[3])*10),int(300*10))
#             acknowledge()
#             #6
#             to_position_task(0,int(pos[2]*10),int((pos[3])*10),int(200*10))
#             acknowledge()
#             #7 gripper open
#             GripperProtocol(0)
#             #8
#             to_position_task(0,int(pos[2]*10),int((pos[3])*10),int(300*10))
#             acknowledge()
#             #9
#             sethomeProtocol()
#             acknowledge()
#         elif chess_mode=='2':
#             #1
#             to_position_task(0,int(pos[2]*10),int((pos[3])*10),int(300*10))
#             acknowledge()
#             #2
#             to_position_task(0,int(pos[2]*10),int((pos[3])*10),int(200*10))
#             acknowledge()
#             #3 gripper close
#             GripperProtocol(1)
#             #4
#             to_position_task(0,int(pos[2]*10),int((pos[3])*10),int(300*10))
#             acknowledge()
#             #5
#             to_position_task(0,int(350*10),int(-430*10),int(300*10))
#             acknowledge()
#             #6 gripper open
#             GripperProtocol(0)
#             # enc()
#             #1
#             to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(300*10))
#             acknowledge()
#             #2
#             to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(200*10))
#             acknowledge()
#             #3 gripper close
#             GripperProtocol(1)
#             #4
#             to_position_task(0,int(pos[0]*10),int(pos[1]*10),int(300*10))
#             acknowledge()
#             #5
#             to_position_task(0,int(pos[2]*10),int((pos[3])*10),int(300*10))
#             acknowledge()
#             #6
#             to_position_task(0,int(pos[2]*10),int((pos[3])*10),int(200*10))
#             acknowledge()
#             #7 gripper open
#             GripperProtocol(0)
#             #8
#             to_position_task(0,int(pos[2]*10),int((pos[3])*10),int(300*10))
#             acknowledge()
#             #9
#             sethomeProtocol()
#             acknowledge()
#         key = 0
#     else:
#         print('invalid key!!!')
#         key = 0
# # KeyPressSerial()
# # serialPort.close()
