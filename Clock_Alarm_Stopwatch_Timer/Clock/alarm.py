import time
import datetime
#import pygame

def alarm(alarm_time):
    print(f"Alarm set for{alarm_time}")
    sound_file = "my_music.mp3"
    is_running =True

    while is_running:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(current_time)
        time.sleep(1)

        if current_time==alarm_time:
             print("ALARM RINGING")
             is_running=False


if __name__ == "__main__":
    alarm_time = input("Enter the alarm time (HH:MM:SS): ")
    alarm(alarm_time)
