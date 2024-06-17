import tkinter as tk

root = tk.Tk()
root.title("Jemi's Image Cryptography System")
root.geometry("700x500")
root.config(bg="White")

label1= tk.Label(root, bg="white", foreground="black",
                 font=("Times New Roman", 25))
label1.pack(expand=True)
label1= tk.Label(root, text="Welcome to Jemi's Image Cryptography System", bg="white", foreground="black",
                 font=("Times New Roman", 25))
label1.pack()
label2= tk.Label(root, text="Please Click the button below to proceed to the cryptography system", bg="white",
                 foreground="black",
                 font=("Times New Roman", 25))
label2.pack()

button1= tk.Button(root, text="Click here", fg="black", highlightbackground="white", font=("Times New Roman", 20))
button1.pack(expand=True)


root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=0)
root.mainloop()