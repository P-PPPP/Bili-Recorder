# -- encoding: utf-8 --
import os , sys , subprocess , requests , time , shutil , zipfile
from threading import Thread , Event

try: assert os.path.exists("./config.json") , FileNotFoundError("config.json not found , Exiting ... ")
except FileNotFoundError: raise SystemExit(128)
os.path.exists('output') or os.mkdir('output')
shutil.move("./config.json", "./output/config.json")
timeout_event = Event()

def Timer_(event):
    start_timestamp = time.time()
    while time.time() - start_timestamp < 21240: # Github Actions Allow 6 hours, set 5.9 hour to kill the process
        time.sleep(60)
    event.set()
Thread(target=Timer_,args=timeout_event,).start()

##### Work flow #####
# Get Recorder Info
recorder_release = requests.get("https://api.github.com/repos/BililiveRecorder/BililiveRecorder/releases/latest").json()["assets"]
download_url = [fn for fn in recorder_release if 
    ("CLI" in fn["name"] and "any" in fn["name"]) ][0]["browser_download_url"]
# Init Environment
if sys.platform == "win32":
    subprocess.run("choco install aria2 7zip", shell=True,
        stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
    subprocess.run(f"aria2c {download_url} -o  recorder.zip", shell=True, 
        stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
if sys.platform == "linux":
    subprocess.run("sudo apt update && apt install aria2 zip unzip", shell=True ,
        stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
    subprocess.run(f"aria2c {download_url} -o  recorder.zip", shell=True, 
        stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
if sys.platform == "darwin":
    subprocess.run("brew install aria2 zip unzip", shell=True,
        stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
    subprocess.run(f"aria2c {download_url} -o  recorder.zip", shell=True, 
        stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)

# Unzip Universal Exe and Run
z = zipfile.ZipFile("./recorder.zip")
z.extractall()
shutil.move("./any/Release","./executeable")

command = ["./excuteable/BililiveRecorder.Cli","run","--bind","http://*:2345","output"]
Record_Process = subprocess.Popen(command, shell=True)

while Record_Process.poll() is None:
    if timeout_event.is_set():
        Record_Process.kill()
        break
    time.sleep(10)