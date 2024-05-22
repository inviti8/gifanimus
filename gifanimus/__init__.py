"""A Simple Gif Animation Window"""

__version__ = "0.01"

import threading
import tkinter
from PIL import Image, ImageTk
import sys
import time

class LoadingGif:
    def __init__(self, gifDir, frameDelay=1000, consoleMsg=""):
        self.gif = gifDir
        self.delay = frameDelay
        self.msg = consoleMsg
        self.window = LoadingWindow(self.gif, self.delay, self.msg)
        self.thread = threading.Thread(target=self.window.new)
        self.thread.setDaemon(True)
        self.thread.start()
        
    def Stop(self):
        self.window.Stop()


class LoadingWindow:
    def __init__(self, gifDir, frameDelay, consoleMsg):
        self.gif = gifDir
        self.delay = frameDelay
        self.root = None
        self.file = None
        self.frames = None
        self.thread = None
        self.active = False
        self.speed = None
        self.process_is_alive = False
        self.window = None
        self.img = None

        self.process_is_alive = False

    def new(self):
        self.root = tkinter.Tk()
        self.root.wait_visibility(self.root)
        self.file = Image.open(self.gif) 
        self.frames = [tkinter.PhotoImage(file=self.gif, format='gif -index %i'%(i)) for i in range(self.file.n_frames)]
        self.speed = self.delay // len(self.frames) # make one cycle of animation around 4 secs

        self.process_is_alive = True
        self.Play()
        thread = threading.Thread(target=self.consoleAnimation)
        thread.setDaemon(True)
        thread.start()
        self.root.mainloop()
        
    def _center_window(self, win):
        win.wait_visibility() # make sure the window is ready
        x = (win.winfo_screenwidth() - (win.winfo_width()//2)) // 2
        y = (win.winfo_screenheight() - (win.winfo_height()//2)) // 2
        win.geometry(f'+{x}+{y}')

    def consoleAnimation(self):
        animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
        i = 0
        while self.process_is_alive:
            sys.stdout.write("\r | Loading..." + animation[i % len(animation)])
            sys.stdout.flush()
            time.sleep(0.4)
            i += 1
            
    def Stop(self):
        self.process_is_alive = False
      
    def Play(self, n=0, top=None, lbl=None):
        if not self.process_is_alive:
            self.window.destroy()
            self.root.destroy()
            return
        
        if n == 0:
            if self.img == None:
                self.root.withdraw()
                self.window = tkinter.Toplevel()
                self.window.overrideredirect(True)
                self.window.wm_attributes("-alpha", 0.0)
                self.img = tkinter.Label(self.window, text="", image=self.frames[0])
                self.img.pack()
                self._center_window(self.window)
                
        if n < len(self.frames)-1:
            self.img.config(image=self.frames[n])
            self.img.after(self.speed, self.Play, n+1, top, lbl)
        else:
            self.img.config(image=self.frames[0])
            self.img.after(self.speed, self.Play, 0, top, lbl)
            


