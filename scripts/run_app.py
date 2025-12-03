import tkinter as tk
from app.gui import ChatUI

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatUI(root)
    app.run()
