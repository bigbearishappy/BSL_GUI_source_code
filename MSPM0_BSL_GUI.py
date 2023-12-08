import tkinter
from tkinter import *
from tkinter.filedialog import *
import platform
from get_file import *
from BSL_pack import *
from UART_send import *
from I2C_send import *
import time
import os
from txt_to_h import *
from glob import glob


class Tkinter_app:
    def __init__(self, master):
        self.passwordfile = b""
        self.firmwaredfile = ""
        self.xds_v = tkinter.StringVar(None, "a")
        # self.xds_r = tkinter.StringVar(None, '1')
        menubar = Menu(master, tearoff=0)
        #        menubar.add_command(label='MoreOption')
        menufile = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="MoreOption", menu=menufile)
        #        menufile.add_command(label='Create Linker Files', command=self.create_linker)
        menufile.add_command(label="TXT_to_H", command=self.txt_h)
        menufile.add_command(label="Update XDS110 firmware", command=self.update_xds110)
        master["menu"] = menubar

        # menubar.config(bg='red')
        #   menubar.pack()

        # variable = StringVar(master)
        # variable.set("one")  # default value
        # w = OptionMenu(master, variable, "one", "two", "three")
        # w.config(bg="gray")  # Set background color to green
        # w.pack()

        frame0 = Frame(master)
        frame0.pack(padx=50, pady=20, anchor=E)
        frame1 = Frame(master)
        frame1.pack(padx=50, anchor=E)
        frame3 = Frame(master)
        frame3.pack(pady=10, fill=X)
        frame4 = Frame(master)
        frame4.pack()
        frame5 = Frame(master)
        frame5.pack()
        # frame6 = Frame(master)
        # frame6.pack(padx=1, pady=20, anchor=E)
        frame2 = Frame(master)
        frame2.pack(side="bottom")

        self.label0 = Label(frame0, text="Application firmware file:")
        self.label0.pack(side="left")
        global input_name
        input_name = StringVar()
        self.entry = Entry(frame0, width=50, textvariable=input_name)
        self.entry.pack(side="left")
        self.button = Button(frame0, text="Choose .txt file", command=self.choosefile)
        self.button.pack(side="left")

        self.label1 = Label(frame1, text="Password file:")
        self.label1.pack(side="left")
        global input_name1
        input_name1 = StringVar()
        self.entry1 = Entry(frame1, width=50, textvariable=input_name1)
        self.entry1.pack(side="left")
        self.button1 = Button(frame1, text="Choose .txt file", command=self.choosefile1)
        self.button1.pack(side="left")

        global photo
        #        photo = PhotoImage(file=SETUP_DIR + "\imag\oi.GIF")
        #photo = PhotoImage(file="imag\oi.GIF")
        #self.label2 = Label(frame2, image=photo)
        #self.label2.pack()

        self.button = Button(frame3, text="Download", command=self.download)
        self.button.pack()

        #self.label3 = Label(frame3, text="(Download: Just support UART with XDS110)")
        #self.label3.pack()

        self.rad_button = Radiobutton(
            frame3,
            text="I2C",
            variable=self.xds_v,
            value="a",
            command=self.xds110_LP,
        )
        self.rad_button.place(relx=0.6, rely=0)

        self.selected_port = "default"
        self.var = StringVar(frame3)
        self.var.trace_add("write", self.on_dropdown_change)
        i2c_devices = glob('/dev/i2c-*')
        self.dropdown_box = OptionMenu(frame3, self.var, *i2c_devices)
        self.dropdown_box.place(relx=0.7, rely=0)

        #self.rad_button2 = Radiobutton(
        #    frame3,
        #    text="Standalone XDS110",
        #    variable=self.xds_v,
        #    value="b",
        #    command=self.xds110_S,
        #)
        #self.rad_button2.place(relx=0.7, rely=0.5)

        # self.rad_button3 = Radiobutton(frame3, text='BOOTRST', variable=self.xds_r, value='1', command=self.xds110_BR)
        # self.rad_button3.place(relx=0.1,rely=0)
        # self.rad_button4 = Radiobutton(frame3, text='POR', variable=self.xds_r, value='2', command=self.xds110_PR)
        # self.rad_button4.place(relx=0.1,rely=0.5)

        self.s1 = Scrollbar(frame4)
        self.s1.pack(side=RIGHT, fill=Y)
        self.textlog = Text(
            frame4, yscrollcommand=self.s1.set, width=70, height=15, bg="white"
        )
        self.s1.config(command=self.textlog.yview)
        self.textlog.pack()

        self.textlog.insert(
            INSERT, "This GUI is developed with Python version: 3.10.4\n"
        )
        self.textlog.insert(INSERT, "Default hardware is XDS110 on Launchpad.\n")
        # self.textlog.insert(INSERT, 'Default reset type is boot reset.\n')
        #        self.textlog.insert(INSERT, "Python version: "+platform.python_version() + '\n')
        self.textlog.tag_config("error", foreground="red")
        self.textlog.tag_config("pass", foreground="green")
        self.textlog.tag_config("normal", foreground="black")
        self.textlog.config(state=DISABLED)

        self.button_c = Button(frame5, text="Clear", command=self.clear_text)
        self.button_c.pack()

        self.connection_pack = BSL_pack.connection_pack()
        self.get_ID_pack = BSL_pack.get_ID_pack()
        self.password_pack = b""
        self.mass_erase_pack = BSL_pack.mass_erase_pack()
        self.firmware_pack = b""
        self.start_app_pack = BSL_pack.start_app_pack()
        self.path = os.getcwd()

    def on_dropdown_change(self, *args):
        self.selected_port = self.var.get()
        print(f"select port:{self.var.get()}")

    def xds110_LP(self):
        self.textlog.config(state=NORMAL)
        self.textlog.insert(
            INSERT, "Changed the hardware bridge to XDS110 on Launchpad.\n", "normal"
        )
        self.textlog.config(state=DISABLED)

    def xds110_S(self):
        self.textlog.config(state=NORMAL)
        self.textlog.insert(
            INSERT, "Changed the hardware bridge to standalone XDS110.\n", "normal"
        )
        self.textlog.config(state=DISABLED)

    def xds110_BR(self):
        self.textlog.config(state=NORMAL)
        self.textlog.insert(INSERT, "Changed reset type to boot reset.\n", "normal")
        self.textlog.config(state=DISABLED)

    def xds110_PR(self):
        self.textlog.config(state=NORMAL)
        self.textlog.insert(INSERT, "Changed reset type to power on reset.\n", "normal")
        self.textlog.config(state=DISABLED)

    def choosefile(self):
        f = askopenfilename(
            title="Choose a firmware file",
            initialdir="c:",
            filetypes=[("textfile", ".txt")],
        )
        input_name.set(f)
        self.textlog.config(state=NORMAL)
        if f:
            self.textlog.insert(
                INSERT, "Choose a firmware file at:" + f + "\n", "normal"
            )
            self.firmwaredfile = file_d.get_firmware(f)
            self.firmware_pack = BSL_pack.firmware_pack(self.firmwaredfile)
        else:
            self.textlog.insert(
                INSERT, "Error: Please choose a firmware file.\n", "error"
            )
            self.firmwaredfile = ""
            self.firmware_pack = b""
        self.textlog.see(END)
        self.textlog.config(state=DISABLED)

    def choosefile1(self):
        f1 = askopenfilename(
            title="Choose a password file",
            initialdir="c:",
            filetypes=[("textfile", ".txt")],
        )
        input_name1.set(f1)
        self.textlog.config(state=NORMAL)
        if f1:
            self.textlog.insert(
                INSERT, "Choose a password file at:" + f1 + "\n", "normal"
            )
            self.passwordfile = b""
            self.passwordfile = file_d.get_password(f1)
            if self.passwordfile == b"":
                self.textlog.insert(
                    INSERT, "Error: Password format is not correct!\n", "error"
                )
            else:
                self.password_pack = BSL_pack.password_pack(self.passwordfile)
        else:
            self.passwordfile = b""
            self.textlog.insert(
                INSERT, "Error: Please choose a password file.\n", "error"
            )

        # else:
        #     print(self.passwordfile)
        self.textlog.see(END)
        self.textlog.config(state=DISABLED)

    def download(self):
        self.textlog.config(state=NORMAL)
        if self.passwordfile != b"" and self.firmwaredfile != "":
            #if self.xds_v.get() == "a":
            #    os.system(
            #        self.path
            #        + "/common/uscif/dbgjtag.exe  -f @xds110 -Y gpiopins, config=0x1, write=0x1"
            #    )
            #    os.system(self.path + "/common/uscif/xds110/xds110reset.exe -d 1400")
            #    # if self.xds_r.get() == '2':
            #    #     os.system(self.path + "/common/uscif/xds110/xds110reset.exe -d 1300")
            #    # else:
            #    #     os.system(self.path + "/common/uscif/xds110/xds110reset.exe")
            #else:
            #    if self.xds_v.get() == "b":
            #        os.system(
            #            self.path
            #            + "/common/uscif/dbgjtag.exe -f @xds110 -Y power,supply=on,voltage=3.2"
            #        )
            #        os.system(
            #            self.path
            #            + "/common/uscif/dbgjtag.exe -f @xds110 -Y gpiopins, config=0x3, write=0x02"
            #        )
            #        time.sleep(1.4)
            #        os.system(
            #            self.path
            #            + "/common/uscif/dbgjtag.exe -f @xds110 -Y gpiopins, config=0x3, write=0x03"
            #        )
            #        # if self.xds_r.get() == '2':
            #        #     os.system(
            #        #         self.path + "/common/uscif/dbgjtag.exe -f @xds110 -Y gpiopins, config=0x3, write=0x02")
            #        #     time.sleep(1.3)
            #        #     os.system(
            #        #         self.path + "/common/uscif/dbgjtag.exe -f @xds110 -Y gpiopins, config=0x3, write=0x03")
            #        # else:
            #        #     os.system(
            #        #         self.path + "/common/uscif/dbgjtag.exe -f @xds110 -Y gpiopins, config=0x3, write=0x02")
            #        #     time.sleep(0.1)
            #        #     os.system(
            #        #         self.path + "/common/uscif/dbgjtag.exe -f @xds110 -Y gpiopins, config=0x3, write=0x03")
            #    else:
            #        # print(self.xds_v.get())
            #        self.textlog.insert(
            #            INSERT, "No correct hardware bridge selected.\n", "error"
            #        )
            #find_flag = UART_S.find_MSP_COM()
            if self.selected_port != "default":
                # self.textlog.insert(
                #     INSERT, "Find MSP COM port:" + find_flag + "\n", "normal"
                # )
                # ser_port = UART_S.config_uart(find_flag)
                # self.textlog.insert(
                #     INSERT,
                #     "Configure UART: 9600 baudrate, 8 data bits (LSB first), no parity, and 1 stop bit.\n",
                #     "normal",
                # )
                #UART_S.send_data(ser_port, self.connection_pack)
                #response_ = UART_S.read_data(ser_port, 1)
                #I2C_S.send_data(self.connection_pack[0], self.connection_pack[1:])
                I2C_S.config_i2c(0x48, int(self.selected_port.split("-")[-1]))
                I2C_S.send_data(list(self.connection_pack)[0], list(self.connection_pack)[1:])
                response_ = I2C_S.read_data(0, 1)
                #if self.xds_v.get() == "a":
                #    os.system(
                #        self.path
                #        + "/common/uscif/dbgjtag.exe  -f @xds110 -Y gpiopins, config=0x1, write=0x0"
                #    )
                #else:
                #    if self.xds_v.get() == "b":
                #        os.system(
                #            self.path
                #            + "/common/uscif/dbgjtag.exe -f @xds110 -Y gpiopins, config=0x3, write=0x01"
                #        )
                #UART_S.send_data(ser_port, b"\xbb")
                #response01 = UART_S.read_data(ser_port, 1)
                I2C_S.send_data(0, [0xbb])
                response01 = I2C_S.read_data(0, 1)
                if response01 == "51":
                    self.textlog.insert(
                        INSERT, "MSPM0 is in BSL mode.\nGet device ID...\n", "normal"
                    )
                    #UART_S.send_data(ser_port, self.get_ID_pack)
                    #response1 = UART_S.read_data(ser_port, 33)
                    I2C_S.send_data(list(self.get_ID_pack)[0], list(self.get_ID_pack)[1:])
                    response1 = I2C_S.read_data(0, 33)
                    self.textlog.insert(INSERT, "Send the password...\n", "normal")
                    #UART_S.send_data(ser_port, self.password_pack)
                    #response2 = UART_S.read_data(ser_port, 1)
                    I2C_S.send_data(list(self.password_pack)[0], list(self.password_pack)[1:])
                    response2 = I2C_S.read_data(0, 1)
                    check = self.check_pack(response2)
                    if check:
                        #response2 = UART_S.read_data(ser_port, 9)
                        response2 = I2C_S.read_data(0, 9)
                        check2 = self.check_reponse(response2[8:10])
                        # print(response2[8:10])
                        if check2:
                            self.textlog.insert(INSERT, "Mass erase...\n", "normal")
                            #UART_S.send_data(ser_port, self.mass_erase_pack)
                            #response2 = UART_S.read_data(ser_port, 1)
                            #response2 = UART_S.read_data(ser_port, 9)
                            I2C_S.send_data(list(self.mass_erase_pack)[0], list(self.mass_erase_pack)[1:])
                            response2 = I2C_S.read_data(0, 1)
                            response2 = I2C_S.read_data(0, 9)
                            self.textlog.insert(
                                INSERT, "Send the firmware...\n", "normal"
                            )
                            # print(type(firmware_pack))
                            # print(firmware_pack)
                            for list_code in self.firmware_pack:
                                #UART_S.send_data(ser_port, list_code)
                                #response3 = UART_S.read_data(ser_port, 1)
                                I2C_S.send_data(list(list_code)[0], list(list_code)[1:])
                                response3 = I2C_S.read_data(0, 1)
                                check = self.check_pack(response3)
                                if check:
                                    #response3 = UART_S.read_data(ser_port, 9)
                                    response3 = I2C_S.read_data(0, 9)
                                    check3 = self.check_reponse(response3[8:10])
                                    if check3:
                                        pass
                                    else:
                                        break
                                else:
                                    break
                            if check:
                                self.textlog.insert(
                                    INSERT, "Send firmware successfully!\n", "normal"
                                )
                                self.textlog.insert(
                                    INSERT,
                                    "Boot reset the device to start application ...\n",
                                    "normal",
                                )
                                self.textlog.insert(
                                    INSERT,
                                    "-----------Download finished!----------\n",
                                    "pass",
                                )
                                #UART_S.send_data(ser_port, self.start_app_pack)
                                #response3 = UART_S.read_data(ser_port, 1)
                                I2C_S.send_data(list(self.start_app_pack)[0], list(self.start_app_pack)[1:])
                                response3 = I2C_S.read_data(0, 1)
                    else:
                        self.textlog.insert(INSERT, "Error: No response！\n", "error")
                else:
                    self.textlog.insert(INSERT, "Error: No response！\n", "error")
            else:
                self.textlog.insert(
                    INSERT, "Error: Can not find MSP COM port!\n", "error"
                )
        else:
            self.textlog.insert(
                INSERT, "Error: please choose all files above!\n", "error"
            )
        self.textlog.see(END)
        self.textlog.config(state=DISABLED)

    def clear_text(self):
        self.textlog.config(state=NORMAL)
        self.textlog.delete("2.0", "end")
        self.textlog.insert(INSERT, "\n")
        self.textlog.config(state=DISABLED)

    def check_pack(self, pack_ack):
        flagg = 0
        #        self.textlog.config(state=NORMAL)
        if pack_ack == "00":
            flagg = 1
            self.textlog.insert(INSERT, "Send package successfully!\n", "normal")
        elif pack_ack == "51":
            self.textlog.insert(INSERT, "Error: Header incorrect!\n", "error")
        elif pack_ack == "52":
            self.textlog.insert(INSERT, "Error: Checksum incorrect!\n", "error")
        elif pack_ack == "53":
            self.textlog.insert(INSERT, "Error: Packet size zero!\n", "error")
        elif pack_ack == "54":
            self.textlog.insert(INSERT, "Error: Packet size too big!\n", "error")
        elif pack_ack == "55":
            self.textlog.insert(INSERT, "Error: Unknown error!\n", "error")
        elif pack_ack == "56":
            self.textlog.insert(INSERT, "Error: Unknown baud rate!\n", "error")
        else:
            self.textlog.insert(INSERT, "Error: Unknow else error!\n", "error")
        #       self.textlog.config(state=DISABLED)
        return flagg

    def check_reponse(self, pack_res):
        flagg = 0
        #       self.textlog.config(state=NORMAL)
        if pack_res == "00":
            flagg = 1
            self.textlog.insert(INSERT, "Operation success!\n", "normal")
        elif pack_res == "01":
            self.textlog.insert(INSERT, "Error: flash program failed!\n", "error")
        elif pack_res == "02":
            self.textlog.insert(INSERT, "Error: Mass Erase failed!\n", "error")
        elif pack_res == "04":
            self.textlog.insert(INSERT, "Error: BSL locked!!\n", "error")
        elif pack_res == "05":
            self.textlog.insert(INSERT, "Error: BSL password error!\n", "error")
        elif pack_res == "06":
            self.textlog.insert(
                INSERT, "Error: Multiple BSL password error!\n", "error"
            )
        elif pack_res == "07":
            self.textlog.insert(INSERT, "Error: Unknown Command!\n", "error")
        elif pack_res == "08":
            self.textlog.insert(INSERT, "Error: Invalid memory range!\n", "error")
        elif pack_res == "0B":
            self.textlog.insert(INSERT, "Error: Factory reset disabled!\n", "error")
        elif pack_res == "0C":
            self.textlog.insert(
                INSERT, "Error: Factory reset password error!\n", "error"
            )
        else:
            self.textlog.insert(INSERT, "Error: Unknow else error!\n", "error")
        return flagg

    #        self.textlog.config(state=DISABLED)

    def txt_h(self):
        sub_win1 = Toplevel(root)
        sub_win1.title("TXT to H")
        #        sub_win1.attributes("-topmost", True)
        sub_win1.geometry("700x350+300+200")
        sub_win1.grab_set()
        frames_0 = Frame(sub_win1)
        frames_0.pack(padx=50, pady=20, anchor=W)
        frames_1 = Frame(sub_win1)
        frames_1.pack(padx=50, anchor=W)
        frames_3 = Frame(sub_win1)
        frames_3.pack(pady=10)
        frames_4 = Frame(sub_win1)
        frames_4.pack()

        self.labelss0 = Label(frames_0, text="Choose a firmware .txt file")
        self.labelss0.pack(side="left")
        global input_name_ss
        input_name_ss = StringVar()
        self.entryss = Entry(frames_0, width=50, textvariable=input_name_ss)
        self.entryss.pack(side="left")
        self.buttonss = Button(
            frames_0, text="Choose .txt file", command=self.choosetxtfile
        )
        self.buttonss.pack(side="left")

        self.labelss1 = Label(frames_1, text="Choose a ouput folder:")
        self.labelss1.pack(side="left")
        global out_name_ss
        out_name_ss = StringVar()
        self.entryss1 = Entry(frames_1, width=50, textvariable=out_name_ss)
        self.entryss1.pack(side="left")
        self.buttonss1 = Button(frames_1, text="Scan", command=self.choosefile_out)
        self.buttonss1.pack(side="left")

        self.buttonss2 = Button(frames_3, text="Convert", command=self.convert_)
        self.buttonss2.pack()

        self.s3 = Scrollbar(frames_4)
        self.s3.pack(side=RIGHT, fill=Y)
        self.textlogsubs = Text(
            frames_4, yscrollcommand=self.s3.set, width=70, height=10, bg="white"
        )
        self.s3.config(command=self.textlogsubs.yview)
        self.textlogsubs.pack()
        self.textlogsubs.tag_config("errors_", foreground="red")
        self.textlogsubs.tag_config("pass_s_", foreground="green")
        self.textlogsubs.insert(
            INSERT, "This function is used for the situation that using MCU as host.\n"
        )
        self.textlogsubs.insert(
            INSERT, "The output header file is used for host MCU.\n"
        )
        self.textlogsubs.config(state=DISABLED)

    def choosetxtfile(self):
        fs = askopenfilename(
            title="Choose a firmware file",
            initialdir="c:",
            filetypes=[("textfile", ".txt")],
        )
        input_name_ss.set(fs)
        self.textlogsubs.config(state=NORMAL)
        if fs:
            self.textlogsubs.insert(
                INSERT, "Choose a firmware file at:" + fs + "\n", "normal"
            )
        else:
            self.textlogsubs.insert(
                INSERT, "Error: Please choose a firmware file.\n", "errors_"
            )
        self.textlogsubs.config(state=DISABLED)

    def choosefile_out(self):
        f3 = askdirectory()
        out_name_ss.set(f3)
        self.textlogsubs.config(state=NORMAL)
        if f3:
            self.textlogsubs.insert(INSERT, "Choose a output folder:" + f3 + "\n")
        else:
            self.textlogsubs.insert(
                INSERT, "Error: Please choose a output folder.\n", "errors_"
            )
        self.textlogsubs.config(state=DISABLED)

    def convert_(self):
        self.textlogsubs.config(state=NORMAL)
        input_names = input_name_ss.get()
        output_paths = out_name_ss.get()
        if input_names:
            if output_paths:
                self.textlogsubs.insert(INSERT, "Converting...\n")
                name_file = input_names.split("/")[-1]
                name_file2 = name_file.split(".")[0]
                output_paths_n = output_paths + "/" + name_file2 + ".h"
                Conver_F.conver_fun(input_names, output_paths_n)
                self.textlogsubs.insert(
                    INSERT,
                    "-----Convert the firmware to header file named "
                    + name_file2
                    + ".h!----\n ",
                    "pass_s_",
                )
            else:
                self.textlogsubs.insert(
                    INSERT, "Error: Please choose a output folder.\n", "errors_"
                )
        else:
            self.textlogsubs.insert(
                INSERT, "Error: Please choose a .txt firmware.\n", "errors_"
            )
        self.textlogsubs.config(state=DISABLED)

    def update_xds110(self):
        self.textlog.config(state=NORMAL)
        self.textlog.insert(
            INSERT, "Update the XDS110 firmware to version firmware_3.0.0.22...\n"
        )
        path = os.getcwd()
        print(path)
        os.system(path + "/common/uscif/xds110/xdsdfu.exe -m")
        time.sleep(0.5)
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        os.system(
            path
            + "/common/uscif/xds110/xdsdfu.exe -f "
            + path
            + "/common/uscif/xds110/firmware_3.0.0.22.bin -r"
        )
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        time.sleep(2)
        self.textlog.insert(INSERT, "XDS110 firmware update finished.\n", "pass")
        self.textlog.config(state=DISABLED)


if __name__ == "__main__":
    file_d = Get_files()
    BSL_pack = BSL_Pack()
    #UART_S = UART_send()
    I2C_S = I2C_send()
    Conver_F = TXT_to_h()
    root = Tk()
    #root.iconbitmap("imag/Capture.ico")
    root.geometry("700x520+500+500")
    root.title("MSPM0 Bootloader GUI  v1.0")
    app = Tkinter_app(root)
    root.mainloop()
