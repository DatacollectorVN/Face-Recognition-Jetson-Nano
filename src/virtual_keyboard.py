import tkinter as tk

class VirtualKeyboard:
    def __init__(self, entry_name, window):

        self.exp = " "          # global variable 
        self.entry_name = entry_name

        # First row of keyboard
        q = tk.Button(window, text = 'Q' , width = 6, command = lambda : self.press('Q'))
        q.place(relx= 0.15 , rely= 0.4, width=60, height=40)

        w = tk.Button(window,text = 'W' , width = 6, command = lambda : self.press('W'))
        w.place(relx= 0.19 , rely= 0.4, width=60, height=40)

        E = tk.Button(window,text = 'E' , width = 6, command = lambda : self.press('E'))
        E.place(relx= 0.23 , rely= 0.4, width=60, height=40)

        R = tk.Button(window,text = 'R' , width = 6, command = lambda : self.press('R'))
        R.place(relx= 0.27 , rely= 0.4, width=60, height=40)

        T = tk.Button(window,text = 'T' , width = 6, command = lambda : self.press('T'))
        T.place(relx= 0.31 , rely= 0.4, width=60, height=40)

        Y = tk.Button(window,text = 'Y' , width = 6, command = lambda : self.press('Y'))
        Y.place(relx= 0.35 , rely= 0.4, width=60, height=40)

        U = tk.Button(window,text = 'U' , width = 6, command = lambda : self.press('U'))
        U.place(relx= 0.39 , rely= 0.4, width=60, height=40)

        I = tk.Button(window,text = 'I' , width = 6, command = lambda : self.press('I'))
        I.place(relx= 0.43 , rely= 0.4, width=60, height=40)

        O = tk.Button(window,text = 'O' , width = 6, command = lambda : self.press('O'))
        O.place(relx= 0.47 , rely= 0.4, width=60, height=40)

        P = tk.Button(window,text = 'P' , width = 6, command = lambda : self.press('P'))
        P.place(relx= 0.51 , rely= 0.4, width=60, height=40)


        # Second row of keyboard
        A = tk.Button(window,text = 'A' , width = 6, command = lambda : self.press('A'))
        A.place(relx= 0.15 , rely= 0.45, width=60, height=40)

        S = tk.Button(window,text = 'S' , width = 6, command = lambda : self.press('S'))
        S.place(relx= 0.19 , rely= 0.45, width=60, height=40)

        D = tk.Button(window,text = 'D' , width = 6, command = lambda : self.press('D'))
        D.place(relx= 0.23 , rely= 0.45, width=60, height=40)

        F = tk.Button(window,text = 'F' , width = 6, command = lambda : self.press('F'))
        F.place(relx= 0.27 , rely= 0.45, width=60, height=40)

        G = tk.Button(window,text = 'G' , width = 6, command = lambda : self.press('G'))
        G.place(relx= 0.31 , rely= 0.45, width=60, height=40)

        H = tk.Button(window,text = 'H' , width = 6, command = lambda : self.press('H'))
        H.place(relx= 0.35 , rely= 0.45, width=60, height=40)

        J = tk.Button(window,text = 'J' , width = 6, command = lambda : self.press('J'))
        J.place(relx= 0.39 , rely= 0.45, width=60, height=40)

        K = tk.Button(window,text = 'K' , width = 6, command = lambda : self.press('K'))
        K.place(relx= 0.43 , rely= 0.45, width=60, height=40)

        L = tk.Button(window,text = 'L' , width = 6, command = lambda : self.press('L'))
        L.place(relx= 0.47 , rely= 0.45, width=60, height=40)

        clear = tk.Button(window,text = 'Clear' , width = 6, background="#808080",command = self.clear)
        clear.place(relx= 0.51 , rely= 0.45, width=60, height=40)


        # Third row of keyboard
        shift_left = tk.Button(window,text = 'Shift' , width = 6, command = lambda : self.press('Shift'))
        shift_left.place(relx= 0.15 , rely= 0.5, width=60, height=40)

        Z = tk.Button(window,text = 'Z' , width = 6, command = lambda : self.press('Z'))
        Z.place(relx= 0.19 , rely= 0.5, width=60, height=40)

        X = tk.Button(window,text = 'X' , width = 6, command = lambda : self.press('X'))
        X.place(relx= 0.23 , rely= 0.5, width=60, height=40)

        C = tk.Button(window,text = 'C' , width = 6, command = lambda : self.press('C'))
        C.place(relx= 0.27 , rely= 0.5, width=60, height=40)

        V = tk.Button(window,text = 'V' , width = 6, command = lambda : self.press('V'))
        V.place(relx= 0.31 , rely= 0.5, width=60, height=40)

        B = tk.Button(window, text= 'B' , width = 6 , command = lambda : self.press('B'))
        B.place(relx= 0.35 , rely= 0.5, width=60, height=40)

        N = tk.Button(window,text = 'N' , width = 6, command = lambda : self.press('N'))
        N.place(relx= 0.39 , rely= 0.5, width=60, height=40)


        M = tk.Button(window,text = 'M' , width = 6, command = lambda : self.press('M'))
        M.place(relx= 0.43 , rely= 0.5, width=60, height=40)

        shift_right = tk.Button(window,text = 'Shift' , width = 6, command = lambda : self.press('Shift'))
        shift_right.place(relx= 0.47 , rely= 0.5, width=122, height=40)


        #Fourth Line Button
        ctrl = tk.Button(window,text = 'Ctrl' , width = 6, command = lambda : self.press('Ctrl'))
        ctrl.place(relx= 0.15 , rely= 0.55, width=60, height=40)

        Fn = tk.Button(window,text = 'Fn' , width = 6, command = lambda : self.press('Fn'))
        Fn.place(relx= 0.19 , rely= 0.55, width=60, height=40)

        Alt = tk.Button(window,text = 'Alt' , width = 6, command = lambda : self.press('Alt'))
        Alt.place(relx= 0.23 , rely= 0.55, width=60, height=40)

        space = tk.Button(window,text = 'Space' , width = 6, command = lambda : self.press(' '))
        space.place(relx= 0.27 , rely= 0.55, width=430, height=40)

    
    def press(self, num):
        self.exp=self.exp + str(num)
        self.entry_name.set(self.exp)

    def clear(self):
        self.exp = " "
        self.entry_name.set(self.exp)

