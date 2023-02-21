# ===================================================
# File: app.py
# Author: Trent Bultsma
# Date: 2/21/2022
# Description: Defines an application for the 
#   user interface of the accessibility app.
# ==================================================

# imports
import os
import tkinter as tk

CRIMSON = "#981E32"
GRAY = "#5E6A71"

class AccessibilityApp(tk.Tk):
    """The user interface application for the accessibility application project."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # set window title
        self.wm_title("WSU Library Accessibility Application")

        # set the size of the window
        self.geometry("750x400")

        # set the window icon
        icon = tk.PhotoImage(file=os.path.dirname(os.path.abspath(__file__)) + "/icon.png")
        self.iconphoto(False, icon)
        
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
            frame.config(background=GRAY)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # switch to the home page
        self.switch_frame(HomePage)

    def switch_frame(self, frame_class):
        """Sets a frame to be the current one in the application window.
        
        Args:
            frame_class: The key for the frame to switch to.
        """
        frame = self.frames[frame_class]
        frame.tkraise()

class HomePage(tk.Frame):
    """A frame with the home page menu."""

    def __init__(self, parent, controller):
        """Construct a frame widget with parent `parent` and the controller for switching frames as `controller`."""
        super().__init__(parent)

        # setup the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create a label for the home page
        label = tk.Label(self, text="Home Page", background=GRAY, fg="white", font=("Montserrat", 25))
        label.grid(row=0, column=0, columnspan=2)

        # TODO fix button press down color

        # create button for switching to the automatic processing page
        switch_to_auto_page_button = tk.Button(
            self,
            text="Automatic Document Processing",
            command=lambda: controller.switch_frame(AutoProcessPage),
            bg=CRIMSON,
            fg="white",
            font=("Montserrat", 15),
            padx=10,
            pady=10,
            relief=tk.FLAT)
        switch_to_auto_page_button.grid(row=1, column=0)

        # create button for switching to the individual processing page
        switch_to_individual_page_button = tk.Button(self, text="Individual Document Processing", 
            command=lambda: controller.switch_frame(IndividualProcessPage),
            bg=CRIMSON,
            fg="white",
            font=("Montserrat", 15),
            padx=10,
            pady=10,
            relief=tk.FLAT)
        switch_to_individual_page_button.grid(row=1, column=1)

# TODO these other frame classes

class AutoProcessPage(tk.Frame):
    """A frame with a menu for automatically processing documents."""

    def __init__(self, parent, controller):
        """Construct a frame widget with parent `parent` and the controller for switching frames as `controller`."""
        super().__init__(parent)

class IndividualProcessPage(tk.Frame):
    """A frame with a menu for individually processing documents."""

    def __init__(self, parent, controller):
        """Construct a frame widget with parent `parent` and the controller for switching frames as `controller`."""
        super().__init__(parent)

if __name__ == "__main__":
    app = AccessibilityApp()
    app.mainloop()