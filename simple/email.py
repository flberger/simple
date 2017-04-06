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

# TODO: Log errors from send_threaded() somewhere, in good Python spirit.

import simple
import smtplib
import codecs
import threading
import io
import traceback
import os
import pathlib
import datetime

def send(sender,
         recipients,
         subject,
         body,
         host,
         user,
         password_rot13):
    """Send an email via SMTP.
    """

    # smtplib logs to stderr, so we need to jump through some
    # hoops to capture the log.
    # Idea taken from http://stackoverflow.com/a/7303587/1132250
    #
    logging_sink = io.StringIO()

    original_stderr = smtplib.stderr

    smtplib.stderr = logging_sink

    try:
        SMTP = smtplib.SMTP(host)

        SMTP.set_debuglevel(1)

        SMTP.starttls()

        SMTP.login(user, codecs.decode(password_rot13, "rot13"))

        SMTP.sendmail(sender,
                      recipients,
                      "From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n{}".format(sender, recipients[0],subject, body))

        SMTP.quit()

    except:

        smtplib.stderr = original_stderr

        # Log error to file
        #
        with pathlib.Path(os.environ["PWD"], "smtp_errors.log").open("at", encoding = "utf8") as f:

            f.write("--- {} ---\n".format(datetime.datetime.now()))

            f.write(logging_sink.getvalue())

            traceback.print_exc(file = f)

            f.write("\n")

        raise

    smtplib.stderr = original_stderr
        
    return

def send_threaded(sender,
                  recipients,
                  subject,
                  body,
                  host,
                  user,
                  password_rot13):
    """Run send() in a background thread, immediately returning after the call.
       Exceptions when sending will terminate the thread, but not the main program.
    """
    
    send_thread = threading.Thread(target = send,
                                   args = (sender,
                                           recipients,
                                           subject,
                                           body,
                                           host,
                                           user,
                                           password_rot13))

    send_thread.start()

    return

def encode_rot13(s):
    """Encode a string in rot13.
    """

    return codecs.encode(s, "rot13")
