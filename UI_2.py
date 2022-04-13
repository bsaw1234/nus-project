from tkinter.ttk import Style

import matplotlib
import reco1
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import ttk
from mpl_toolkits.axisartist.axislines import Subplot

LARGE_FONT = ("Verdana", 12)
MED_FONT = ("Verdana", 8)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Recommendation System")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, UiPage):
            val = ''.join(args)
            frame = F(container, self, val)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    def show_frame_ui(self, cont):
        frame = self.frames[UiPage]
        cont.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller, val):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Recommendation System", font=LARGE_FONT)
        style = Style()
        style.configure('W.TButton', font=('calibri', 10, 'bold'),
                        foreground='blue')
        label.pack(pady=10, padx=10)
        label1 = tk.Label(self, text="Profile", font=MED_FONT)
        # label1.config(bg="yellow")
        label1.place(x=400, y=50)
        label1 = tk.Label(self, text="Customer", font=MED_FONT)
        label1.place(x=120, y=50)
        label1 = tk.Label(self, text="Amount", font=MED_FONT)
        label1.place(x=700, y=50)
        style = Style()
        style.configure('W.TButton', font=('calibri', 10, 'bold'),
                        foreground='blue')



        # button1.pack(side="top", padx=100, pady=20)
        df = pd.read_csv('D://matplot/pfolio2.csv')
        self.Customer = ttk.Combobox(self, values=list(df["Client"].unique()), state="readonly", style='W.TButton')
        self.Customer.place(x=200, y=50)

        self.Profile = ttk.Combobox(self, values=['Aggressive', 'Moderate', 'Considerate'], state="readonly", style='W.TButton')
        self.Profile.place(x=480, y=50)

        def getval():
            print(self.Customer.get())
            val=self.Customer.get()
            UiPage(self, self, val)
            #uio = UiPage(self, self, val)
            #print(uio,"obj")

            #controller.show_frame_ui(UiPage(self,self,val))

        button1 = ttk.Button(self, text="Submit Button", style='W.TButton',
                            command=lambda: controller.show_frame(UiPage))
        #button1 = ttk.Button(self, text="Submit Button", style='W.TButton',
         #                        command=getval)
        button1.place(x=900, y=50)



        T = tk.Text(self, height=0.75, width=8)
        T.place(x=800, y=50)


class UiPage(tk.Frame):

    def __init__(self, parent, controller, getval):
        tk.Frame.__init__(self, parent)
        self.getval = getval
        label = tk.Label(self, text="Recommendation System", font=LARGE_FONT)
        style = Style()
        style.configure('W.TButton', font=('calibri', 10, 'bold'),
                        foreground='blue')
        label.pack(pady=10, padx=10)
        label1 = tk.Label(self, text="Profile", font=MED_FONT)
        # label1.config(bg="yellow")
        label1.place(x=400, y=50)
        label1 = tk.Label(self, text="Customer", font=MED_FONT)
        label1.place(x=120, y=50)
        label1 = tk.Label(self, text="Amount", font=MED_FONT)
        label1.place(x=700, y=50)
        style = Style()
        style.configure('W.TButton', font=('calibri', 10, 'bold'),
                        foreground='blue')
        #Button for customer and profile
        button1 = ttk.Button(self, text="Submit Button", style='W.TButton',
                             command=lambda: controller.show_frame(UiPage))
        button1.place(x=900, y=50)
        df = pd.read_csv('D://matplot/pfolio2.csv')
        self.Customer = ttk.Combobox(self, values=list(df["Client"].unique()), state="readonly", style='W.TButton')
        self.Customer.place(x=200, y=50)

        self.Profile = ttk.Combobox(self, values=['Aggressive', 'Moderate', 'Considerate'], state="readonly", style='W.TButton')
        self.Profile.place(x=480, y=50)
        #Amount Text box
        T = tk.Text(self, height=0.75, width=8)
        T.place(x=800, y=50)

        f = Figure(figsize=(3, 3), dpi=100)
        ax = Subplot(f, 111)
        f.add_subplot(ax)

        ##USER INPUT TO FILTER DATA##
        df_line = df[df['Client'] == self.getval]
        if df_line.empty:
            df_line = df[df['Client'] == 'Suriya']

        xdata = list(df_line["Product"])
        ydata = list(df_line["Units"])
        ax.bar(xdata, ydata,  width=0.2, data=ydata)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=50, y=100)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=900, y=100)
        #Table data
        fig, ax = plt.subplots()
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')
        fig.set_figwidth(3)
        fig.set_figheight(3)
        df1 = reco1.merged_data3.copy()
        df1 = df1[['symbol', 'trend', 'Sentiment', 'curr_price', 'pred_price']]
        ax.table(cellText=df1.values, colLabels=df1.columns, loc='center', colWidths=[0.25,0.25,0.25,0.25,0.25])
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=500, y=100)
        #Hyperlink graph
        f3, a3 = plt.subplots()
        f3.patch.set_visible(False)
        f3.set_figwidth(3)
        f3.set_figheight(3)
        df_trend = pd.read_csv('D://matplot/stock_data.csv')
        Mon_date = df_trend["Date"]
        Trend = df_trend["AAL"]
        a3.plot(Mon_date, Trend, color='red', marker='o')
        canvas = FigureCanvasTkAgg(f3, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=500, y=300)

app = SeaofBTCapp()
app.mainloop()