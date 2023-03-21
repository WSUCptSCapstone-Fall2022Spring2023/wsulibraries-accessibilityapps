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
from utils.user_interface.app_controller import AccessibilityAppController

GRAY = "#4D4D4D"
LIGHT_GRAY = "#808080"
CRIMSON = "#A60F2D"
RED = "#CA1237"

# TODO
# - search by document id
# - search by research unit
# - filter by document set
# - set input/output folder
# - *input from local folder with metadata as csv file and pdfs
# - *list of document ids input from a csv file
# - error displaying

# TODO create function to generate a button instead of copy/pasting the big block of code for that

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
        switch_to_auto_page_button = tk.Button(
            self,
            text="Automatic Document Processing",
            command=lambda: ui_controller.switch_frame(AutoProcessPage),
            bg=CRIMSON,
            activebackground=RED,
            activeforeground="white",
            fg="white",
            font=("Montserrat", 15),
            padx=10,
            pady=10,
            relief=tk.FLAT)
        switch_to_auto_page_button.grid(row=1, column=0)

        # create button for switching to the local folder input page
        switch_to_individual_page_button = tk.Button(self, text="Local Folder Input", 
            command=lambda: ui_controller.switch_frame(LocalFolderInputPage),
            bg=CRIMSON,
            activebackground=RED,
            activeforeground="white",
            fg="white",
            font=("Montserrat", 15),
            padx=10,
            pady=10,
            relief=tk.FLAT)
        switch_to_individual_page_button.grid(row=1, column=1)

        # create button for switching to the single document search page
        switch_to_individual_page_button = tk.Button(self, text="Single Document ID Search", 
            command=lambda: ui_controller.switch_frame(SingleDocumentSearchPage),
            bg=CRIMSON,
            activebackground=RED,
            activeforeground="white",
            fg="white",
            font=("Montserrat", 15),
            padx=10,
            pady=10,
            relief=tk.FLAT)
        switch_to_individual_page_button.grid(row=2, column=0)

        # create button for switching to the multi document search page
        switch_to_individual_page_button = tk.Button(self, text="Multi Document ID Search", 
            command=lambda: ui_controller.switch_frame(MultiDocumentSearchPage),
            bg=CRIMSON,
            activebackground=RED,
            activeforeground="white",
            fg="white",
            font=("Montserrat", 15),
            padx=10,
            pady=10,
            relief=tk.FLAT)
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
        pause_resume_button = tk.Button(self, text="Start", 
            command=lambda: ui_controller.toggle_auto_processing(pause_resume_button),
            bg=CRIMSON,
            activebackground=RED,
            activeforeground="white",
            fg="white",
            font=("Montserrat", 15),
            padx=10,
            pady=10,
            relief=tk.FLAT)
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
        folder_select_button = tk.Button(self, text="Select Folder", 
            command=lambda: None, # TODO
            bg=CRIMSON,
            activebackground=RED,
            activeforeground="white",
            fg="white",
            font=("Montserrat", 15),
            padx=10,
            pady=10,
            relief=tk.FLAT)
        folder_select_button.grid(row=1, column=0)

        # create label for the name of the folder
        folder_name_label = tk.Label(self, text="None", background=LIGHT_GRAY, fg="white", font=("Montserrat", 15), wraplength=350)
        folder_name_label.grid(row=1, column=1)

        # create button to run the processing
        # TODO error box if there is no csv found
        run_processing_button = tk.Button(self, text="Start", 
            command=lambda: None, # TODO
            bg=CRIMSON,
            activebackground=RED,
            activeforeground="white",
            fg="white",
            font=("Montserrat", 15),
            padx=10,
            pady=10,
            relief=tk.FLAT)
        run_processing_button.grid(row=2, column=0)

        # create progress bar
        # TODO needs to be updated as progress is made
        self.progress_bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=200)
        self.progress_bar.grid(row=2, column=1)

class SingleDocumentSearchPage(tk.Frame):
    """A frame with a menu for processing a single document searched by document id."""

    def __init__(self, parent, ui_controller):
        """Construct a frame widget with parent `parent` and the controller for switching frames as `ui_controller`."""
        super().__init__(parent)

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
        search_bar = tk.Entry(self, font=("Montserrat", 15))
        search_bar.grid(row=1, column=1)

        # create start button
        start_button = tk.Button(self, text="Start", 
            command=lambda: None, # TODO
            bg=CRIMSON,
            activebackground=RED,
            activeforeground="white",
            fg="white",
            font=("Montserrat", 15),
            padx=10,
            pady=10,
            relief=tk.FLAT)
        start_button.grid(row=2, column=0)

        # create progress label
        # TODO this needs to be updated to say "Processing..." and then "Done"
        progress_label = tk.Label(self, text="Waiting", background=LIGHT_GRAY, fg="white", font=("Montserrat", 15))
        progress_label.grid(row=2, column=1)

class MultiDocumentSearchPage(tk.Frame):
    """A frame with a menu for processing documents given a list of document ids."""

    def __init__(self, parent, ui_controller):
        """Construct a frame widget with parent `parent` and the controller for switching frames as `ui_controller`."""
        super().__init__(parent)

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
        start_button = tk.Button(self, text="Select ID List", 
            command=lambda: None, # TODO
            bg=CRIMSON,
            activebackground=RED,
            activeforeground="white",
            fg="white",
            font=("Montserrat", 15),
            padx=10,
            pady=10,
            relief=tk.FLAT)
        start_button.grid(row=1, column=0)

        # create selected csv label
        folder_name_label = tk.Label(self, text="None", background=LIGHT_GRAY, fg="white", font=("Montserrat", 15), wraplength=350)
        folder_name_label.grid(row=1, column=1)

        # create start button
        start_button = tk.Button(self, text="Start", 
            command=lambda: None, # TODO
            bg=CRIMSON,
            activebackground=RED,
            activeforeground="white",
            fg="white",
            font=("Montserrat", 15),
            padx=10,
            pady=10,
            relief=tk.FLAT)
        start_button.grid(row=2, column=0)

        # create progress bar
        # TODO needs to be updated as progress is made
        self.progress_bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=200)
        self.progress_bar.grid(row=2, column=1)

class SetInputOutputFoldersPage(tk.Frame):
    """A frame with a menu for setting the default input and output folder."""

    def __init__(self, parent, ui_controller):
        """Construct a frame widget with parent `parent` and the controller for switching frames as `ui_controller`."""
        super().__init__(parent)

        # setup the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create label for description of the purpose of the page
        label = tk.Label(self, text="Put some text input boxes here", background=LIGHT_GRAY, fg="white", font=("Montserrat", 25))
        label.grid(row=0, column=0)

        # TODO