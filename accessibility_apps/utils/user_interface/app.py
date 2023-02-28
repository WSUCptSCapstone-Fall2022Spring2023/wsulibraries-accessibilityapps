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
from utils.user_interface.app_controller import AccessibilityAppController

GRAY = "#4D4D4D"
LIGHT_GRAY = "#808080"
CRIMSON = "#A60F2D"
RED = "#CA1237"

class AccessibilityApp(tk.Tk):
    """The user interface application for the accessibility application project."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # set window title and size
        self.wm_title("WSU Library Accessibility Application")
        self.geometry("750x400")

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
        self.config(menu=menu_bar)

        # create a dictionary of frames for navigation
        self.frames = {}
        for FrameClass in (HomePage, AutoProcessPage, IndividualProcessPage):
            # setup the frame
            frame = FrameClass(frame_container, self)
            frame.config(background=LIGHT_GRAY)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # switch to the home page
        self.switch_frame(HomePage)

        # setup the application controller
        self.app_controller = AccessibilityAppController()
        self.update_ui_current_auto_document = self.update_current_auto_document
        self.update_ui_current_document_count = self.update_document_count

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
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
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

        # create button for switching to the individual processing page
        switch_to_individual_page_button = tk.Button(self, text="Individual Document Processing", 
            command=lambda: ui_controller.switch_frame(IndividualProcessPage),
            bg=CRIMSON,
            activebackground=RED,
            activeforeground="white",
            fg="white",
            font=("Montserrat", 15),
            padx=10,
            pady=10,
            relief=tk.FLAT)
        switch_to_individual_page_button.grid(row=1, column=1)

class AutoProcessPage(tk.Frame):
    """A frame with a menu for automatically processing documents."""

    def __init__(self, parent, ui_controller):
        """Construct a frame widget with parent `parent` and the controller for switching frames as `ui_controller`."""
        super().__init__(parent)

        # configure the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=1)

        # create label for the current document being processed
        self.current_document_label = tk.Label(self, text="Current Document: None", background=LIGHT_GRAY, fg="white", font=("Montserrat", 25))
        self.current_document_label.grid(row=0, column=0)

        # create label for the count of how many documents have been processed
        self.document_count_label = tk.Label(self, text="Documents Processed: 0", background=LIGHT_GRAY, fg="white", font=("Montserrat", 25))
        self.document_count_label.grid(row=1, column=0)

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
        pause_resume_button.grid(row=2, column=0)

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

class IndividualProcessPage(tk.Frame):
    """A frame with a menu for individually processing documents."""

    def __init__(self, parent, ui_controller):
        """Construct a frame widget with parent `parent` and the controller for switching frames as `ui_controller`."""
        super().__init__(parent)

        # setup the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create a label for the home page
        label = tk.Label(self, text="Maybe put a search bar here later?", background=LIGHT_GRAY, fg="white", font=("Montserrat", 25))
        label.grid(row=0, column=0)