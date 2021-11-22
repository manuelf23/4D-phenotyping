
import json
import sys
import os
actual_file_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(f"{actual_file_path}/../src")
# from feno4D_visualizer import visualizer
# from ImgAnalyze import ImgAnalyze
# import threading
from rotation_xy_plane import plane_calibration
from center_calibration import find_center
from image_registration import image_registration
from extract_3dand2d_kpoints import sensory_fusion_calibration
from tkinter import Button, Entry, Frame, Label, StringVar
from tkinter import filedialog as FileDialog
from tkinter import messagebox as MessageBox
from tkinter import Checkbutton, BooleanVar


SEARCH_BUTTON = "Search"
FONT_H = "Helvetica 14 bold"
FONT_S = "Helvetica 13"
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
        self.checkbox_value = BooleanVar(self)
        self.checkbox_value.set(False)
        
        self.folder_save_calibs = StringVar()
        self.folder_save_calibs.set("")
        self.folderPath_2 = StringVar()
        self.folderPath_2.set("")
        self.filePath_3 = StringVar()
        self.filePath_3.set("")
        self.y_limit_min = StringVar()
        self.y_limit_min.set("")
        self.y_limit_max = StringVar()
        self.y_limit_max.set("")
        self.z_limit_min = StringVar()
        self.z_limit_min.set("")
        self.z_limit_max = StringVar()
        self.z_limit_max.set("")
        self.imgRegisFolder = StringVar()
        self.imgRegisFolder.set("")
        self.fusion_folder = StringVar()
        self.fusion_folder.set("")
        self.folderPath_10 = StringVar()
        self.folderPath_10.set("")

       
        # CALIB 1
        banner_path = Frame(self, height=40, bg=bg_color)
        banner_path.pack(fill='x')
        head_message = StringVar()
        head_message.set("Folder for saving calibrations")
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
        entry = Entry(banner_entry, textvariable=self.folder_save_calibs)
        entry.config(state='disabled')
        entry.grid(row=0, column=1, padx=5, pady=5)
        entry.config(justify="center", state="disabled")
        # checkbutton
        checkbox = Checkbutton(self,
            text="Display calibration graphs when calibrating", variable=self.checkbox_value)
        checkbox.pack()
        # CALIB 1

        space_blank_banner = Frame(self, height=20, bg=bg_color)
        space_blank_banner.pack(fill='x')

        # CALIB 2
        # Message
        banner_path = Frame(self, height=40, bg=bg_color)
        banner_path.pack(fill='x')
        
        head_message = StringVar()
        head_message.set("Geometric Calibration")
        head_text = Label(
            banner_path, textvariable=head_message, fg=FG, font=FONT_H)
        head_text.pack()

        subtitle_message = StringVar()
        subtitle_message.set("Plane calibration data folder")
        head_text = Label(
            banner_path, textvariable=subtitle_message, fg=FG, font=FONT_S)
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
        # Message
        # Message
        banner_path = Frame(self, height=40, bg=bg_color)
        banner_path.pack(fill='x')
        subtitle_message = StringVar()
        subtitle_message.set("Center of the turntable .csv gile (PCD)")
        head_text = Label(
            banner_path, textvariable=subtitle_message, fg=FG, font=FONT_S)
        head_text.pack()
        banner_entry = Frame(self, height=40, bg=bg_color)
        banner_entry.pack()
        search_text = StringVar()
        search_text.set(SEARCH_BUTTON)
        search_text_button = Button(
            banner_entry, textvariable=search_text, command=self.getFilePath_3)
        search_text_button.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry = Entry(banner_entry, textvariable=self.filePath_3)
        entry.config(state='disabled')
        entry.grid(row=0, column=1, padx=5, pady=5)
        entry.config(justify="center", state="disabled")

        banner_entry = Frame(self, height=40, bg=bg_color)
        banner_entry.pack()
        head_message = StringVar()
        head_message.set("Y limit for filter PCD")
        head_text = Label(
            banner_entry, textvariable=head_message, fg=FG, font=FONT_S)
        head_text.pack()
        banner_entry = Frame(self, height=40, bg=bg_color)
        banner_entry.pack()

        label = Label(banner_entry, text="Min")
        label.grid(row=0, column=0)
        entry_min = Entry(banner_entry, width=8,
                          textvariable=self.y_limit_min)
        entry_min.grid(row=0, column=1)

        label = Label(banner_entry, text="Max")
        label.grid(row=0, column=2)
        entry_max = Entry(banner_entry, width=8,
                          textvariable=self.y_limit_max)
        entry_max.grid(row=0, column=3)

        banner_entry = Frame(self, height=40, bg=bg_color)
        banner_entry.pack()
        head_message = StringVar()
        head_message.set("Z limit for filter PCD")
        head_text = Label(
            banner_entry, textvariable=head_message, fg=FG, font=FONT_S)
        head_text.pack()
        banner_entry = Frame(self, height=40, bg=bg_color)
        banner_entry.pack()

        label = Label(banner_entry, text="Min")
        label.grid(row=0, column=0)
        entry_min = Entry(banner_entry, width=8,
                          textvariable=self.z_limit_min)
        entry_min.grid(row=0, column=1)

        label = Label(banner_entry, text="Max")
        label.grid(row=0, column=2)
        entry_max = Entry(banner_entry, width=8,
                          textvariable=self.z_limit_max)
        entry_max.grid(row=0, column=3)

        # Message
        # START BUTTON
        banner_botones = Frame(self, height=10, bg=bg_color)
        banner_botones.pack()


        start_multispectral_calib_text = StringVar()
        start_multispectral_calib_text.set("Start geometric calibration")
        cali_button = Button(
            banner_botones, textvariable=start_multispectral_calib_text, command=self.start_geometri_calib)
        cali_button.pack()

        # START BUTTON

        # # CALIB 2

        space_blank_banner = Frame(self, height=20, bg=bg_color)
        space_blank_banner.pack(fill='x')

        # CALIB 3
        # Message
        banner_path = Frame(self, height=40, bg=bg_color)
        banner_path.pack(fill='x')
        
        head_message = StringVar()
        head_message.set("Multispectral image registration")
        head_text = Label(
            banner_path, textvariable=head_message, fg=FG, font=FONT_H)
        head_text.pack()

        subtitle_message = StringVar()
        subtitle_message.set("Images folder")
        head_text = Label(
            banner_path, textvariable=subtitle_message, fg=FG, font=FONT_S)
        head_text.pack()

        banner_entry = Frame(self, height=40, bg=bg_color)
        banner_entry.pack()
        search_text = StringVar()
        search_text.set(SEARCH_BUTTON)
        search_text_button = Button(
            banner_entry, textvariable=search_text, command=self.getImgRegisFolder)
        search_text_button.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry = Entry(banner_entry, textvariable=self.imgRegisFolder)
        entry.config(state='disabled')
        entry.grid(row=0, column=1, padx=5, pady=5)
        entry.config(justify="center", state="disabled")
        # Message
        
        # START BUTTON
        banner_botones = Frame(self, height=10, bg=bg_color)
        banner_botones.pack()


        start_multispectral_calib_text = StringVar()
        start_multispectral_calib_text.set("Start multispectral image registration")
        cali_button = Button(
            banner_botones, textvariable=start_multispectral_calib_text, command=self.start_img_regis)
        cali_button.pack()

        # START BUTTON

        space_blank_banner = Frame(self, height=20, bg=bg_color)
        space_blank_banner.pack(fill='x')

        # CALIB 4
        # Message
        banner_path = Frame(self, height=40, bg=bg_color)
        banner_path.pack(fill='x')
        
        head_message = StringVar()
        head_message.set("4D Geometric calibration (sensory fusion)")
        head_text = Label(
            banner_path, textvariable=head_message, fg=FG, font=FONT_H)
        head_text.pack()

        subtitle_message = StringVar()
        subtitle_message.set("Images and PCD folder for calibration")
        head_text = Label(
            banner_path, textvariable=subtitle_message, fg=FG, font=FONT_S)
        head_text.pack()

        banner_entry = Frame(self, height=40, bg=bg_color)
        banner_entry.pack()
        search_text = StringVar()
        search_text.set(SEARCH_BUTTON)
        search_text_button = Button(
            banner_entry, textvariable=search_text, command=self.getFusionFolder)
        search_text_button.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry = Entry(banner_entry, textvariable=self.fusion_folder)
        entry.config(state='disabled')
        entry.grid(row=0, column=1, padx=5, pady=5)
        entry.config(justify="center", state="disabled")
        # Message
        
        # START BUTTON
        banner_botones_t = Frame(self, height=10, bg=bg_color)
        banner_botones_t.pack()
        subtitle_message = StringVar()
        subtitle_message.set("Start 4D Geometric calibration")
        head_text = Label(
            banner_botones_t, textvariable=subtitle_message, fg=FG, font=FONT_S)
        head_text.pack()

        banner_botones = Frame(self, height=10, bg=bg_color)
        banner_botones.pack()
        start_multispectral_calib_text = StringVar()
        start_multispectral_calib_text.set("2D points auto")
        cali_button = Button(
            banner_botones, textvariable=start_multispectral_calib_text, command=self.start_fusion_auto)
        cali_button.grid(column=0, row=0)

        start_multispectral_calib_text = StringVar()
        start_multispectral_calib_text.set("2D points manual")
        cali_button = Button(
            banner_botones, textvariable=start_multispectral_calib_text, command=self.start_fusion_manual)
        cali_button.grid(column=1, row=0)

        # START BUTTON

        # # CALIB 4

        space_blank_banner = Frame(self, height=20, bg=bg_color)
        space_blank_banner.pack(fill='x')




    def getFolderPath(self):
        folder_selected = FileDialog.askdirectory()
        self.folder_save_calibs.set(folder_selected)

    def getFolderPath_2(self):
        folder_selected = FileDialog.askdirectory()
        self.folderPath_2.set(folder_selected)

    def getFilePath_3(self):
        folder_selected = FileDialog.askopenfilename()
        self.filePath_3.set(folder_selected)
    
    def getFolderPath_4(self):
        folder_selected = FileDialog.askdirectory()
        self.y_limit_min.set(folder_selected)

    def getImgRegisFolder(self):
        folder_selected = FileDialog.askdirectory()
        self.imgRegisFolder.set(folder_selected)

    def getFusionFolder(self):
        folder_selected = FileDialog.askdirectory()
        self.fusion_folder.set(folder_selected)

    def start_geometri_calib(self):
        # print(self.folder_save_calibs.get())
        show_graphs = self.checkbox_value.get()
        save_folder_path = self.folder_save_calibs.get()
        if save_folder_path == "":
            MessageBox.showerror("Error", "Path to the folder for saving calibrations is required")
            return -1
        folder_path = self.folderPath_2.get()
        if folder_path == "":
            MessageBox.showerror("Error", "Path to the plane calibration data folder is required")
            return -1
        file_path = self.filePath_3.get()
        if file_path == "" or ".csv" not in file_path:
            MessageBox.showerror("Error", "Path to the .csv file with center calibration data is required")
            return -1
        try:
            y_limit = (float(self.y_limit_min.get()), float(self.y_limit_max.get()))
            z_limit = (float(self.z_limit_min.get()), float(self.z_limit_max.get()))
        except ValueError:
            MessageBox.showerror("Error", "Y-limit and Z-limit must be floats values")
            return -1
        if show_graphs:
            MessageBox.showinfo("Calibration", "When there will be a graph the calibration will stop until you press the 'q' key to close the graph")
        plane_calibration(folder_path, save_folder_path, show_graphs, y_limit=y_limit, z_limit=z_limit)
        find_center(file_path, save_folder_path, show_graphs, y_limit=y_limit, z_limit=z_limit)

        
        MessageBox.showinfo("Calibration", "Calibration process finished successfully")
    
    def start_img_regis(self):
        show_graphs = self.checkbox_value.get()
        save_folder_path = self.folder_save_calibs.get()
        if save_folder_path == "":
            MessageBox.showerror("Error", "Path to the folder for saving calibrations is required")
            return -1
        image_folder_path = self.imgRegisFolder.get()
        if image_folder_path == "":
            MessageBox.showerror("Error", "Path to the multispectral images data folder is required")
            return -1
        image_registration(image_folder_path, save_folder_path)
        MessageBox.showinfo("Calibration", "Calibration process finished successfully")
    
    def start_fusion_auto(self):
        show_graphs = self.checkbox_value.get()

        MessageBox.showinfo("Calibration", "For selecting 2D point automatically the images must have a green or blue background")
        save_folder_path = self.folder_save_calibs.get()
        if save_folder_path == "":
            MessageBox.showerror("Error", "Path to the folder for saving calibrations is required")
            return -1
        folder_path = self.fusion_folder.get()
        if folder_path == "":
            MessageBox.showerror("Error", "Path to the multispectral images and PCD data folder is required")
            return -1
        multispectral_calib = f"{save_folder_path}/multispectral_image_registration"
        if not os.path.isdir(multispectral_calib):
            MessageBox.showerror("Error", "There is not multispectral image registration calibration. Please do that calibration first")
            return -1
        if show_graphs:
            MessageBox.showinfo("Calibration", "When there will be a graph the calibration will stop until you press the 'q' key to close the graph")
        sensory_fusion_calibration(folder_path, save_folder_path, multispectral_calib, show_graphs, auto=True)
        MessageBox.showinfo("Calibration", "Calibration process finished successfully")
    
    def start_fusion_manual(self):
        MessageBox.showinfo("Calibration", "Select with the left button click the board corners starting with the upper corner and following clockwise direction.\n\nONLY SELECT FOUR POINTS PER IMAGE")
        save_folder_path = self.folder_save_calibs.get()
        if save_folder_path == "":
            MessageBox.showerror("Error", "Path to the folder for saving calibrations is required")
            return -1
        folder_path = self.fusion_folder.get()
        if folder_path == "":
            MessageBox.showerror("Error", "Path to the multispectral images and PCD data folder is required")
            return -1
        multispectral_calib = f"{save_folder_path}/multispectral_image_registration"
        if not os.path.isdir(multispectral_calib):
            MessageBox.showerror("Error", "There is not multispectral image registration calibration. Please do that calibration first")
            return -1
        sensory_fusion_calibration(folder_path, save_folder_path, multispectral_calib, show_graphs, auto=False)
        MessageBox.showinfo("Calibration", "Calibration process finished successfully")