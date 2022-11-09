from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
import serial
import serial.tools.list_ports
import time
import threading
#import tkinter.messagebox

class Win:
    
    i = 1
    status = 0
    decode_dict = {"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9}
    port_tupple = tuple(serial.tools.list_ports.comports())
    baud_tupple = ('9600','19200','38400','57600','115200')
    databit_tupple = ('6','7','8')
    checkbit_tupple = ('None','奇校验','偶校验')
    stopbit_tupple = ('1','2')
    serial_port = ''
    thread_flag = 0

    def __init__(self):
        self.root = self.__win()
        self.tk_label_log_label = self.__tk_label_log_label()
        self.tk_text_log_box = self.__tk_text_log_box()
        self.tk_label_send_label = self.__tk_label_send_label()
        self.tk_button_send_button = self.__tk_button_send_button()
        self.tk_button_sendinhex_button = self.__tk_button_sendinhex_button()
        self.tk_input_send_box = self.__tk_input_send_box()
        self.tk_label_port = self.__tk_label_port()
        self.tk_select_box_port_m = self.__tk_select_box_port_m()
        self.tk_label_baud = self.__tk_label_baud()
        self.tk_label_data_bit = self.__tk_label_data_bit()
        self.tk_label_stop_bit = self.__tk_label_stop_bit()
        self.tk_label_check_bit = self.__tk_label_check_bit()
        self.tk_select_box_baud_m = self.__tk_select_box_baud_m()
        self.tk_select_box_databit_m = self.__tk_select_box_databit_m()
        self.tk_select_box_stopbit_m = self.__tk_select_box_stopbit_m()
        self.tk_select_box_checkbit_m = self.__tk_select_box_checkbit_m()
        self.tk_button_run_button = self.__tk_button_run_button()
        self.tk_button_stop_button = self.__tk_button_stop_button()
        self.tk_button_clear_button = self.__tk_button_clear_button()

    def __win(self):
        root = Tk()
        root.title("Serialport_py")
        # 设置大小 居中展示
        width = 600
        height = 400
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(geometry)
        root.resizable(width=False, height=False)
        return root

    def show(self):
        self.root.mainloop()

    def __tk_label_log_label(self):
        label = Label(self.root,text="Log")
        label.place(x=180, y=24, width=50, height=24)
        return label

    def __tk_text_log_box(self):
        text = scrolledtext.ScrolledText(self.root)
        text.place(x=180, y=50, width=400, height=133)
        text.tag_add('send_tag','1.1','1.100')
        text.tag_config('send_tag',foreground='green')
        text.tag_add("receive_tag",'1.1','1.100')
        text.tag_config('receive_tag',foreground='purple')
        return text

    def __tk_label_send_label(self):
        label = Label(self.root,text="发送")
        label.place(x=180, y=214, width=50, height=24)
        return label

    def __tk_button_send_button(self):
        btn = Button(self.root, text="Send",command=self.send)
        btn.place(x=410, y=350, width=80, height=24)
        return btn

    def __tk_button_sendinhex_button(self):
        btn = Button(self.root, text="SendinHEX",command=self.sendinhex)
        btn.place(x=500, y=350, width=80, height=24)
        return btn

    def __tk_input_send_box(self):
        ipt = Entry(self.root)
        ipt.place(x=180, y=240, width=400, height=96)
        return ipt

    def __tk_label_port(self):
        label = Label(self.root,text="端口")
        label.place(x=24, y=40, width=35, height=24)
        return label

    def __tk_select_box_port_m(self):
        cb = Combobox(self.root, state="readonly")
        cb['values'] = self.port_tupple#("COM1", "COM2", "COM3")
        cb.place(x=80, y=40, width=80, height=24)
        return cb

    def __tk_label_baud(self):
        label = Label(self.root,text="波特率")
        label.place(x=10, y=80, width=50, height=24)
        return label

    def __tk_label_data_bit(self):
        label = Label(self.root,text="数据位")
        label.place(x=10, y=120, width=50, height=24)
        return label

    def __tk_label_stop_bit(self):
        label = Label(self.root,text="停止位")
        label.place(x=10, y=160, width=50, height=24)
        return label

    def __tk_label_check_bit(self):
        label = Label(self.root,text="校检位")
        label.place(x=10, y=200, width=50, height=24)
        return label

    def __tk_select_box_baud_m(self):
        cb = Combobox(self.root )#state="readonly"
        cb['values'] = (9600,19200,38400,56700,115200)#("下拉选择框", "Python", "Tkinter Helper")
        cb.place(x=80, y=80, width=80, height=24)
        return cb

    def __tk_select_box_databit_m(self):
        cb = Combobox(self.root, state="readonly")
        cb['values'] = self.databit_tupple#("下拉选择框", "Python", "Tkinter Helper")
        cb.place(x=80, y=120, width=80, height=24)
        return cb

    def __tk_select_box_stopbit_m(self):
        cb = Combobox(self.root, state="readonly")
        cb['values'] = self.stopbit_tupple#("下拉选择框", "Python", "Tkinter Helper")
        cb.place(x=80, y=160, width=80, height=24)
        return cb

    def __tk_select_box_checkbit_m(self):
        cb = Combobox(self.root, state="readonly")
        cb['values'] = self.checkbit_tupple#("下拉选择框", "Python", "Tkinter Helper")
        cb.place(x=80, y=200, width=80, height=24)
        return cb

    def __tk_button_run_button(self):
        btn = Button(self.root, text="Run",command=self.run)
        btn.place(x=30, y=250, width=121, height=24)
        return btn

    def __tk_button_stop_button(self):
        btn = Button(self.root, text="Stop",command=self.stop)
        btn.place(x=30, y=290, width=119, height=24)
        return btn

    def __tk_button_clear_button(self):
        btn = Button(self.root, text="Clear",command=self.clear)
        btn.place(x=500, y=190, width=80, height=24)
        return btn

    def run(self):
        self.thread_flag = 1
        com_r = self.tk_select_box_port_m.get()       #com_r = self.__tk_select_box_port_m,则com_r为函数
        com_r = com_r[0:4]                               #com_r = self.__tk_select_box_port_m()，则com_r为函数返回值

        baudrate_r = self.tk_select_box_baud_m.get()
        j = 1
        temp = 0
        for _ in reversed(baudrate_r):                    #将波特率字符串转为10进制值
            temp = self.decode_dict[_] * j + temp
            j = j * 10
        parity_r = self.tk_select_box_checkbit_m.get()
        if parity_r == "None":
            parity_r = "N"
        elif parity_r == "奇校验":
            parity_r = "E"
        else:
            parity_r = "O"
        
        databit_r = self.tk_select_box_databit_m.get()
        databit_r = self.decode_dict[databit_r]
        stopbit_r = self.tk_select_box_stopbit_m.get()
        stopbit_r = self.decode_dict[stopbit_r]
        #try:
        self.serial_port = serial.Serial(com_r,baudrate=temp,parity=parity_r,bytesize=databit_r,stopbits=stopbit_r,timeout=2)
        self.tk_text_log_box.insert(END,"\n串口已打开\n")
        self.start_thread()
        self.status = 1                              #串口的状态位需在开启串口后方可置1（表示串口已打开）
        #except serial.serialutil.SerialException:
            #self.tk_text_log_box.insert(END,"\n串口已被占用\n")

    
    def stop(self):
        if self.serial_port:
            #print("准备关闭线程！")
            self.stop_thread()
            #print("aiguo")
            self.serial_port.close()
            self.status = 0
            self.tk_text_log_box.insert(END,"\n串口已关闭\n")
        else:
            self.tk_text_log_box.insert(END,"\n串口未打开\n")

    def clear(self):
        self.tk_text_log_box.delete(1.0,END)
    
    def send(self):
        if self.status:
            text = self.tk_input_send_box.get()
            if text:
                self.serial_port.write(text.encode("utf-8"))
                send_str = time.asctime(time.localtime(time.time())) + " send :" + text + '\n'          #记录发送内容
                self.tk_text_log_box.insert(END,send_str,'send_tag')
            else:
                self.tk_text_log_box.insert(END,"\n发送内容不能为空\n")
        else:
            self.tk_text_log_box.insert(END,"\n串口未打开\n")
    
    def sendinhex(self):
        pass

    
    def receive_data(self):
        try:
            while(True):
                if self.serial_port and self.serial_port.in_waiting:
                    text = self.serial_port.read(self.serial_port.in_waiting)
                    #print("Receive thread is working.")
                    receive_str = time.asctime(time.localtime(time.time())) + " receive:" + text.decode('utf-8') + '\n'
                    self.tk_text_log_box.insert(END,receive_str,'receive_tag')
                #else:
                    #print("串口未打开或无数据接收\n")
                    #time.sleep(0.5)
                    #continue
        except OSError:
            print("串口已关闭")

    
    def start_thread(self):                        #启动接收线程的函数
        if self.thread_flag:
            self.ReceiveUartThread = threading.Thread(target=self.receive_data)
            self.ReceiveUartThread.start()
            print("线程启动！")
        #return ReceiveUartThread
    
    
    def stop_thread(self):
        try:
            if self.thread_flag:
                self.ReceiveUartThread.join(1)         #注意：join的参数为timeout，此参数不能为空，否则关闭线程会卡死python
                print("线程关闭")
                self.thread_flag = 0
            else:
                self.tk_text_log_box.insert(END,"线程未启动。\n")
        except OSError:
            pass
    
    

if __name__ == "__main__":
    win = Win()
    # TODO 绑定点击事件或其他逻辑处理
    #win.start_thread()
    win.show()
