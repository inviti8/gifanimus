"""A Simple Gif Animation Window"""

__version__ = "0.01"

import threading
import tkinter
from PIL import Image, ImageTk
import sys
import time

class GifAnimation:
    def __init__(self, gifDir, frameDelay=1000, loop=True, consoleMsg=""):
        self.gif = gifDir
        self.delay = frameDelay
        self.loop = loop
        self.msg = consoleMsg
        self.window = AnimationWindow(self.gif, self.delay, self.loop, self.msg)
        self.thread = threading.Thread(target=self.window.Activate)
        self.thread.setDaemon(True)

    def Play(self):
        self.thread.start()
        
    def Stop(self):
        self.window.Stop()


class AnimationWindow:
    def __init__(self, gifDir, frameDelay, loop, consoleMsg):
        self.gif = gifDir
        self.delay = frameDelay
        self.loop = loop
        self.msg = consoleMsg
        self.root = None
        self.file = None
        self.frames = None
        self.speed = None
        self.window = None
        self.img = None
        self.active = False

    def Activate(self):
        self.root = tkinter.Tk()
        #self.root.wait_visibility(self.root)
        self.file = Image.open(self.gif) 
        self.frames = [tkinter.PhotoImage(file=self.gif, format='gif -index %i'%(i)) for i in range(self.file.n_frames)]
        self.speed = self.delay // len(self.frames) # make one cycle of animation around 4 secs

        self.active = True
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
        animation = ['  -  ', '  /  ', '  |  ', '  \\  ']
        i = 0
        while self.active:
            sys.stdout.write( animation[i % len(animation)] + f"\r{self.msg}" )
            sys.stdout.flush()
            time.sleep(0.25)
            i += 1
            
    def Stop(self):
        self.active = False
      
    def Play(self, n=0, top=None, lbl=None):
        if not self.active:
            self.window.destroy()
            self.root.destroy()
            sys.stdout.flush()
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
            if self.loop:
                self.img.config(image=self.frames[0])
                self.img.after(self.speed, self.Play, 0, top, lbl)
            else:
                self.active = False
            

