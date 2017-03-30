"""Convenience function for sending mail

   Copyright (c) 2009, 2017 Florian Berger <florian.berger@posteo.de>
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

# Adapted from mailtool.py, started on 17. Feb 2009, on 30 Mar 2017.
# mailtool.py in turn was taken from my first quick-and-dirty MOWS
# (My Own Web Shop) implementation (mows.cgi) from June 2008.

import simple
import smtplib
import codecs

def send(sender,
         recipients,
         subject,
         body,
         host,
         user,
         password_rot13):

    SMTP = smtplib.SMTP(host)

    SMTP.set_debuglevel(1)

    SMTP.starttls()

    SMTP.login(user, codecs.decode(password_rot13, "rot13"))

    SMTP.sendmail(sender,
                  recipients,
                  "From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n{}".format(sender, recipients[0],subject, body))

    SMTP.quit()

    return

def encode_rot13(s):

    return codecs.encode(s, "rot13")
