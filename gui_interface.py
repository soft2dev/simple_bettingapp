from tkinter import *
import tkinter.messagebox
import math
from betting_bot import *

inputData = {
    "user_name": "lukicama",
    "user_pass": "test12345",
    "bet_type": 0,
    "url": "https://www.lutrija.hr/lotokladenjestaro",
    "result_url": "https://www.lutrija.hr/igraj/user/gamesHistory.html",
    "maxNum_A": 4,
    "maxNum_B": 5,
    "maxNum_C": 5,
    "initialStake": 2,
    "nextStake": 2,
    "money_risk": 100
}

time_run = []

array_a = [1, 2, 4, 3, 9, 7, 3, 5, 4]
array_b = [1, 2, 4, 5, 7, 5, 3, 4, 5, 4, 8, 2]

# calc class
class Interface:

    def __init__(self, master):
        
        """
        self.bot = Bettingbot(inputData["user_name"], inputData["user_pass"], inputData["url"], 
                              inputData["bet_type"], inputData["maxNum_A"], inputData["maxNum_B"], inputData["maxNum_C"],
                              inputData["nextStake"], inputData["result_url"], inputData["money_risk"] )
        """
        self.bet_type = StringVar()
        self.maxA = StringVar()
        self.maxB = StringVar()
        self.maxC = StringVar()
        self.moneyrisk = StringVar()
        self.initialstake = StringVar()
        
        self.nextstake = StringVar()
        self.accountmoney = StringVar()
        self.statusA = StringVar()
        self.statusB = StringVar()
        self.statusC = StringVar()
        self.Trigger = StringVar()
          
        master.title('Bot program')
        master.geometry('400x600+600+300')
        
        self.input_frame = LabelFrame(master, width=600, height=500, text='Input Data', pady=20)
        self.input_frame.pack(side=TOP)
        self.output_frame = LabelFrame(master, width=600, height=500, text='Output Data', pady=20)
        self.output_frame.pack()
    
        self.l_type = Label(self.input_frame, text="Bet type", font=("Arial Bold", 14))
        self.l_type.grid(row=0, column=0)
        self.e_type = Entry(self.input_frame, textvariable=self.bet_type)
        self.e_type.grid(row=0, column=1, columnspan=3, pady=3)
        self.e_type.focus_set()  # Sets focus on the input text area

        self.l_Amax = Label(self.input_frame, text="A limit", font=("Arial Bold", 14))
        self.l_Amax.grid(row=1, column=0)
        self.e_Amax = Entry(self.input_frame, textvariable=self.maxA)
        self.e_Amax.grid(row=1, column=1, columnspan=3, pady=3)
        self.e_Amax.focus_set()  # Sets focus on the input text area

        self.l_Bmax = Label(self.input_frame, text="B limit", font=("Arial Bold", 14))
        self.l_Bmax.grid(row=2, column=0)
        self.e_Bmax = Entry(self.input_frame, textvariable=self.maxB)
        self.e_Bmax.grid(row=2, column=1, columnspan=3, pady=3)
        self.e_Bmax.focus_set()  # Sets focus on the input text area

        self.l_Cmax = Label(self.input_frame, text="C limit", font=("Arial Bold", 14))
        self.l_Cmax.grid(row=3, column=0)
        self.e_Cmax = Entry(self.input_frame, textvariable=self.maxC)
        self.e_Cmax.grid(row=3, column=1, columnspan=3, pady=3)
        self.e_Cmax.focus_set()  # Sets focus on the input text area
        
        self.l_moneyrisk = Label(self.input_frame, text="Money risk", font=("Arial Bold", 14))
        self.l_moneyrisk.grid(row=4, column=0)
        self.e_moneyrisk = Entry(self.input_frame, textvariable=self.moneyrisk)
        self.e_moneyrisk.grid(row=4, column=1, columnspan=3, pady=3)
        self.e_moneyrisk.focus_set()  # Sets focus on the input text area

        self.l_initialstake = Label(self.input_frame, text="Initial stake", font=("Arial Bold", 14))
        self.l_initialstake.grid(row=5, column=0)
        self.e_initialstake = Entry(self.input_frame, textvariable=self.initialstake)
        self.e_initialstake.grid(row=5, column=1, columnspan=1, pady=3)

        self.b_start = Button(self.input_frame, text="Start", cursor="circle", width=6, height=2, command=self.start)
        self.b_start.grid(row=6, column=0, columnspan=2, pady=3)

        # output
        self.l_accountMoney = Label(self.output_frame, text="Left  money", font=("Arial Bold", 14))
        self.l_accountMoney.grid(row=0, column=3)
        self.e_accountMoney = Entry(self.output_frame, state="readonly")
        self.e_accountMoney.grid(row=0, column=4, columnspan=3, pady=3)

        self.l_statusA = Label(self.output_frame, text="A status", font=("Arial Bold", 14))
        self.l_statusA.grid(row=1, column=3)
        self.e_statusA = Entry(self.output_frame, state="readonly")
        self.e_statusA.grid(row=1, column=4, columnspan=3, pady=3)

        self.l_statusB = Label(self.output_frame, text="B status", font=("Arial Bold", 14))
        self.l_statusB.grid(row=2, column=3)
        self.e_statusB = Entry(self.output_frame, state="readonly")
        self.e_statusB.grid(row=2, column=4, columnspan=3, pady=3)

        self.l_statusC = Label(self.output_frame, text="C status", font=("Arial Bold", 14))
        self.l_statusC.grid(row=3, column=3)
        self.e_statusC = Entry(self.output_frame, state="readonly")
        self.e_statusC.grid(row=3, column=4, columnspan=3, pady=3)
        
        self.l_nextstake = Label(self.output_frame, text="Next stake", font=("Arial Bold", 14))
        self.l_nextstake.grid(row=4, column=3)
        self.e_nextstake = Entry(self.output_frame, textvariable=self.nextstake)
        self.e_nextstake.grid(row=4, column=4, columnspan=1, pady=3)

        self.l_trigger = Label(self.output_frame, text="Trigger", font=("Arial Bold", 14))
        self.l_trigger.grid(row=5, column=3)
        self.e_trigger = Entry(self.output_frame, state="readonly")
        self.e_trigger.grid(row=5, column=4, columnspan=3, pady=3)

        self.b_stop = Button(self.output_frame, text="Stop", cursor="circle", command=self.stop, state=DISABLED, width=6, height=2)
        self.b_stop.grid(row=6, column=4, columnspan=2, pady=3)
    
    def start(self):
        is_validated = self.validation()
        if is_validated:
            print(int(self.bet_type.get()))
            self.set_inputData()
            self.b_start['state'] = 'disabled'
            self.b_stop['state'] = 'normal'
            
            username = inputData["user_name"]
            password = inputData["user_pass"]
            site_url = "https://www.lutrija.hr/lotokladenjestaro"
            result_url = "https://www.lutrija.hr/igraj/user/gamesHistory.html"
            bet_type = inputData["bet_type"]
            maxNum_A = inputData["maxNum_A"]
            maxNum_B = inputData["maxNum_B"]
            maxNum_C = inputData["maxNum_C"]
            initialstake = inputData["initialstake"]
            money_risk = inputData["money_risk"]

            self.bot.set_inputData(bet_type, maxNum_A, maxNum_B, maxNum_C, initialstake, money_risk)
        #    bot = Bettingbot(username, password, site_url, bet_type, maxNum_A, maxNum_B, maxNum_C, nextStake, result_url, money_risk)
            self.bot.set_ka(array_a)
            self.bot.set_kb(array_b)

            self.bot.login()
            self.bot.get_accountmoney()
            self.outputData()
            self.bot.get_nextstake(self.bot.statusA, self.bot.statusB)
            self.bot.bet_hungary()
    #       bot.bet_italy()
            self.bot.get_result()
            self.bot.get_status()
            
    def stop(self):
        self.bot.closedriver()
        self.b_stop['state'] = 'disabled' 
        self.b_start['state'] = 'normal'
        self.reset()       
    
    def set_inputData(self):
        inputData["bet_type"] = int(self.bet_type.get())
        inputData["maxNum_A"] = int(self.maxA.get())
        inputData["maxNum_B"] = int(self.maxB.get())
        inputData["maxNum_C"] = int(self.maxC.get())
        inputData["initialstake"] = int(self.initialstake.get())
        inputData["money_risk"] = int(self.moneyrisk.get())
        
    def reset(self):
        self.maxA.set("")
        self.maxB.set("")
        self.maxC.set("")
        self.initialstake.set("")
        self.bet_type.set("")
        self.moneyrisk.set("")
        
    def outputData(self):
        self.nextstake.set(str(self.bot.nextStake))
        self.accountmoney.set(str(self.bot.money_onAccount))
        self.statusA.set(str(self.bot.statusA))
        self.statusB.set(str(self.bot.statusB))
        self.statusC.set(str(self.bot.statusC))
        self.Trigger.set(str(self.bot.trigger))
        
    def validation(self):
        maxA = self.maxA.get()
        maxB = self.maxB.get()
        maxC = self.maxC.get()
        bet_type = self.bet_type.get()
        initialstake = self.initialstake.get()
        moneyrisk = self.moneyrisk.get()
        if maxA.isdigit() and maxB.isdigit() and maxC.isdigit() and bet_type.isdigit() and initialstake.isdigit() and moneyrisk.isdigit():
            if int(bet_type) == 0 or int(bet_type) == 1:
                print("ok")
                print(bet_type, maxA, maxB, maxC, initialstake)
                return True
            else:
                tkinter.messagebox.showwarning("Validation Error", "Bet type must be 0 or 1")
                return False
        else:
            tkinter.messagebox.showwarning("Validation Error", "Input only number!")
            self.reset()
            return False
            
if __name__ == '__main__':
    root = Tk()
    obj = Interface(root)  # object instantiated
    root.mainloop()
    
