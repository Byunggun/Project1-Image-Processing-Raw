################################### - 권장1 : GrayScale 영상 처리 및 데이터 분석 툴 제작 ##################################
from tkinter import *; import os.path ;import math
from  tkinter.filedialog import *
from  tkinter.simpledialog import *
import operator
import threading

## 함수 선언부
def loadImage(fname) :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    fsize = os.path.getsize(fname) # 파일 크기 확인
    inH = inW = int(math.sqrt(fsize))  # 입력메모리 크기 결정! (중요)

    inImage = []; tmpList = []
    for i in range(inH) :  # 입력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(inW) :
            tmpList.append(0)
        inImage.append(tmpList)
    # 파일 --> 메모리로 데이터 로딩
    fp = open(fname, 'rb') # 파일 열기(바이너리 모드)
    for  i  in range(inH) :
        for  k  in  range(inW) :
            inImage[i][k] =  int(ord(fp.read(1)))
    fp.close()

def openFile() :
    global window, canvas, paper, filename,inImage, outImage,inW, inH, outW, outH
    filename = askopenfilename(parent=window,
                               filetypes=(("RAW파일", "*.raw"), ("모든파일", "*.*")))
    loadImage(filename) # 파일 --> 입력메모리
    equal() # 입력메모리--> 출력메모리

def display() : #Thread를 활용한 display() 함수
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 기존에 캐버스 있으면 뜯어내기.
    if  canvas != None :
        canvas.destroy()
    # 화면 준비 (고정됨)
    window.geometry(str(outH) + 'x' + str(outW))
    canvas = Canvas(window, width=outW, height=outH)
    paper = PhotoImage(width=outW, height=outH)
    canvas.create_image((outW/2, outH/2), image=paper, state='normal')
    # 화면에 출력
    def putPixel() :
        for i in range(0, outH) :
            for k in range(0, outW) :
                data = outImage[i][k]
                paper.put('#%02x%02x%02x' % (data, data, data), (k,i))

    threading.Thread(target=putPixel).start() #Thread를 활용한 display() 함수
    canvas.pack()


#
def equal() :  # 동일 영상 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;  outH = inH;
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            outImage[i][k] = inImage[i][k]

    display()

#[화소점처리 알고리즘]
def addImage(num) :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW
    outH = inH
    outImage = []
    tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)

    if num == 1: #밝게하기(덧셈)
        value = askinteger('밝게하기', '밝게할 값-->', minvalue=1, maxvalue=255)
        for  i  in  range(inH) :
            for  k  in  range(inW) :
                if inImage[i][k] + value > 255 : # 덧셈
                    outImage[i][k] = 255
                else :
                    outImage[i][k] = inImage[i][k] + value

    elif num == 2: #어둡게하기(뺄셈)
        value = askinteger('어둡게하기', '어둡게할 값-->', minvalue=1, maxvalue=255)
        for i in range(inH):
            for k in range(inW):
                if inImage[i][k] - value < 0:  # 뺄셈
                    outImage[i][k] = 0
                else:
                    outImage[i][k] = inImage[i][k] - value

    elif num == 3: #밝게하기(곱셈)=뚜렷하게
        value = askinteger('밝게하기(뚜렷하게)', '밝게할 값-->', minvalue=1, maxvalue=255)
        for i in range(inH):
            for k in range(inW):
                if inImage[i][k] * value > 255:  # 곱셈
                    outImage[i][k] = 255
                else:
                    outImage[i][k] = inImage[i][k] * value

    elif num == 4: #어둡게하기(나눗셈)=희미하게
        value = askinteger('어둡게하기(희미하게)', '어둡게할 값-->', minvalue=1, maxvalue=255)
        for i in range(inH):
            for k in range(inW):
                if inImage[i][k] // value > 255:  # 나눗셈 : {조심} 몫만 출력 if not 에러.
                    outImage[i][k] = 255
                elif inImage[i][k] // value < 0:
                    outImage[i][k] = 0
                else:
                    outImage[i][k] = inImage[i][k] // value

    elif num == 5:  # AND연산
        pass

    elif num == 6:  # OR연산
        pass

    elif num == 7:  # XOR연산
        pass

    elif num == 8:  # 반전
        pass

    elif num == 9:  # 감마
        pass

    elif num == 10:  # 파라볼라(Cap)
        pass

    elif num == 11:  # 파라볼라(Cup)
        pass

    elif num == 12:  # 이진화
        pass

    elif num == 13:  # 범위강조
        pass

    display()

#[데이터분석]
def analyzeData(num) :
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    if num == 1 : # 입출력 영상의 평균값
        rawSum = 0
        for  i  in  range(inH) :
            for  k  in  range(inW) :
                rawSum += inImage[i][k]
        inRawAvg = int(rawSum / (inH*inW))

        rawSum = 0
        for  i  in  range(outH) :
            for  k  in  range(outW) :
                rawSum += outImage[i][k]
        outRawAvg = int(rawSum / (outH*outW))

        subWindow = Toplevel(window) # 부모(window)에 종속된 서브윈도
        subWindow.geometry('200x100')
        label1 = Label(subWindow, text='입력영상 평균값 -->' + str(inRawAvg))
        label1.pack()
        label2 = Label(subWindow, text='출력영상 평균값 -->' + str(outRawAvg))
        label2.pack()

    elif num == 2 : #입출력 시 최대값, 최소값
        inDict, outDict = {}, {}
        for i in range(inH): #{중요}{다시보기}
            for k in range(inW):
                if inImage[i][k] in inDict:
                    inDict[inImage[i][k]] += 1
                else:
                    inDict[inImage[i][k]] = 1
                if outImage[i][k] in outDict:
                    outDict[outImage[i][k]] += 1
                else:
                    outDict[outImage[i][k]] = 1
        insortList = sorted(inDict.items(), key=operator.itemgetter(1))
        outsortList = sorted(outDict.items(), key=operator.itemgetter(1))
        subWindow = Toplevel(window) # 부모(window)에 종속된 서브윈도
        subWindow.geometry('200x100')
        label1 = Label(subWindow, text="입력 시 최대값, 최소값 : " + str(insortList[-1]) + str(insortList[0]))
        label1.pack()
        label2 = Label(subWindow, text="출력 시 최대값, 최소값 : " + str(outsortList[-1]) + str(outsortList[0]))
        label2.pack()

    subWindow.mainloop()

#[기하학 처리]
def upDown() :  # 상하 반전 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;  outH = inH;
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            outImage[outW-1-i][k] = inImage[i][k] #{핵심}outH-K : 맨 뒤. #outH-1-K :0~255

    display()

def LRReversalImage():# 좌우반전 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    outW = inW;  outH = inH;
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            outImage[i][outH - 1 - k] = inImage[i][k] #{핵심} #좌우 반전

    display()


#화면 이동 알고리즘
def panImage() :
    global  panYN
    panYN = True

def mouseClick(event) :  # 동일 영상 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global sx, sy, ex, ey, panYN
    if not panYN :
        return
    sx = event.x;  sy = event.y;

def mouseDrop(event):  # 동일 영상 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global sx, sy, ex, ey, panYN
    if not panYN:
        return
    ex = event.x; ey = event.y;
    my = sx - ex ; mx = sy - ey

    # 중요! 출력메모리의 크기를 결정
    outW = inW;  outH = inH;
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            if 0<= i-mx <outH and 0<= k-my < outW :
                outImage[i-mx][k-my] = inImage[i][k] #Q)?
    panYN = False
    display()


def zoomOut() :  # 축소하기 알고리즘
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    scale = askinteger('축소하기', '축소할 배수-->', minvalue=2, maxvalue=32)
    outW = int(inW/scale);  outH = int(inH/scale);
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    for  i  in  range(inH) :
        for  k  in  range(inW) :
             outImage[int(i/scale)][int(k/scale)] = inImage[i][k] #{핵심} 나누기
    display()

def zoomInForW() : #화면확대-전방향
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    scale = askinteger('화면확대-전방향', '화면확대(전방향)할 배수-->', minvalue=2, maxvalue=32)
    outW = int(inW*scale);  outH = int(inH*scale);
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            outImage[int(i * scale)][int(k * scale)] = inImage[i][k]  # {핵심} 곱하기
    display()

def zoomInBackW(): #화면확대-역방향-이웃 화소 보간법
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # 중요! 출력메모리의 크기를 결정
    scale = askinteger('화면확대-역방향', '화면확대(역방향)할 배수-->', minvalue=2, maxvalue=32)
    outW = int(inW*scale);  outH = int(inH*scale);
    outImage = [];   tmpList = []
    for i in range(outH):  # 출력메모리 확보(0으로 초기화)
        tmpList = []
        for k in range(outW):
            tmpList.append(0)
        outImage.append(tmpList)
    #############################
    # 진짜 영상처리 알고리즘을 구현
    ############################
    for  i  in  range(inH) :
        for  k  in  range(inW) :
            outImage[int(i)][int(k)] = inImage[int(i/scale)][int(k/scale)] #{핵심}
    display()


#############
def RotationImage(): #회전 {작업 중}
    pass
     # global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
     # global sx, sy, ex, ey, panYN
     #
     # scale = askinteger('이동', '이동 각도-->', minvalue=1, maxvalue=360)
     #
     # my = sx - ex;
     # mx = sy - ey
     #
     # outW = inW;
     # outH = inH;
     # outImage = [];
     # tmpList = []
     # for i in range(outH):  # 출력메모리 확보(0으로 초기화)
     #     tmpList = []
     #     for k in range(outW):
     #         tmpList.append(0)
     #     outImage.append(tmpList)
     # #############################
     # # 진짜 영상처리 알고리즘을 구현
     # ############################
     # for i in range(inH):
     #     for k in range(inW):
     #         if 0 <= i - mx < outH and 0 <= k - my < outW:
     #             outImage[i - mx][k - my] = inImage[i][k] #{작업 중}
     #
     # display()
# ######################
#      # 화면 이동 알고리즘
#      def panImage():
#          global panYN
#          panYN = True
#
#      def mouseClick(event):  # 동일 영상 알고리즘
#          global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
#          global sx, sy, ex, ey, panYN
#          if not panYN:
#              return
#          sx = event.x;
#          sy = event.y;
#
#      def mouseDrop(event):  # 동일 영상 알고리즘
#          global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
#          global sx, sy, ex, ey, panYN
#          if not panYN:
#              return
#          ex = event.x;
#          ey = event.y;
#          my = sx - ex;
#          mx = sy - ey
#
#          # 중요! 출력메모리의 크기를 결정
#          outW = inW;
#          outH = inH;
#          outImage = [];
#          tmpList = []
#          for i in range(outH):  # 출력메모리 확보(0으로 초기화)
#              tmpList = []
#              for k in range(outW):
#                  tmpList.append(0)
#              outImage.append(tmpList)
#          #############################
#          # 진짜 영상처리 알고리즘을 구현
#          ############################
#          for i in range(inH):
#              for k in range(inW):
#                  if 0 <= i - mx < outH and 0 <= k - my < outW:
#                      outImage[i - mx][k - my] = inImage[i][k]  # Q)?
#          panYN = False
#          display()

################
def SyntheticImage():
    pass

##
def saveFile() :
    global window, canvas, paper, filename,inImage, outImage,inW, inH, outW, outH
    pass

def exitFile() :
    global window, canvas, paper, filename,inImage, outImage,inW, inH, outW, outH
    pass

## 전역 변수부
window, canvas, paper, filename = [None] * 4
inImage, outImage = [], []; inW, inH, outW, outH = [0] * 4
panYN = False;  sx, sy, ex, ey = [0] * 4
# ###
# Cf. <변수 정의>
# Window : 화면에 윈도창 출력
# Canvas : 출력 화면의 모양 나타내기
# Paper : 사진 이미지
# Filename : 불러올 이미지 파일
# inImage, inW, inH : (영상 처리 전)원시 영상에서 불러온 이미지, 그 폭, 그 높이
# outImage, outW, outH : (영상 처리 후)목적 영상으로 출력할 이미지, 그 폭, 그 높이
# panYN : 마우스 이동 변수
# sx, sy, ex, ey : 시작점x, 시작점y, 끝점x, 끝점y
# ##

## 메인 코드부
window = Tk();  window.geometry('400x400');
window.title('영상 처리&데이터 분석 Ver 0.3')
window.bind("<Button-1>", mouseClick)
window.bind("<ButtonRelease-1>", mouseDrop)


mainMenu = Menu(window);window.config(menu=mainMenu)
fileMenu = Menu(mainMenu);mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label='열기', command=openFile)
fileMenu.add_command(label='저장', command=saveFile)
fileMenu.add_separator()
fileMenu.add_command(label='종료', command=exitFile)

pixelMenu = Menu(mainMenu);mainMenu.add_cascade(label='화소점처리', menu=pixelMenu)
pixelMenu.add_command(label='동일영상', command=equal)
pixelMenu.add_command(label='밝게하기', command=lambda: addImage(1)) #덧셈
pixelMenu.add_command(label='어둡게하기', command=lambda: addImage(2)) #뺄셈
pixelMenu.add_command(label='밝게하기(뚜렷하게)', command=lambda: addImage(3)) #곱셈
pixelMenu.add_command(label='어둡게하기(희미하게)', command=lambda: addImage(4)) #나눗셈
#{작업 하기}
pixelMenu.add_command(label='AND연산', command=lambda: addImage(5))
pixelMenu.add_command(label="OR연산", command=lambda: addImage(6))
pixelMenu.add_command(label='XOR연산', command=lambda: addImage(7))
pixelMenu.add_command(label='반전', command=lambda: addImage(8))
pixelMenu.add_command(label='감마', command=lambda: addImage(9))
pixelMenu.add_command(label='파라볼라(Cap)', command=lambda: addImage(10))
pixelMenu.add_command(label='파라볼라(Cup)', command=lambda: addImage(11))
pixelMenu.add_command(label='이진화', command=lambda: addImage(12))
pixelMenu.add_command(label='범위강조', command=lambda: addImage(13))


##
geoMenu = Menu(mainMenu);mainMenu.add_cascade(label='기하학 처리', menu=geoMenu)
geoMenu.add_command(label='상하반전', command=upDown)
geoMenu.add_command(label='좌우반전', command=LRReversalImage)
geoMenu.add_command(label='화면이동', command=panImage)
geoMenu.add_command(label='화면축소', command=zoomOut)
geoMenu.add_command(label='화면확대-전방향', command=zoomInForW)
geoMenu.add_command(label='화면확대-역방향(이웃 화소 보간법)', command=zoomInBackW)
##{작업 하기}
geoMenu.add_command(label='회전', command=RotationImage)#{작업 중}
geoMenu.add_command(label='영상 합성', command=SyntheticImage)
##

analyseMenu = Menu(mainMenu);
analyzeMenu = Menu(mainMenu);mainMenu.add_cascade(label='데이터분석', menu=analyzeMenu)
analyzeMenu.add_command(label='평균값', command=lambda: analyzeData(1))
analyzeMenu.add_command(label='입출력 시 최대값, 최소값', command=lambda: analyzeData(2))
#더 작업하기

window.mainloop()

