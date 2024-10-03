import socket
import threading
import matplotlib.pyplot as plt
from time import sleep, time, strftime, localtime
from sys import exit
import numpy as np
from csv import reader

plt.rcParams['font.sans-serif'] = ['SimHei']  # 表格中文
plt.rcParams['axes.unicode_minus'] = False

# 记录各个部分连接的的端口
port_esp = 2333
port_mobile = 2233

# 建项目文件夹同路径下的文件夹，用于保存数据并记录时间
file_count = 0  # 当前文件数目
str_time = strftime('%Y-%m-%d, %H.%M.%S', localtime())  # 当前时间
dir_name = '../user_data/' + str_time
filename = ''


# mkdir(dir_name)  # 按照时间创建文件夹


# 画图的函数
def graph():
    sampling_rate = 125
    plt_len = 6
    global package_count
    # 先建立窗口
    if package_count == 0:
        plt.ion()
        plt.figure(figsize=(12, 5))
    else:
        if package_count % 1 == 0:  # 每几包画一个
            plot_data = list()
            with open(filename, 'r') as file:
                csv_reader = reader(file)
                for row in csv_reader:
                    plot_data.append(float(row[0].strip()))
            if len(plot_data) <= sampling_rate * plt_len:
                plt.plot(plot_data)
            else:
                plt.plot(plot_data[len(plot_data) - sampling_rate * plt_len:len(plot_data)])
            plt.title('波形')
            plt.xlabel('采样点')
            plt.ylabel('电压值')
            plt.axis([0, sampling_rate * plt_len, -2, 4])
            plt.pause(0.1)
            plt.clf()


# 文件保存函数，用于数据分割成多文件保存
def file_save(start_time):
    global file_count, filename
    total_package = 1000  # 程序停止时记录的包数
    package_length = 6  # 一包数据时长
    if file_count > total_package:
        exit(0)  # 程序出口
    if time() - start_time >= package_length:
        if file_count and file_count != 2:
            print("Unlocking......")
            sleep(0.2)
        else:
            if file_count and file_count != 2:
                print('\nIdentification unsuccessful.')
        file_count += 1
        filename = dir_name + '/file' + str(file_count) + '.csv'
        new_f = open(filename, 'w', newline='')
        print('\nSaving data in file' + str(file_count), end='')
        return new_f, time()
    else:
        if package_length > 10:
            graph()
        f = open(filename, 'a', newline='')
        return f, start_time


def handle_mobile(c_mobile, add_mobile):
    print("Client mobile:", add_mobile, "connected")
    while True:
        msg = ""
        c_mobile.send(msg.encode())
        sleep(0.2)
        msg = ""
        c_mobile.send(msg.encode())


def handle_esp(c_esp, add_esp):
    print("Client ESP8266:", add_esp, "connected")
    while True:
        data = c_esp.recv(2 ** 15).decode('utf-8')
        print(data, end='')
        if data[:4] == "plot":
            s = []
            for _ in range(800):
                s.append(c_esp.recv(2 ** 15).decode('utf-8'))
            s = np.array(s).flatten()
        msg = strftime('t%Y-%m-%d, %H.%M.%S', localtime())
        c_esp.send(msg.encode())


# use while for multi-connection
print("Server started. Waiting for connection")
s_esp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_esp.bind(("0.0.0.0", port_esp))
s_esp.listen()
client_esp, address_esp = s_esp.accept()
t1 = threading.Thread(target=handle_esp, args=(client_esp, address_esp))
t1.start()

s_mobile = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_mobile.bind(("0.0.0.0", port_mobile))
s_mobile.listen()
client_mo, address_mo = s_mobile.accept()
t2 = threading.Thread(target=handle_mobile, args=(client_mo, address_mo))
t2.start()
