import threading
count = 0
def aa(count):
    count +=1
    print(count)
    timer=threading.Timer(1,aa,args=[count])
    timer.start()

    if count == 5:
        timer.cancel()

aa(0)