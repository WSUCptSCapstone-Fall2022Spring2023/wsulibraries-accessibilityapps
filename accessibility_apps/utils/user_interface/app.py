# ===================================================
# File: app.py
# Author: Trent Bultsma
# Date: 2/21/2022
# Description: Defines a front end application for 
#   the user interface of the accessibility app.
# ==================================================

# imports
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from utils.user_interface.app_controller import AccessibilityAppController

GRAY = "#4D4D4D"
LIGHT_GRAY = "#808080"
CRIMSON = "#A60F2D"
RED = "#CA1237"

def create_button(parent:object, text:str, command):
    """Instantiates a WSU custom stylized button with only the parent, text, and command needing to be specified.
    
    Args:
        parent (object): The parent widget of the button.
        text (str): The text label of the button.
        command (function): The function to run upon clicking the button.
    """
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=CRIMSON,
        activebackground=RED,
        activeforeground="white",
        fg="white",
        font=("Montserrat", 15),
        padx=10,
        pady=10,
        relief=tk.FLAT)
    
    return button

class AccessibilityApp(tk.Tk):
    """The user interface application for the accessibility application project."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # set window title and size
        self.wm_title("WSU Library Accessibility Application")
        self.geometry("750x400")
        self.resizable(False, False)

        # set the window icon
        icon = tk.PhotoImage(file=os.path.dirname(os.path.abspath(__file__)) + "/icon.png")
        self.iconphoto(False, icon)

        # setup variables for keeping track of app state
        self.auto_processing_running = False
        
        # create a container for the frames for the application and set it to fill the window
        frame_container = tk.Frame(self)
        frame_container.pack(side="top", fill="both", expand=True)

        # setup the location of the frame container with a grid
        frame_container.grid_rowconfigure(0, weight=1)
        frame_container.grid_columnconfigure(0, weight=1)

        # setup the menu bar
        menu_bar = tk.Menu(self)
        menu_bar.add_command(label="Home", command=lambda: self.switch_frame(HomePage))
        menu_bar.add_command(label="Set input/output", command=lambda: self.switch_frame(SetInputOutputFoldersPage))
        self.config(menu=menu_bar)

        # create a dictionary of frames for navigation
        self.frames = {}
        for FrameClass in (HomePage, AutoProcessPage, LocalFolderInputPage, SingleDocumentSearchPage, MultiDocumentSearchPage, SetInputOutputFoldersPage):
            # setup the frame
            frame = FrameClass(frame_container, self)
            frame.config(background=LIGHT_GRAY)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # switch to the home page
        self.switch_frame(HomePage)

        # setup the application controller
        self.app_controller = AccessibilityAppController()
        self.app_controller.update_ui_current_auto_document = self.update_current_auto_document
        self.app_controller.update_ui_current_document_count = self.update_document_count

    def switch_frame(self, frame_class):
        """Sets a frame to be the current one in the application window.
        
        Args:
            frame_class: The key for the frame to switch to.
        """
        frame = self.frames[frame_class]
        frame.tkraise()

    def toggle_auto_processing(self, button):
        """Pauses or resumes the auto processing depending on if it is already going or not (it toggles).
        
        Args:
            button: The button being pressed to call this function. It's label will be changed depending on the state of pause/resume."""
        if self.auto_processing_running:
            self.app_controller.stop_auto_mode()
            button["text"] = "Resume"
            self.auto_processing_running = False
        else:
            self.app_controller.start_auto_mode()
            button["text"] = "Pause"
            self.auto_processing_running = True

    def update_current_auto_document(self, current_document_name:str):
        """Updates the label for the automatic document processing current document.
        
        Args:
            current_document_name (str): The name for the new current document."""
        self.frames[AutoProcessPage].update_current_document(current_document_name)

    def update_document_count(self, document_count:int):
        """Updates the label for the document count of how many documents have been processed automatically.
        
        Args:
            document_count (int): The new number for how many documents have been processed."""
        self.frames[AutoProcessPage].update_document_count(document_count)

class HomePage(tk.Frame):
    """A frame with the home page menu."""

    def __init__(self, parent, ui_controller):
        """Construct a frame widget with parent `parent` and the controller for switching frames as `ui_controller`."""
        super().__init__(parent)

        # setup the grid
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create a label for the home page
        label = tk.Label(self, text="WSU Accessibility App Home Page", background=LIGHT_GRAY, fg="white", font=("Montserrat", 25))
        label.grid(row=0, column=0, columnspan=2)

        # create button for switching to the automatic processing page
        switch_to_auto_page_button = create_button(self, "Automatic Document Processing", lambda: ui_controller.switch_frame(AutoProcessPage))
        switch_to_auto_page_button.grid(row=1, column=0)

        # create button for switching to the local folder input page
        switch_to_individual_page_button = create_button(self, "Local Folder Input", lambda: ui_controller.switch_frame(LocalFolderInputPage))
        switch_to_individual_page_button.grid(row=1, column=1)

        # create button for switching to the single document search page
        switch_to_individual_page_button = create_button(self, "Single Document ID Search", lambda: ui_controller.switch_frame(SingleDocumentSearchPage))
        switch_to_individual_page_button.grid(row=2, column=0)

        # create button for switching to the multi document search page
        switch_to_individual_page_button = create_button(self, "Multi Document ID Search", lambda: ui_controller.switch_frame(MultiDocumentSearchPage))
        switch_to_individual_page_button.grid(row=2, column=1)

# TODO add resumption tag? (low priority)
class AutoProcessPage(tk.Frame):
    """A frame with a menu for automatically processing documents."""

    def __init__(self, parent, ui_controller):
        """Construct a frame widget with parent `parent` and the controller for switching frames as `ui_controller`."""
        super().__init__(parent)

        # configure the grid
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=2)
        self.grid_columnconfigure(0, weight=1)

        # create label for description of the purpose of the page
        page_description_label = tk.Label(self, text="Automatically process documents from the repository in order and export them to a folder. " +
            "This can be used to go through the entire repository without user interaction like leaving it on overnight.", 
            background=LIGHT_GRAY, fg="white", font=("Montserrat", 17), wraplength=700)
        page_description_label.grid(row=0, column=0)

        # create label for the current document being processed
        self.current_document_label = tk.Label(self, text="Current Document: None", background=LIGHT_GRAY, fg="white", font=("Montserrat", 15), wraplength=700)
        self.current_document_label.grid(row=1, column=0)

        # create label for the count of how many documents have been processed
        self.document_count_label = tk.Label(self, text="Documents Processed: 0", background=LIGHT_GRAY, fg="white", font=("Montserrat", 15), wraplength=700)
        self.document_count_label.grid(row=2, column=0)

        # create start/pause/resume button
        pause_resume_button = create_button(self, "Start", lambda: ui_controller.toggle_auto_processing(pause_resume_button))
        pause_resume_button.grid(row=3, column=0)

    def update_current_document(self, current_document_name:str):
        """Updates the label for the current document.
        
        Args:
            current_document_name (str): The name for the new current document."""
        self.current_document_label["text"] = "Current Document: " + current_document_name

    def update_document_count(self, document_count:int):
        """Updates the label for the document count.
        
        Args:
            document_count (int): The new number for how many documents have been processed."""
        self.document_count_label["text"] = "Documents Processed: " + str(document_count)

class LocalFolderInputPage(tk.Frame):
    """A frame with a menu for processing all documents inside a local input folder."""

    def __init__(self, parent, ui_controller):
        """Construct a frame widget with parent `parent` and the controller for switching frames as `ui_controller`."""
        super().__init__(parent)

        self.ui_controller = ui_controller

        # setup the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # create label for description of the purpose of the page
        page_description_label = tk.Label(self, text="Process documents automatically from a local input folder containing a bunch of pdfs and a csv file to contain metadata.", 
            background=LIGHT_GRAY, fg="white", font=("Montserrat", 17), wraplength=700)
        page_description_label.grid(row=0, column=0, columnspan=2)

        # create button for selecting the folder
        folder_select_button = create_button(self, "Select Folder", self._set_folder)
        folder_select_button.grid(row=1, column=0)

        # create label for the name of the folder
        self.folder_name_label = tk.Label(self, text="None", background=LIGHT_GRAY, fg="white", font=("Montserrat", 15), wraplength=350)
        self.folder_name_label.grid(row=1, column=1)
        self.folder = None

        # create button to run the processing
        self.run_processing_button = create_button(self, "Start", self._process_folder)
        self.run_processing_button.grid(row=2, column=0)

        # create progress bar
        self.progress_bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=200)
        self.progress_bar.grid(row=2, column=1)

    def _set_folder(self):
        """Opens a file dialog to select the folder and sets it for the page."""
        self.folder = filedialog.askdirectory()
        self.folder_name_label["text"] = self.folder

    def _process_folder(self):
        """Processes through the documents in the folder."""
        
        # reset the progress bar
        self.progress_bar["value"] = 0

        # check errors
        if self.folder is None:
            messagebox.showerror("Error", "Must select a folder")
        else:
            try:
                # disable the button so it cannot be clicked again until the job is done
                self.run_processing_button["state"] = tk.DISABLED
                # run the job
                self.ui_controller.app_controller.process_local_folder(self.folder, lambda progress: self.progress_bar.step(progress), self._processing_finished)
            except Exception as e:
                # reset the stuff when processing is done even though it failed
                self._processing_finished()
                # show the error
                messagebox.showerror("Error", str(e))

    def _processing_finished(self):
        """Cleans up and resets some stuff after processing is done."""
        # enables the run button so it can be pressed again
        self.run_processing_button["state"] = tk.NORMAL
        # reset the progress bar
        self.progress_bar["value"] = 0

class SingleDocumentSearchPage(tk.Frame):
    """A frame with a menu for processing a single document searched by document id."""

    def __init__(self, parent, ui_controller):
        """Construct a frame widget with parent `parent` and the controller for switching frames as `ui_controller`."""
        super().__init__(parent)

        self.ui_controller = ui_controller

        # setup the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # create label for description of the purpose of the page
        page_description_label = tk.Label(self, text="Process a single document from the repository given its document id.", background=LIGHT_GRAY, fg="white", font=("Montserrat", 17), wraplength=700)
        page_description_label.grid(row=0, column=0, columnspan=2)

        # create label for document id search bar title
        document_id_title = tk.Label(self, text="Document ID:", background=LIGHT_GRAY, fg="white", font=("Montserrat", 15))
        document_id_title.grid(row=1, column=0)

        # create document id search bar
        self.search_bar = tk.Entry(self, font=("Montserrat", 15))
        self.search_bar.grid(row=1, column=1)

        # create start button
        self.start_button = create_button(self, "Start", self.run_document_processing)
        self.start_button.grid(row=2, column=0)

        # create progress label
        self.progress_label = tk.Label(self, text="Waiting", background=LIGHT_GRAY, fg="white", font=("Montserrat", 15))
        self.progress_label.grid(row=2, column=1)

    def run_document_processing(self):
        """Runs the document search and processing using the id from the search bar."""
        self.progress_label["text"] = "Processing..."
        self.start_button["state"] = tk.DISABLED
        self.ui_controller.app_controller.process_document_by_id(self.search_bar.get(), self.processing_done_callback)
        
    def processing_done_callback(self, progress_text:str="Done"):
        """Signifies that the document processing has finished and updates the ui accordingly.
        
        Args:
            progress_text (str): The text to display on the progress label.
        """
        self.progress_label["text"] = progress_text
        self.start_button["state"] = tk.NORMAL

class MultiDocumentSearchPage(tk.Frame):
    """A frame with a menu for processing documents given a list of document ids. The 
    document ids should be in a csv file with just a column of ids and no header or anything."""

    def __init__(self, parent, ui_controller):
        """Construct a frame widget with parent `parent` and the controller for switching frames as `ui_controller`."""
        super().__init__(parent)

        self.ui_controller = ui_controller
        self.csv_input_file = None

        # setup the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # create label for description of the purpose of the page
        page_description_label = tk.Label(self, text="Process many documents from the repository given a list of document ids in a csv file.", background=LIGHT_GRAY, fg="white", font=("Montserrat", 17), wraplength=700)
        page_description_label.grid(row=0, column=0, columnspan=2)

        # create csv select button
        start_button = create_button(self, "Select ID List", self._select_csv_input)
        start_button.grid(row=1, column=0)

        # create selected csv label
        self.file_name_label = tk.Label(self, text="None", background=LIGHT_GRAY, fg="white", font=("Montserrat", 15), wraplength=350)
        self.file_name_label.grid(row=1, column=1)

        # create start button
        self.start_button = create_button(self, "Start", self._process_documents)
        self.start_button.grid(row=2, column=0)

        # create progress bar
        self.progress_bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=200)
        self.progress_bar.grid(row=2, column=1)

    def _select_csv_input(self):
        """Sets the csv file for document input"""
        self.csv_input_file = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV Files","*.csv")])
        self.file_name_label["text"] = self.csv_input_file
        
    def _process_documents(self):
        """Process the documents in the selected csv file."""
        # reset the progress bar
        self.progress_bar["value"] = 0

        # check errors
        if self.csv_input_file is None:
            messagebox.showerror("Error", "Must select a file")
        else:
            try:
                # disable the button so it cannot be clicked again until the job is done
                self.start_button["state"] = tk.DISABLED
                # run the job
                self.ui_controller.app_controller.process_document_id_list(self.csv_input_file, lambda progress: self.progress_bar.step(progress), self._processing_finished)
            except Exception as e:
                # reset the stuff when processing is done even though it failed
                self._processing_finished()
                # show the error
                messagebox.showerror("Error", str(e))

    def _processing_finished(self):
        """Cleans up and resets some stuff after processing is done."""
        # enables the run button so it can be pressed again
        self.start_button["state"] = tk.NORMAL
        # reset the progress bar
        self.progress_bar["value"] = 0

class SetInputOutputFoldersPage(tk.Frame):
    """A frame with a menu for setting the default input and output folder."""

    def __init__(self, parent, ui_controller):
        """Construct a frame widget with parent `parent` and the controller for switching frames as `ui_controller`."""
        super().__init__(parent)

        self.ui_controller = ui_controller
        self.selected_input_folder = None
        self.selected_output_folder = None

        # setup the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # create label for description of the purpose of the page
        page_description_label = tk.Label(self, text="Set the folder for all output files and the default folder for input when none is specified.", background=LIGHT_GRAY, fg="white", font=("Montserrat", 17), wraplength=700)
        page_description_label.grid(row=0, column=0, columnspan=2)

        # create button for selecting the input folder
        input_folder_select_button = create_button(self, "Select Input Folder", self._select_input_folder)
        input_folder_select_button.grid(row=1, column=0)

        # create label to display selected input folder
        self.input_folder_name_label = tk.Label(self, text="None", background=LIGHT_GRAY, fg="white", font=("Montserrat", 15), wraplength=350)
        self.input_folder_name_label.grid(row=1, column=1)

        # create button for selecting the output folder
        output_folder_select_button = create_button(self, "Select Output Folder", self._select_output_folder)
        output_folder_select_button.grid(row=2, column=0)
        
        # create label to display selected output folder
        self.output_folder_name_label = tk.Label(self, text="None", background=LIGHT_GRAY, fg="white", font=("Montserrat", 15), wraplength=350)
        self.output_folder_name_label.grid(row=2, column=1)

        # create button to set the values
        folder_set_button = create_button(self, "Set Values", self._set_selected_folders)
        folder_set_button.grid(row=3, column=0, columnspan=2)

    def _select_input_folder(self):
        """Selects a folder to set for default input."""
        self.selected_input_folder = filedialog.askdirectory()
        self.input_folder_name_label["text"] = self.selected_input_folder

    def _select_output_folder(self):
        """Selects a folder to set for default output."""
        self.selected_output_folder = filedialog.askdirectory()
        self.output_folder_name_label["text"] = self.selected_output_folder

    def _set_selected_folders(self):
        """Sets the selected folders for input and output to be 
        the corresponding folders in the backend of the program."""
        if self.selected_input_folder == self.selected_output_folder:
            messagebox.showerror("Error", "Input and output directories may not match.")
        else:
            self.ui_controller.app_controller.set_default_input_output_folders(self.selected_input_folder, self.selected_output_folder)