#!/usr/bin/env python

""" This file contains main() which is where our application begins.
It is used for testing purposes because the true application starts
in terminal_application.py.
"""
# * Modules
from utils.user_interface.app import AccessibilityApp

# ? VSCode Extensions Used:
# ?     - Better Comments
# ?     - autoDocstring

__author__ = "Trent Bultsma, Reagan Kelley, Marisa Loyd"
__copyright__ = "N/A"
__credits__ = ["Trent Bultsma", "Reagan Kelley", "Marisa Loyd"]
__license__ = "GNU GENERAL PUBLIC LICENSE"
__version__ = "3.0.0"
__maintainer__ = "Trent Bultsma"
__email__ = "trent.bultsma@wsu.edu"
__status__ = "Development"

if __name__ == "__main__":
    app = AccessibilityApp()
    app.mainloop()