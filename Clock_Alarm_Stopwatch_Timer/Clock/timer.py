import time

timer = int(input("Enter time in seconds: "))

for i in range(timer,0,-1):
    sec = i%60
    min = int(i/60)%60
    hr = int(i/3600)

    print(f"{hr}:{min}:{sec}")
    time.sleep(1)

print("TIME UP")
