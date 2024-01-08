import tkinter as tk

root = tk.Tk()
label = tk.Label(root, text="Hello, Tkinter!")
label.pack()
root.mainloop()



from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication([])
label = QLabel('Hello, PyQt!')
label.show()
app.exec_()



from kivy.app import App
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        return Label(text='Hello, Kivy!')

if __name__ == '__main__':
    MyApp().run()