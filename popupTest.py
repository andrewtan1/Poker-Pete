import tkinter as tk

''' Global Bet Value Variable: Use This As Input Value '''
betValue = 0

def askInput():
    root = tk.Tk()
    # Set Window Position
    winWidth = root.winfo_reqwidth()    # find width
    winHeight = root.winfo_reqheight()  # find heigh
    posRight = int(root.winfo_screenwidth()/2-winWidth/2)   # find half width
    posDown = int(root.winfo_screenheight()/2-winHeight/2)  # find half height
    root.geometry("+{}+{}".format(posRight,posDown))    # set geometry to center
    # Form Label
    betLabel = tk.Label(root, text="Bet Amount")
    # Entry Definition
    ent = tk.Entry(root, bd=5)

    def getName(event):
        global betValue # globally change betValue
        betValue = ent.get()  # get input (could be any type) 
        root.destroy()  # close window

    root.bind('<Return>', getName)

    # Submit Button
    submit = tk.Button(root, text="Submit", command=getName)
    submit.bind('<Button-1>', getName)

    # Pack Elements
    betLabel.pack()
    ent.pack()
    submit.pack()
    root.mainloop()

while True:    
    try:
        askInput()
        print(betValue)
        val = float(betValue)
        if val > 0:
            break
        print('Please enter a valid bet amount')
    except ValueError:
        print('Please enter a valid bet amount')