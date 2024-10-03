from mul_net import MulNet
import jittor as jt
import tkinter as tk

jt.flags.use_cuda = 1


class MulWin:
    def __init__(self, master):
        self.master = master
        master.title("拟合乘法器")
        master.geometry("250x120")

        self.label1 = tk.Label(master, text="x：")
        self.label1.grid(row=0, column=0, sticky="e")

        self.label2 = tk.Label(master, text="y：")
        self.label2.grid(row=1, column=0, sticky="e")

        self.entry1 = tk.Entry(master)
        self.entry1.grid(row=0, column=1, sticky="w")

        self.entry2 = tk.Entry(master)
        self.entry2.grid(row=1, column=1, sticky="w")

        self.button = tk.Button(master, text="计算", command=self.calculate)
        self.button.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.result = tk.Label(master, text="")
        self.result.grid(row=3, column=0, columnspan=2, sticky="nsew")

        self.model = MulNet()
        self.model.load('multiplier.pkl')

        master.grid_rowconfigure(2, weight=1)
        master.grid_rowconfigure(3, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

    def calculate(self):
        try:
            x = float(self.entry1.get())
            y = float(self.entry2.get())
            result = self.model(jt.array((x / max(x, y) / 2, y / max(x, y) / 2))) * max(x, y) ** 2 * 4
            self.result.config(text=f"model(x, y)={result:.2f}")
        except ValueError:
            self.result.config(text="输入有误，请输入数字。")


if __name__ == '__main__':
    root = tk.Tk()
    multiplier = MulWin(root)
    root.mainloop()
