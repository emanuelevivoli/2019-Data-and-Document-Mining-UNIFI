import sys
import time
MAX_ = 7
i = 0

input = sys.stdin.readline()
app = str(input)
fixation_name = str(app.split("\\")[-1])

while i < MAX_: 

    print("PHOTO_"+str(i))
    sys.stdout.flush()
    time.sleep(3)
    i = i+1


print("END")
sys.stdout.flush()