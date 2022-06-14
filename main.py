# -- encoding: utf-8 --
import os , sys , subprocess , requests , time , shutil , zipfile
from threading import Thread , Event

try: assert os.path.exists("./config.json") , FileNotFoundError("config.json not found , Exiting ... ")
except FileNotFoundError: raise SystemExit(128)
os.path.exists('output') or os.mkdir('output')
shutil.copy("./config.json", "./output/config.json")
timeout_event = Event()
RUNNING = True

def Timer_(event:Event):
    start_timestamp = time.time()
    while time.time() - start_timestamp < 21240: # Github Actions Allow 6 hours, set 5.9 hour to kill the process
        time.sleep(1)
        if RUNNING == False: break
    event.set()
timer_thread = Thread(target=Timer_,args=(timeout_event , ) , daemon=True)
timer_thread.start()

##### Work flow #####
# Download Recorder
recorder_release = requests.get("https://api.github.com/repos/BililiveRecorder/BililiveRecorder/releases/latest").json()["assets"]
download_url = [fn for fn in recorder_release if 
    ("CLI" in fn["name"] and "any" in fn["name"]) ][0]["browser_download_url"]
with requests.get(download_url, stream=True) as r:
    with open("recorder.zip", "wb") as f:
        shutil.copyfileobj(r.raw, f)
    r.close()

# Unzip Universal Exe and Run
z = zipfile.ZipFile("./recorder.zip")
z.extractall()
shutil.move("./any/Release","./executeable")
if sys.platform == "linux" or sys.platform == "darwin":  subprocess.run("sudo chmod +x ./executeable/BililiveRecorder.Cli", shell=True)
command = ["./executeable/BililiveRecorder.Cli","run","--bind","http://*:2345","output"]
Record_Process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=False)

while Record_Process.poll() is None:
    try:
        if timeout_event.is_set():
            Record_Process.terminate()
            break
        time.sleep(2)
    except KeyboardInterrupt:
        os.system("echo KeyboardInterrupt Pressed") 
        RUNNING = False
        Record_Process.terminate()
        Record_Process.wait()
        raise SystemExit(128)