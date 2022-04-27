import threading
import tkinter

tk = tkinter.Tk()
threading.Thread(target=tk.mainloop).start()

