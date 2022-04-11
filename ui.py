from tkinter.ttk import Style

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import ttk
from mpl_toolkits.axisartist.axislines import Subplot

LARGE_FONT = ("Verdana", 12)
MED_FONT = ("Verdana", 8)

import r1

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

        for F in (StartPage, PageThree):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
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
        button1 = ttk.Button(self, text="Submit Button", style='W.TButton',
                             command=r1 controller.show_frame(PageThree))
        button1.place(x=900, y=50)
        # button1.pack(side="top", padx=100, pady=20)

        df = pd.DataFrame({"currency": ["ER", "XCD", "ARS", "CAD"],
                           "volume": [400, 500, 600, 700]})
        self.Customer = ttk.Combobox(self, values=list(df["currency"].unique()), state="readonly", style='W.TButton')
        self.Customer.place(x=200, y=50)

        self.Profile = ttk.Combobox(self, values=list(df["volume"].unique()), state="readonly", style='W.TButton')
        self.Profile.place(x=480, y=50)

        T = tk.Text(self, height=0.75, width=8)
        T.place(x=800, y=50)


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
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
        button1 = ttk.Button(self, text="Submit Button", style='W.TButton',
                             command=lambda: controller.show_frame(PageThree))
        button1.place(x=900, y=50)
        # button1.pack(side="top", padx=100, pady=20)

        df = pd.DataFrame({"Stock": ["S1", "S2", "S3", "S4"],
                           "Trend": [400, 500, 600, 700]})
        self.Customer = ttk.Combobox(self, values=list(df["Stock"].unique()), state="readonly", style='W.TButton')
        self.Customer.place(x=200, y=50)

        self.Profile = ttk.Combobox(self, values=list(df["Trend"].unique()), state="readonly", style='W.TButton')
        self.Profile.place(x=480, y=50)

        T = tk.Text(self, height=0.75, width=8)
        T.place(x=800, y=50)

        f = Figure(figsize=(3, 3), dpi=100)
        # a = f.add_subplot(222)
        ax = Subplot(f, 111)
        f.add_subplot(ax)

        # x data:
        # df = pd.read_excel('D:\matplot\pfolio2.xlsx', sheet_name='pfolio2', engine='openpyxl', keep_default_na=False)
        xdata = ['S1', 'S2', 'S3']

        # y data:
        ydata = [100, 300, 500]
        ax.bar(xdata, ydata,  width=0.2, data=ydata)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=50, y=100)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=900, y=100)

        #f1 = Figure(figsize=(3, 3), dpi=100)
        # a = f.add_subplot(222)

        #ax1 = Subplot(f1, 111)
        #f1.add_subplot(ax1)
        #ax1.get_yaxis().set_visible(False)
        #ax1.axis('off')
        fig, ax = plt.subplots()

        # Hide axes without removing it:
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')
        fig.set_figwidth(3)
        fig.set_figheight(3)

        ax.table(cellText=df.values, colLabels=df.columns, loc='center')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=500, y=100)

        f3, a3 = plt.subplots()
        f3.set_figwidth(3)
        f3.set_figheight(3)
        Year = [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
        Unemployment_Rate = [5.6, 5.7, 5.4, 5.2, 5.9, 5, 5.5, 5.2, 5.5, 5.3]
        a3.plot(Year, Unemployment_Rate, color='red', marker='o')
        canvas = FigureCanvasTkAgg(f3, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=500, y=300)



        #toolbar = NavigationToolbar2TkAgg()
        #toolbar.update()
        #canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

app = SeaofBTCapp()
#app.mainloop()