from tkinter import *
from tkinter import ttk
import os
import pickle
import Game
from tkinter import messagebox

class Yatzy(ttk.Frame):
    
    dice = [ Game.Dice() for n in range(5) ]

    def __init__(self,master=None):

        super().__init__(master)

        master.title("Micke's Yazty")
        master.geometry("800x800")
       # master.configure(background='#ffffdd')
        
        self.frame = ttk.Frame(master)
        self.frame.pack(fill=BOTH, expand=1)

        # Set up menu bar
        self.menubar = Menu(self.master)
        master.config(menu=self.menubar)
        master.option_add('*tearOff', 0) # Fix menus
        # Make menu bar options
        self.filemenu, self.helpmenu = Menu(self.menubar), Menu(self.menubar)
        self.menubar.add_cascade(label="Fil", menu=self.filemenu) # Attach to menu bar
        self.menubar.add_cascade(label="Hjälp", menu=self.helpmenu) 
        # Add menu items
        self.filemenu.add_command(label="Nytt spel", command=self.playAgain) # Add menu option to entry
        self.filemenu.add_command(label="Rensa sparat spel", command=resetSave) # Add menu option to entry
        self.filemenu.add_command(label="Avsluta", command=quit) # Add menu option to entry
        self.helpmenu.add_command(label="Om programmet", command=about) 

        # Add images
        self.banner_photo = PhotoImage(file='images/banner.png')
        ttk.Label(self.frame, image=self.banner_photo).grid(row=0, column=0, columnspan=5)
        self.dice_img = []

        # Splash images, replace with nicer ones?
        for n in range(5):
            dice_path=f"images/d{n+1}.png"
            self.dice_img.append(PhotoImage(file=dice_path))
            ttk.Label(self.frame, image=self.dice_img[n]).grid(row=1,column=n)

        newBtn = ttk.Button(
                self.frame, text="Nytt Spel", command=self.newGame).grid(row=2,column=1)
        contBtn = ttk.Button(
                self.frame, text="Fortsätt Spela", command=self.loadAutoSave, state='disabled')
        if os.path.isfile("saves/autosave.sav"):
            contBtn.state(['!disabled']) # Enable button if theres an Autosave file present
        contBtn.grid(row=2,column=3)

        for child in self.frame.winfo_children(): child.grid_configure(padx=5, pady=5)
        
        self.resetGame()
        
    def resetGame(self):
        # Reset all values
        self.scorecard = [None for i in range(17)]
        self.tempscore = []
        self.catnr = IntVar()
        self.catnr.set(15)

    def newGame(self):

        # Check previous score and update
        if len(self.tempscore):
            cat, score = self.tempscore
            self.scorecard[cat] = score
            upper = sum([i for i in self.scorecard[0:6] if i is not None])
            self.scorecard[16] = 50 if upper > 62 else 0 # Handle bonus
            for die in self.dice: die.thaw()
            self.catnr.set(len([i for i in self.scorecard if i is None])-1)
            with open("saves/autosave.sav","wb") as f: # Generate autosave file
                pickle.dump(self.scorecard, f)
        # Reset game
        self.kastnr = IntVar()
        # Reset frames, destroy old
        self.frame.destroy()
        self.frame = ttk.Frame(self.master)
        self.frame.pack()
        self.banner_photo = PhotoImage(file='images/banner.png')
        ttk.Label(self.frame, image=self.banner_photo).grid(row=0, column=1,columnspan=3)

        # Diceframe contains the dice and the hold buttons
        self.diceframe = ttk.Frame(self.frame)
        self.diceframe.grid(row=1,column=1,sticky="e")
        # Scoreframe houses the radio buttons to select score category
        self.scoreframe = ttk.Frame(self.frame)
        self.scoreframe.grid(row=1,column=2)
        self.scoreBtn = ttk.Button(self.diceframe, text="Nästa kategori", command=self.newGame)
        # Some rows to display status of throw and cathegories left
        ttk.Label(self.scoreframe, text="Kast nummer").grid(row=18,column=0,pady=10)
        ttk.Label(self.scoreframe, textvariable=self.kastnr).grid(row=18,column=1,pady=10,sticky=E)
        ttk.Label(self.scoreframe, text="av 3").grid(row=18,column=2,pady=10)
        ttk.Label(self.scoreframe, text="Kategorier kvar ").grid(row=19,column=0)
        ttk.Label(self.scoreframe, textvariable=self.catnr).grid(row=19,column=1,sticky=E)
        ttk.Label(self.scoreframe, text="av 15").grid(row=19,column=2)
        self.scoreBtn.grid(row=8,column=3,pady=10)
        self.scoreBtn.state(['disabled'])
        self.rollBtn = ttk.Button(self.diceframe, text="Kasta om", command=self.rollDice)
        self.rollBtn.grid(row=8,column=1,pady=10)
        if self.catnr.get() == 0:
            self.gameWon()
        else:
            self.rollDice()

    def rollDice(self):
        self.kastnr.set(self.kastnr.get()+1)
        self.dice_img = []
        self.die_vars = []
        chkBtns = []
        diceboxes = []
        for n in range(5):
            # the labels with the dice are made here
            dice_path=f"images/d{n+1}.png"
            die = self.dice[n]
            die.roll()
            mycommand = lambda:print(n)
            dice_path=f"images/d{die.value}-64.png"
            self.dice_img.append(PhotoImage(file=dice_path))
            ttk.Label(self.diceframe, image=self.dice_img[n]).grid(row=n,column=1)
            var = IntVar()
            IntVar.set(var,die.iced)
            check = ttk.Checkbutton(self.diceframe, text=f"Lås tärning {n+1}", 
                    variable=var)
            check.grid(row=n,column=2)
            self.die_vars.append(var)
            chkBtns.append(check)
        # This is here so functions work correctly
        chkBtns[0]['command'] = lambda:self.dice[0].toggle()
        chkBtns[1]['command'] = lambda:self.dice[1].toggle()
        chkBtns[2]['command'] = lambda:self.dice[2].toggle()
        chkBtns[3]['command'] = lambda:self.dice[3].toggle()
        chkBtns[4]['command'] = lambda:self.dice[4].toggle()
        self.scoreBtn.state(['disabled'])

        if self.kastnr.get() > 2:
            for check in chkBtns: check.state(['disabled']) 
            self.rollBtn.state(['disabled']) # Disable button if it's the last throw
            for die in self.dice: die.thaw()

        self.scoreDice()

    def scoreDice(self):
        ttk.Label(self.scoreframe,text="Kategori",width=15).grid(
                row=0,column=0)
        self.scorelist = [ 
                ("Ettor",Game.Score.ones), 
                ("Tvåor",Game.Score.twos),
                ("Treor",Game.Score.threes), 
                ("Fyror",Game.Score.fours),
                ("Femmor",Game.Score.fives), 
                ("Sexor",Game.Score.sixes),
                ("Ett par",Game.Score.onePair), 
                ("Två par",Game.Score.twoPairs),
                ("Triss",Game.Score.threeKind),
                ("Fyrtal",Game.Score.fourKind),
                ("Liten stege",Game.Score.smStraight),
                ("Stor stege",Game.Score.lgStraight),
                ("Kåk",Game.Score.fullHouse),
                ("Chans:",Game.Score.chance),
                ("Yatzy:",Game.Score.yatzy)
        ]
        self.sel_score = IntVar()
        self.possible_scores = []
        self.rdoBtns = []
        for val, scoreObj in enumerate(self.scorelist):
            rownr = val+1 if val <= 5 else val+2
            # indicatoron=0 makes the radio buttons wide
            r = Radiobutton(self.scoreframe,text=scoreObj[0],command=self.enableScore,
                    variable=self.sel_score,value=val,width=15,
                    padx=5,anchor=E,indicatoron=0)
            r.grid(row=rownr,column=0)
            r.deselect()
            self.rdoBtns.append(r)
            scoretext = scoreObj[1](self.dice)
            self.possible_scores.append(scoretext)
            ttk.Label(self.scoreframe,text=scoretext,width=3,
                    relief='raised').grid(padx=2,row=rownr,column=1)
            ttk.Label(self.scoreframe,text=self.scorecard[val],width=3,
                    relief='raised').grid(padx=2,row=rownr,column=2)
            if self.scorecard[val] is not None:
                r['state'] = 'disabled'
            if val == 6: # Insert bonus rows
                # make it look the same
                ttk.Label(self.scoreframe,text="Bonus",width=15).grid(
                        padx=5,row=7,column=0)
                ttk.Label(self.scoreframe,text=self.scorecard[16],width=3,
                    relief='raised').grid(padx=2,row=7,column=2)

        ttk.Label(self.scoreframe,text="Summa",width=15).grid(
                padx=5,row=17,column=0)
        scorecard_sum = sum([i for i in self.scorecard if i is not None])
        ttk.Label(self.scoreframe,text=scorecard_sum,width=3,
                relief='raised').grid(padx=2,row=17,column=2)

    def gameWon(self):
        """ This replaces the dice screen when the game is finished """
        self.win_photo = PhotoImage(file='images/winner.png')
        self.diceframe.destroy()
        self.diceframe = ttk.Frame(self.frame)
        self.diceframe.grid(row=1,column=1,sticky="e")
        ttk.Label(self.diceframe, image=self.win_photo).grid(row=2, column=0)
        score = sum([i for i in self.scorecard if i is not None])
        ttk.Label(self.diceframe,
                text=f"Grattis!\nDu vann spelet med {score} poäng",
        ).grid(row=3,column=0)
        ttk.Button(self.diceframe, text="Nytt spel", 
                command=self.playAgain).grid(row=4,column=1,pady=10)
        resetSave()
        ttk.Button(self.diceframe, text="Avsluta", 
                command=quit).grid(row=4,column=2,pady=10)
        self.scoreDice()

    def playAgain(self):
        """ Resets the game ( from endscreen and menu )"""
        self.resetGame()
        self.newGame()

    def enableScore(self): 
        """ This function is called my the radioboxes 
        I disables the score button so it cant submit unless
        a value is chosen"""
        cat_num = self.sel_score.get()
        score = self.possible_scores[cat_num]
        if self.scorecard[cat_num] == None:
            self.scoreBtn.state(['!disabled'])
            self.tempscore = [cat_num, score]
        else: 
            self.scoreBtn.state(['disabled'])

    def loadAutoSave(self):
        with open("saves/autosave.sav","rb") as f: # Load autosave file
            self.scorecard = pickle.load(f)
            self.newGame()

def resetSave():
    os.remove("saves/autosave.sav")


def about(): # Show a nice popup from the menu
    messagebox.showinfo("Om programmet", """Yatzy-spelet!
Gjort av Micke 2018
~~ --- ~~
""")

def main():
    root = Tk()
    yatzy = Yatzy(root)
    root.mainloop()

if __name__ == "__main__":
    main()
