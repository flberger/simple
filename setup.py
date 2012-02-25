"""quickhtml Setup Script

   Copyright  Florian Berger <fberger@florian-berger.de>
"""

# This file is part of quickhtml.
#
# quickhtml is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# quickhtml is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with quickhtml.  If not, see <http://www.gnu.org/licenses/>.

# Work started on Sat Feb 25 16:10:15 CET 2012.

import distutils.core
import quickhtml

LONG_DESCRIPTION = ""

distutils.core.setup(name = "quickhtml",
                     version = quickhtml.VERSION,
                     author = "Florian Berger",
                     author_email = "fberger@florian-berger.de",
                     url = "http://florian-berger.de/en/software/quickhtml/",
                     description = "quickhtml - DESCRIPTION HERE",
                     long_description = LONG_DESCRIPTION,
                     license = "GPL",
                     py_modules = ["quickhtml"],
                     packages = [],
                     requires = [],
                     provides = ["quickhtml"],
                     scripts = [],
                     data_files = [("", ["COPYING"])])

