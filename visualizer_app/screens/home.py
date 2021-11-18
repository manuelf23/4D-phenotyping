
import json
import sys
import os
file_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(f"{file_path}/../src")
from feno4D_visualizer import visualizer
import threading
from tkinter import Button, Entry, Frame, Label, StringVar
from tkinter import filedialog as FileDialog
from tkinter import messagebox as MessageBox


SEARCH_BUTTON = "Search"
FONT_H = "Helvetica 14 bold"
FG = "black"


def show_instructions():
    instructions = """
    INSTRUCTIONS

    When the graph appears press the following keys to change between different color spaces for the PCD.

            Key             Color space
            P  ------------ RGB
            O  ------------ DVI
            I  ------------ NDVI
            U  ------------ NDRE
            Y  ------------ SAVI
            T  ------------ MSAVI
             
    
    To continue press OK
    """
    MessageBox.showinfo("Instructions", instructions)


class Home(Frame):

    def __init__(self, controller, parent):

        Frame.__init__(self, parent)
        bg_color = '#EBEBEB'
        self.config(bg=bg_color)
        self.controller = controller
        self.parent = parent

        space_blank_banner = Frame(self, height=40, bg=bg_color)
        space_blank_banner.pack(fill='x')

        self.cache_file = f"{file_path}/../cache.json"
        if os.path.isfile(self.cache_file):
            self.f = open(self.cache_file, "r+")
            data = json.load(self.f)
            self.folderPath = StringVar()
            self.folderPath.set(data["4D_calibration"])
            self.folderPath_2 = StringVar()
            self.folderPath_2.set(data["geometric_calibration"])
            self.folderPath_3 = StringVar()
            self.folderPath_3.set(data["data_folder"])
            self.folderPath_4 = StringVar()
            self.folderPath_4.set(str(data["y_limit"][0]))
            self.folderPath_5 = StringVar()
            self.folderPath_5.set(str(data["y_limit"][1]))
            self.folderPath_6 = StringVar()
            self.folderPath_6.set(str(data["z_limit"][0]))
            self.folderPath_7 = StringVar()
            self.folderPath_7.set(str(data["z_limit"][1]))
            self.folderPath_8 = StringVar()
            self.folderPath_8.set(str(data["divisor"]))
            self.folderPath_9 = StringVar()
            self.folderPath_9.set(str(data["step_angle"]))
            self.folderPath_10 = StringVar()
            self.folderPath_10.set("")
            self.folderPath_11 = StringVar()
            self.folderPath_11.set("")

        else:
            self.f = open(self.cache_file, "w+")
            # paths var
            self.folderPath = StringVar()
            self.folderPath.set("")
            self.folderPath_2 = StringVar()
            self.folderPath_2.set("")
            self.folderPath_3 = StringVar()
            self.folderPath_3.set("")
            self.folderPath_4 = StringVar()
            self.folderPath_4.set("")
            self.folderPath_5 = StringVar()
            self.folderPath_5.set("")
            self.folderPath_6 = StringVar()
            self.folderPath_6.set("")
            self.folderPath_7 = StringVar()
            self.folderPath_7.set("")
            self.folderPath_8 = StringVar()
            self.folderPath_8.set("")
            self.folderPath_9 = StringVar()
            self.folderPath_9.set("")
            self.folderPath_10 = StringVar()
            self.folderPath_10.set("")
            self.folderPath_11 = StringVar()
            self.folderPath_11.set("")
            data_cache = {
                "data_folder": "",
                "geometric_calibration": "",
                "4D_calibration": "",
                "y_limit": ["", ""],
                "z_limit": ["", ""],
                "divisor": "",
                "step_angle": ""
            }
            json.dump(data_cache, self.f)
        self.f.close()
        # CALIB 1
        banner_path = Frame(self, height=40, bg=bg_color)
        banner_path.pack(fill='x')
        head_message = StringVar()
        head_message.set("4D calibration (Sensory Fusion)")
        head_text = Label(banner_path, textvariable=head_message,
                          fg=FG, font=FONT_H)
        head_text.pack()

        banner_entry = Frame(self, height=40, bg=bg_color)
        banner_entry.pack()

        search_text = StringVar()
        search_text.set(SEARCH_BUTTON)
        search_text_button = Button(
            banner_entry, textvariable=search_text, command=self.getFolderPath)
        search_text_button.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry = Entry(banner_entry, textvariable=self.folderPath)
        entry.config(state='disabled')
        entry.grid(row=0, column=1, padx=5, pady=5)
        entry.config(justify="center", state="disabled")
        # CALIB 1

        space_blank_banner = Frame(self, height=20, bg=bg_color)
        space_blank_banner.pack(fill='x')

        # CALIB 2
        banner_path = Frame(self, height=40, bg=bg_color)
        banner_path.pack(fill='x')
        head_message = StringVar()
        head_message.set("Geometric Calibration")
        head_text = Label(
            banner_path, textvariable=head_message, fg=FG, font=FONT_H)
        head_text.pack()
        banner_entry = Frame(self, height=40, bg=bg_color)
        banner_entry.pack()
        search_text = StringVar()
        search_text.set(SEARCH_BUTTON)
        search_text_button = Button(
            banner_entry, textvariable=search_text, command=self.getFolderPath_2)
        search_text_button.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry = Entry(banner_entry, textvariable=self.folderPath_2)
        entry.config(state='disabled')
        entry.grid(row=0, column=1, padx=5, pady=5)
        entry.config(justify="center", state="disabled")
        # CALIB 2

        space_blank_banner = Frame(self, height=20, bg=bg_color)
        space_blank_banner.pack(fill='x')

        # CALIB 3
        banner_path = Frame(self, height=40, bg=bg_color)
        banner_path.pack(fill='x')
        head_message = StringVar()
        head_message.set("PCD and Images Folder")
        head_text = Label(
            banner_path, textvariable=head_message, fg=FG, font=FONT_H)
        head_text.pack()
        banner_entry = Frame(self, height=40, bg=bg_color)
        banner_entry.pack()
        search_text = StringVar()
        search_text.set(SEARCH_BUTTON)
        search_text_button = Button(
            banner_entry, textvariable=search_text, command=self.getFolderPath_3)
        search_text_button.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry = Entry(banner_entry, textvariable=self.folderPath_3)
        entry.grid(row=0, column=1, padx=5, pady=5)
        entry.config(justify="center", state="disabled")
        # CALIB 3

        space_blank_banner = Frame(self, height=20, bg=bg_color)
        space_blank_banner.pack(fill='x')

        # CALIB 4
        banner_path = Frame(self, height=40, bg=bg_color)
        banner_path.pack(fill='x')
        head_message = StringVar()
        head_message.set("Y limit")
        head_text = Label(
            banner_path, textvariable=head_message, fg=FG, font=FONT_H)
        head_text.pack()
        banner_entry = Frame(self, height=40, bg=bg_color)
        banner_entry.pack()

        label = Label(banner_entry, text="Min")
        label.grid(row=0, column=0)
        entry_min = Entry(banner_entry, width=8,
                          textvariable=self.folderPath_4)
        entry_min.grid(row=0, column=1)

        label = Label(banner_entry, text="Max")
        label.grid(row=0, column=2)
        entry_max = Entry(banner_entry, width=8,
                          textvariable=self.folderPath_5)
        entry_max.grid(row=0, column=3)

        # CALIB 4

        space_blank_banner = Frame(self, height=20, bg=bg_color)
        space_blank_banner.pack(fill='x')

        # CALIB 5
        banner_path = Frame(self, height=40, bg=bg_color)
        banner_path.pack(fill='x')
        head_message = StringVar()
        head_message.set("Z limit")
        head_text = Label(
            banner_path, textvariable=head_message, fg=FG, font=FONT_H)
        head_text.pack()
        banner_entry = Frame(self, height=40, bg=bg_color)
        banner_entry.pack()

        label = Label(banner_entry, text="Min")
        label.grid(row=0, column=0)
        entry_min = Entry(banner_entry, width=8,
                          textvariable=self.folderPath_6)
        entry_min.grid(row=0, column=1)

        label = Label(banner_entry, text="Max")
        label.grid(row=0, column=2)
        entry_max = Entry(banner_entry, width=8,
                          textvariable=self.folderPath_7)
        entry_max.grid(row=0, column=3)
        # CALIB 5

        space_blank_banner = Frame(self, height=20, bg=bg_color)
        space_blank_banner.pack(fill='x')

        # CALIB 6
        banner_path = Frame(self, height=40, bg=bg_color)
        banner_path.pack(fill='x')
        head_message = StringVar()
        head_message.set("Divisor and Step angle")
        head_text = Label(
            banner_path, textvariable=head_message, fg=FG, font=FONT_H)
        head_text.pack()
        banner_entry = Frame(self, height=40, bg=bg_color)
        banner_entry.pack()

        label = Label(banner_entry, text="Divisor")
        label.grid(row=0, column=0)
        entry_min = Entry(banner_entry, width=8,
                          textvariable=self.folderPath_8)
        entry_min.grid(row=0, column=1)

        label = Label(banner_entry, text="Step angle")
        label.grid(row=0, column=2)
        entry_max = Entry(banner_entry, width=8,
                          textvariable=self.folderPath_9)
        entry_max.grid(row=0, column=3)
        # CALIB 6

        space_blank_banner = Frame(self, height=40, bg=bg_color)
        space_blank_banner.pack(fill='x')

        # START BUTTON
        banner_botones = Frame(self, height=40, bg=bg_color)
        banner_botones.pack()


        start_multispectral_calib_text = StringVar()
        start_multispectral_calib_text.set("Start")
        cali_button = Button(
            banner_botones, textvariable=start_multispectral_calib_text, command=self.start_calibration)
        cali_button.pack()

        # START BUTTON

    def start_calibration(self):
        form_fields = [self.folderPath.get(),
                       self.folderPath_2.get(),
                       self.folderPath_3.get(),
                       self.folderPath_4.get(),
                       self.folderPath_5.get(),
                       self.folderPath_6.get(),
                       self.folderPath_7.get(),
                       self.folderPath_8.get(),
                       self.folderPath_9.get()]
        full_data = "" not in form_fields
        
        if full_data:
            f_path = self.folderPath_3.get()
            f_key_calib = self.folderPath.get()
            f_geometric_calib = self.folderPath_2.get()
            try:
                y_limit = (float(self.folderPath_4.get()),
                           float(self.folderPath_5.get()))
            except ValueError:
                MessageBox.showerror(
                    "Error", "Y limit values must be float type")
                return None
            try:
                z_limit = (float(self.folderPath_6.get()),
                           float(self.folderPath_7.get()))
            except ValueError:
                MessageBox.showerror(
                    "Error", "Z limit values must be float type")
                return None
            try:
                divisor = int(self.folderPath_8.get())
            except ValueError:
                MessageBox.showerror(
                    "Error", "Divisor value must be integer type")
                return None
            try:
                data_step_angle = int(self.folderPath_9.get())
            except ValueError:
                MessageBox.showerror(
                    "Error", "Step angle value must be integer type")
                return None
            print("Iniciar calibración")
            print("\n".join(form_fields))
            data_cache = {
                "data_folder": f_path,
                "geometric_calibration": f_geometric_calib,
                "4D_calibration": f_key_calib,
                "y_limit": y_limit,
                "z_limit": z_limit,
                "divisor": divisor,
                "step_angle": data_step_angle
            }
            self.f = open(self.cache_file, "r+")
            self.f.seek(0)
            json.dump(data_cache, self.f)
            self.f.truncate()
            self.f.close()
            show_instructions()
            status = visualizer(f_path + "/", f_key_calib, f_geometric_calib,
                 y_limit, z_limit, divisor, data_step_angle)
            if status is not None:
                MessageBox.showerror("Error", status[1])
        else:
            MessageBox.showerror("Error", "All the fields are required")

    def getFolderPath(self):
        folder_selected = FileDialog.askopenfilename()
        self.folderPath.set(folder_selected)

    def getFolderPath_2(self):
        folder_selected = FileDialog.askopenfilename()
        self.folderPath_2.set(folder_selected)

    def getFolderPath_3(self):
        folder_selected = FileDialog.askdirectory()
        self.folderPath_3.set(folder_selected)
