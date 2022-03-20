
import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title('Article submission')
label = tk.Label(window, text = "Welcome to Analytics page").pack()
window.geometry("800x500")  

name = tk.Label(window, text = "Name").place(x = 30,y = 50)  
email = tk.Label(window, text = "Email").place(x = 30, y = 90)  
phone = tk.Label(window, text = "Contact #").place(x = 30, y = 130)  

a1 = tk.Entry(window).place(x = 80, y = 50)  

a2 = tk.Entry(window).place(x = 80, y = 90)  

a3 = tk.Entry(window).place(x = 100, y = 135)

gender = tk.Label(window, text = "Gender").place(x = 30, y = 165) 

radio1 = tk.Radiobutton(window, text="Male").place(x = 80, y = 165)
radio2 = tk.Radiobutton(window, text="Female", state='disabled').place(x =80,y = 185)
radio3 = tk.Radiobutton(window, text="Other", state = 'disabled').place(x = 80, y = 205)

skill = tk.Label(window, text = "Skills").place(x = 30, y = 225) 

check1 = tk.Checkbutton(window, text = "AI", height =1, width = 15).place(x= 80, y = 225) 
check2 = tk.Checkbutton(window, text = "ML", height = 1, width = 13).place(x= 80, y = 245)
check3 = tk.Checkbutton(window, text = "DS", height = 1,width = 9).place(x= 80, y = 265)

def onClick():

     messagebox.showinfo("Thank You", "Our team will get back to you")

click1 = tk.Button(window,text = "Submit", command = onClick).place(x= 150, y=380)

window.mainloop()