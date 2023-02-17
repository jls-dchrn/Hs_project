import lib as li

if __name__ == "__main__":

    root = li.Tk()
    root.title("Programme JuMo")
    root.geometry("1920x1080")

    bg = li.PhotoImage(file='bg.png')
    background_label = li.Label(image=bg)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    li.centrefenetre(root)

    li.mere(root).pack()
    root.mainloop()
