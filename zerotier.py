import os , sys , requests , subprocess , shutil

def Download_And_instal():
    if sys.platform == "linux" or sys.platform == "darwin": subprocess.run("curl -s https://install.zerotier.com | sudo bash", shell=True)
    if sys.platform == "win32":
        with requests.get("https://download.zerotier.com/dist/ZeroTier%20One.msi", stream=True) as r:
            with open("1.msi", "wb") as f:
                shutil.copyfileobj(r.raw, f)
            r.close()
        subprocess.run("msiexec /i 1.msi /quiet /passive", shell=True)

def Main():
    Network_id = os.getenv("ZEROTIER_NETWORK_ID")
    subprocess.Popen("zerotier-cli join {}".format(Network_id), shell=True)