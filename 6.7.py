import turtle
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import glob
import threading
import ctypes
import subprocess
from bs4 import BeautifulSoup

# =======================
# 1️⃣ Turtle Logo Code
# =======================

def start_turtle_logo():
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.title("Nxo Launcher")

    # 🔥 Zugriff auf Fenster
    root = screen._root

    # ❌ Kein X / kein Rahmen / kein Minimieren
    root.overrideredirect(True)

    # 🔥 Vollbild
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f"{width}x{height}+0+0")

    t = turtle.Turtle()
    t.shape("turtle")
    t.color("white")
    t.fillcolor("black")
    t.pensize(6)
    t.speed(3)

    # Dreieck
    size = 200
    radius = 40

    t.penup()
    t.goto(-100, -60)
    t.pendown()

    t.begin_fill()
    for i in range(3):
        t.forward(size)
        t.circle(radius, 120)
    t.end_fill()

    # Position N
    ziel_x = -120
    ziel_y = -100

    t.penup()
    t.goto(ziel_x, ziel_y)

    # Text
    t.goto(-120, -140)
    t.write("Nxo Launcher", align="left", font=("Arial", 28, "bold"))

    # Schildkröte oben lassen
    t.goto(ziel_x, ziel_y)

    # 🔥 Automatisch schließen nach 3 Sekunden
    def close_window():
        turtle.bye()

    screen.ontimer(close_window, 3000)

    turtle.mainloop()


# =======================
# 2️⃣ Tkinter USB Creator
# =======================

def start_tkinter_app():
    root = tk.Tk()
    root.title("XO USB Creator")
    root.geometry("520x600")
    root.configure(bg="#2e2e2e")
    root.withdraw()

    def log(text):
        output.insert(tk.END, text + "\n")
        output.see(tk.END)

    def get_laufwerke():
        laufwerke = []
        result = os.popen('wmic logicaldisk get name,size').read().splitlines()
        for line in result[1:]:
            parts = line.split()
            if len(parts) == 2:
                name = parts[0]
                size = int(parts[1])
                laufwerke.append(f"{name} ({size//(1024**3)} GB)")
        return laufwerke

    def start_rufus_admin(path):
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", path, None, None, 1)
            return True
        except:
            return False

    def finde_rufus():
        downloads = os.path.expanduser("~/Downloads")
        files = glob.glob(os.path.join(downloads,"rufus*.exe"))
        return files[0] if files else None

    def lade_rufus():
        log("Rufus wird heruntergeladen...")
        url = "https://rufus.ie/downloads/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text,"html.parser")
        link = soup.find("a",href=lambda href: href and href.endswith(".exe"))
        download_url = link['href']

        downloads = os.path.expanduser("~/Downloads")
        path = os.path.join(downloads,"rufus_latest.exe")

        r = requests.get(download_url,stream=True)
        total = int(r.headers.get("content-length",0))
        downloaded = 0

        with open(path,"wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                progress["value"] = downloaded/total*100
                root.update_idletasks()

        log("Rufus Download abgeschlossen")
        return path

    def rufus_workflow():
        try:
            rufus = finde_rufus()
            if not rufus:
                log("Rufus nicht gefunden")
                rufus = lade_rufus()

            log("Rufus wird gestartet...")
            start_rufus_admin(rufus)

            log("Bitte Rufus schließen um fortzufahren")

            while True:
                tasks = os.popen("tasklist").read().lower()
                if "rufus" not in tasks:
                    break
                root.after(1000)

            log("Rufus wurde geschlossen")
            download_pack()

        except Exception as e:
            log(f"Fehler: {e}")

    def download_pack():
        url = urls.get(combobox.get())
        laufwerk = laufwerks_combobox.get()

        if not laufwerk:
            log("Kein Laufwerk gewählt")
            return

        laufwerk = laufwerk.split()[0]

        log("Pack wird heruntergeladen...")

        r = requests.get(url,stream=True)
        total = int(r.headers.get("content-length",0))
        downloaded = 0

        filename = os.path.join(laufwerk,"XO_pack.txt")

        with open(filename,"wb") as f:
            for chunk in r.iter_content(chunk_size=4096):
                f.write(chunk)
                downloaded += len(chunk)
                progress["value"] = downloaded/total*100
                root.update_idletasks()

        progress["value"] = 100
        log("Download fertig")

    def start():
        threading.Thread(target=rufus_workflow,daemon=True).start()

    def choose_language():
        win = tk.Toplevel(root)
        win.title("Sprache wählen")
        win.geometry("300x150")

        tk.Label(win,text="Sprache wählen").pack(pady=10)

        var = tk.StringVar(value="de")
        combo = ttk.Combobox(win,textvariable=var)
        combo["values"] = ("de","en")
        combo.pack()

        def ok():
            win.destroy()
            root.deiconify()
            combobox["values"] = (
                "Download XO",
                "Install XO",
                "Support XO"
            )
            combobox.set("Download XO")

        tk.Button(win,text="OK",command=ok).pack(pady=10)

    label = tk.Label(root,text="Option wählen",bg="#2e2e2e",fg="white")
    label.pack(pady=10)

    combobox = ttk.Combobox(root)
    combobox.pack(pady=10)

    laufwerk_label = tk.Label(root,text="SD Karte wählen",bg="#2e2e2e",fg="white")
    laufwerk_label.pack()

    laufwerks_combobox = ttk.Combobox(root, state="readonly")
    laufwerks_combobox["values"] = get_laufwerke()
    laufwerks_combobox.pack(pady=10)

    output = tk.Text(root,height=12,width=60,bg="#333333",fg="white")
    output.pack(pady=20)

    progress = ttk.Progressbar(root,length=420)
    progress.pack(pady=10)

    start_btn = tk.Button(root,text="Start",command=start,bg="#4CAF50",fg="white")
    start_btn.pack(pady=20)

    urls = {
        "Download XO":"https://raw.githubusercontent.com/LurNyx/Ox-Puport/main/test.txt",
        "Install XO":"https://raw.githubusercontent.com/LurNyx/Ox-Puport/main/test.txt",
        "Support XO":"https://raw.githubusercontent.com/LurNyx/Ox-Puport/main/test.txt"
    }

    choose_language()
    root.mainloop()


# =======================
# 🔹 Hauptprogramm
# =======================

if __name__ == "__main__":
    start_turtle_logo()   # läuft automatisch + nicht schließbar
    start_tkinter_app()  # startet danach