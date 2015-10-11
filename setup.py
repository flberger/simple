"""simple Setup Script

   Copyright (c) 2013--2015 Florian Berger <mail@florian-berger.de>
"""

# This file is part of simple.
#
# simple is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# simple is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with simple.  If not, see <http://www.gnu.org/licenses/>.

# Work started on 29. Jan 2013.

import simple

# Fallback
#
from distutils.core import setup

SCRIPTS = []

EXECUTABLES = []

try:
    import cx_Freeze

    setup = cx_Freeze.setup

    EXECUTABLES = [cx_Freeze.Executable(path) for path in SCRIPTS]

except ImportError:

    print("Warning: the cx_Freeze module could not be imported. You will not be able to build binary packages.")

LONG_DESCRIPTION = """About
-----

simple is a simplified GUI generator using Tkinter.

Prerequisites
-------------

Python http://www.python.org

Installation
------------

Unzip the file, then at the command line run

::

    python setup.py install

Usage
-----

::

    >>> import simple.gui
    >>> g = simple.gui.GUI()
    >>> def buttoncallback():
    ...     g.status("Button klicked!")
    >>> g.button("Klick me!", buttoncallback)
    >>> g.button("Klick me too!", buttoncallback)
    >>> def listboxcallback(text):
    ...     g.status("listbox select: '{0}'".format(text))
    >>> g.listbox(["one", "two", "three"], listboxcallback)
    >>> g.listbox(["A", "B", "C"], listboxcallback)
    >>> def scalecallback(text):
    ...     g.status("scale value: '{0}'".format(text))
    >>> g.scale("Scale me!", scalecallback)
    >>> g.run()
    >>>

Documentation
-------------

To read the API documentation, open a shell / DOS window, navigate to
the simple directory, and run

::

    pydoc simple

You can create a HTML version using

::

    pydoc -w simple

License
-------

simple is licensed under the GPL. See the file COPYING for details.

Author
------

Florian Berger
"""

# Python 2.x doesn't honour the 'package_dir' and 'package_data' arguments to
# setup() when building an 'sdist'. Generate MANIFEST.in containing the
# necessary files.
#
print("regenerating MANIFEST.in for Python 2.x")
MANIFEST = open("MANIFEST.in", "wt")
MANIFEST.write("include COPYING")
MANIFEST.close()

setup(name = "simple",
      version = simple.VERSION,
      author = "Florian Berger",
      author_email = "mail@florian-berger.de",
      url = "http://florian-berger.de/en/software/simple",
      description = "simple.gui - Simplified GUI generation using Tkinter",
      long_description = LONG_DESCRIPTION,
      license = "GPL",
      py_modules = ["simple.gui"],
      packages = [],
      requires = [],
      provides = ["simple.gui"],
      scripts = SCRIPTS,
      executables = EXECUTABLES)
