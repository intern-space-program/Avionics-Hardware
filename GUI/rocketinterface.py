import kivy
import subprocess
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window 
Window.size = (300, 200)

class grid(Widget):

    def graphbtn(self):
        print("plotting graphs")
        subprocess.call("python rocketGUI.py", shell=True)

        print("graphs plotted")
    def groundbtn(self):
        print("activate ground pi")

    def rocketbtn(self):
        print("activate rocket pi")
    

class Gui(App):

    def build(self):
        
        return grid()

Gui().run()