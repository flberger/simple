""" Simplified GUI generation using Tkinter

    Copyright (c) 2013 by Florian Berger <fberger@florian-berger.de>
"""

# This file is part of simplegui.
#
# simplegui is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# simplegui is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with simplegui.  If not, see <http://www.gnu.org/licenses/>.

# work started on 22. Jan 2013

# Checked, but insufficient:
#
# pytkmdiapp http://pypi.python.org/pypi/pytkmdiapp/0.1.1
# Grun http://www.manatlan.com/page/grun
# EasyGUI http://easygui.sourceforge.net/

# TODO: scales should display the actual value sent
# TODO: keep track of generated buttons per GUI, and make them all the same width

VERSION = "0.1.1"

import sys

try:
    import tkinter

except ImportError:

    # Support Python 2.x
    #
    import Tkinter as tkinter

# Different Python versions supply different Tk extension packages.
#
# In Python 2.x and above, there is Tix. It is an older 3rd party
# addon.
#
# In Python 3.x and above, there is ttk. It is part of Tk and generally
# looks more modern. Common advice is to
#
#     from Tkinter import *
#     from ttk import *
#
# to make ttk overwrite certain Tk widgets.
#
# Tix and ttk supply similar extensions:
#
#     Tkinter       Tix (Python 2.x)    ttk (Python 3.x)
#     -------       ----------------    ----------------
#     Button                            Button
#     Checkbutton                       Checkbutton
#                                       Combobox
#     Entry                             Entry
#     Frame                             Frame
#     Label                             Label
#     LabelFrame                        LabelFrame
#     Menubutton                        Menubutton
#                                       Notebook
#     PanedWindow                       PanedWindow
#                                       Progressbar
#     Radiobutton                       Radiobutton
#     Scale                             Scale
#     Scrollbar                         Scrollbar
#                                       Separator
#                                       Sizegrip
#                                       Treeview
#
#                   Balloon
#                   BitmapImage
#                   Button
#                   ButtonBox
#                   Canvas
#                   CheckList
#                   Checkbutton
#                   ComboBox
#                   Control
#                   DialogShell
#                   DirList
#                   DirSelectBox
#                   DirSelectDialog
#                   DirTree
#                   ExFileSelectBox
#                   ExFileSelectDialog
#                   FileEntry
#                   FileSelectBox
#                   FileSelectDialog
#                   Form
#                   Frame
#                   Grid
#                   Image
#                   InputOnly
#                   Label
#                   LabelEntry
#                   LabelFrame
#                   ListNoteBook
#                   Listbox
#                   Menu
#                   Menubutton
#                   Message
#                   Meter
#                   NoteBook
#                   NoteBookFrame
#                   OptionMenu
#                   OptionName
#                   Pack
#                   PanedWindow
#                   PhotoImage
#                   Place
#                   PopupMenu
#                   Radiobutton
#                   ResizeHandle
#                   Scale
#                   Scrollbar
#                   ScrolledGrid
#                   ScrolledHList
#                   ScrolledListBox
#                   ScrolledTList
#                   ScrolledText
#                   ScrolledWindow
#                   Select
#                   Shell
#                   Spinbox
#                   StdButtonBox
#                   Text
#                   Tree
#                   Tributton
#
# See also:
# [Tix, ttk and Tkinter ](http://poquitopicante.blogspot.de/2013/05/tix-ttk-and-tkinter.html)
#
# For starters, we use ttk over tkinter if available, to replace
# standard widgets with their more shiny counterparts:
#
USING_TTK = False
STYLE = None

try:
    import tkinter.ttk as ttk

except ImportError:

    try:

        # Support Python 2.7
        #
        import ttk

    except ImportError:

        # TODO: Use logging module for warnings
        #
        sys.stderr.write("Warning: ttk unavailable" + "\n")

        ttk = None

if ttk is not None:

    # Diving into Python internals! "Everything is an object" boils
    # down to "Everything has a __dict__". :-)
    #
    for key in ttk.__dict__.keys():

        # Restrict to actual exported items.
        # Don't mess with ttk.Widget
        #
        if (key in tkinter.__dict__.keys()
            and not key.startswith("_")
            and key != "Widget"):

            sys.stderr.write("Setting tkinter.{0} -> ttk.{0}".format(key) + "\n")

            tkinter.__dict__[key] = ttk.__dict__[key]

    USING_TTK = True

# Then, we use Tix in a separate namespace
#
try:

    import tkinter.tix as tix

except ImportError:

    # Support Python 2.x
    #
    import Tix as tix

# Now that does not mean a lot. Check it.
#
t = tkinter.Tk()

t.withdraw()

try:
    t.tk.eval('package require Tix')

except:

    # "TclError: can't find package Tix"
    #
    tix = None
    
t.destroy()

t = None


class GUI:
    """Base class for a window to add widgets to.
    """

    def __init__(self, title = "simplegui GUI"):
        """Initialise. Call this first before calling any other tkinter routines.
        """

        if tix is not None:

            # To access Tix widgets, Tix' Tk must be the root
            #
            self.root = tix.Tk()

        else:

            self.root = tkinter.Tk()

        #self.root = tkinter.Toplevel()

        self.style = None

        if USING_TTK:

            self.style = ttk.Style()

        self.root.title(title)

        self.frame = tkinter.Frame(master = self.root)

        self.frame.pack(fill = "both")

        self.statusbar = tkinter.Label(master = self.frame,
                                       text = "simplegui (tkinter {0})".format(tkinter.TkVersion))

        self.statusbar.pack(padx = 10, pady = 5)

        return

    def status(self, text):
        """Display the new status text in the status bar.
        """

        self.statusbar["text"] = text

        return


    def center(self):
        """Center the root window on screen.
        """

        self.root.update()

        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()

        windowwidth = self.root.winfo_width()
        windowheight = self.root.winfo_height()
        
        self.root.geometry("+{0}+{1}".format(int(screenwidth / 2 - windowwidth / 2),
                                             int(screenheight / 2 - windowheight / 2)))

        return

    def run(self):
        """ Run the tkinter mainloop.
        """

        self.root.mainloop()

        return

    def button(self, label, callback):
        """Add a button.
        """

        tkinter.Button(master = self.frame,
                       text = label,
                       command = callback).pack(padx = 10, pady = 5)

        return

    def listbox(self, stringlist, callback):
        """Add a listbox.
           Klicking an entry in listbox will call callback(entry),
           where entry is a string.
        """

        stringvar = tkinter.StringVar(value = tuple(stringlist))

        listbox = tkinter.Listbox(master = self.frame,
                                  height = len(stringlist),
                                  listvariable = stringvar)

        listbox.pack(padx = 10, pady = 5)

        def callbackwrapper(event):
            callback(event.widget.get(event.widget.curselection()[0]))

        listbox.bind("<<ListboxSelect>>", callbackwrapper)

        return

    def scale(self, scalelabel, callback):
        """Add a scale.
           Moving the scale will call callback(value), where value is a
           float 0..1.
        """

        if USING_TTK:

            # No label option for ttk Scale
            #
            self.label(scalelabel)

            # No showvalue option for ttk Scale
            #
            value_label = tkinter.Label(master = self.frame,
                                        text = "0")

            value_label.pack(padx = 10, pady = 5)

            def callbackwrapper(value):

                # ttk.Scale calls back with a float string
                #
                value_label["text"] = int(float(value) * 100)

                callback(float(value))

            self.style.configure("Simplegui.Horizontal.TScale",
                                 orient = "horizontal",
                                 length = 100,
                                 sliderlength = 10)

            tkinter.Scale(master = self.frame,
                          command = callbackwrapper,
                          style = "Simplegui.Horizontal.TScale").pack(padx = 10, pady = 5)

        else:

            def callbackwrapper(value):

                # Original tkinter.Scale calls back with an int string
                #
                callback(int(value) / 100.0)

            tkinter.Scale(master = self.frame,
                          label = scalelabel,
                          orient = "horizontal",
                          length = 100,
                          showvalue = "true",
                          sliderlength = 10,
                          command = callbackwrapper).pack(padx = 10, pady = 5)

        return

    def label(self, text):
        """Add a label.
        """

        tkinter.Label(master = self.frame,
                      text = text).pack(padx = 10, pady = 5)

        return

    def bar(self):
        """Add a bar for progress or meter display.

           Returns a function to be called with a float 0..1.
        """

        if USING_TTK:

            # This is not a standard widget, so we get it from
            # ttk directly.
            # We use dimensions as with Scale.
            # TODO: centralise these values somewhere
            #
            bar = ttk.Progressbar(master = self.frame,
                                          orient = "horizontal",
                                          length = 100,
                                          mode = "determinate",
                                          maximum = 100,
                                          value = 0)

            bar.pack(padx = 10, pady = 5)

            def callback(value):

                bar["value"] = int(value * 100)

                return

            return callback

        elif tix is not None:

            # We use dimensions as with Scale.
            # TODO: centralise these values somewhere
            # Setting text to whitespace to prevent displaying percentages.
            #
            bar = tix.Meter(master = self.frame,
                            text = " ",
                            value = 0.0)

            bar.pack(padx = 10, pady = 5)

            def callback(value):

                bar["value"] = value

                return

            return callback

        else:

            # TODO: implement fallback
            sys.stderr.write("No scrollbar\n")

        return
