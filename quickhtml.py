"""quickhtml - Python classes to quickly create HTML documents

   Originating from the Building Block 2 CMS

   Outsourced on 14 Feb 2009

   Copyright 2009, 2012 Florian Berger <fberger@florian-berger.de>
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

# Import into Bazaar Sat Feb 25 16:10:15 CET 2012.

# TODO
#
# - use string.Template for all string building

VERSION = "0.1.0"

# Dimensions of a Textarea
#
ROWS = 20
COLS = 60

DOCTYPE = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'

def build_table_row(DataList):
    """This method returns a HTML table row containing the table data from the list given.
    """

    HTML = '<tr>'

    for Data in DataList:
        HTML = HTML + '<td>' + Data + '</td>'

    HTML = HTML + '</tr>'

    return(HTML)

class Page:
    """This is a helper class to easily create HTML documents.

       Attributes:

       Page.title
           The document title.

       Page.css
           The document inline stylesheets.

       Page.body
           The document body.

       Page.link_dict
           A dictionary containing relation identifiers pointing to URIs,
           as {"stylesheet" : "/stylesheet.css"}.
    """

    def __init__(self, title, css = "", body = "", link_dict = None):
        """Initialize the document with a title, an optional CSS section to be put in <style></style> and optional body content.

           body, if given, must be a string containing valid HTML.

           link_dict is an optional dictionary to create <link> elements in the
           HTML head. It must contain relation identifiers pointing to URIs,
           as {"stylesheet" : "/stylesheet.css"}.
        """

        self.title = title
        self.css = css
        self.body = body

        if link_dict is None:

            self.link_dict = {}

        else:
            self.link_dict = link_dict

        return

    def append(self, HTML):
        """Append HTML to the body of the document.
        """

        self.body = self.body + HTML

        return

    def __str__(self):
        """Return the complete HTML document.
        """

        link_str = ''.join(['<link rel="{0}" href="{1}">'.format(link, uri) for link, uri in self.link_dict.items()])

        document_str = '{0}<html><head><title>{1}</title>{2}<style type="text/css">{3}</style></head><body>{4}</body></html>'

        return(document_str.format(DOCTYPE,
                                   self.title,
                                   link_str,
                                   self.css,
                                   self.body))

class Form:
    """This is a helper class to quickly create HTML forms.
    """

    def __init__(self, action, method, separator, submit_label):
        """Initialize the form.
           action must be an URI to call and method must be GET or POST.
           separator separates the fieldset elements.
           submit_label is the value for the submit element.
        """

        # TODO: Do we need to specify action
        # at all, or does POST suffice?
        #
        self.action = action
        self.method = method
        self.separator = separator
        self.submit_label = submit_label
        self.fieldsets = {}
        self.current_fieldset = ''
        self.hidden = ''
        self.no_fieldset = ''

        return

    def add_fieldset(self, legend):
        """Add a new fieldset and make it the current.
        """

        self.fieldsets[legend] = ''
        self.current_fieldset = legend

        return

    def add_input(self, label, type, name, value = '', checked = ''):
        """Add a new input element.
           If there is a current fieldset, add it there.
           The optional arguments value, checked are there for creating
           checkboxes.
           They are used by the proxy method add_checkbox(). Normal call is

           add_input(self, label, type, name)
        """

        label_html = '<label for="' \
                    + name \
                    + '">' \
                    + label \
                    + '</label>'

        input_html = '<input type="' \
                    + type \
                    + '" name="' \
                    + name

        if value:
            input_html = input_html + '" value="' + value

        if checked:
            input_html = input_html + '" checked="checked'

        input_html = input_html + '" id="'  \
                              + name  \
                              + '">'

        if self.current_fieldset:

            self.fieldsets[self.current_fieldset] = self.fieldsets[self.current_fieldset] \
                                                   + build_table_row( [ label_html , input_html ] )

        else:
            self.no_fieldset = self.no_fieldset + label_html + input_html + self.separator

        return

    def add_checkbox(self, label, name, value, checked):
        """Add a checkbox.
           This method acts as a proxy to add_input()
        """

        self.add_input(label, 'checkbox', name, value, checked)

        return

    def add_textarea(self, name, content = ""):
        """Add a text area to the form or the current fieldset (if any).
        """

        HTML = '<textarea name="{0}" rows="{1}" cols="{2}">{3}</textarea>'

        HTML = HTML.format(name, str(ROWS), str(COLS), content)

        if self.current_fieldset:

            self.fieldsets[self.current_fieldset] = self.fieldsets[self.current_fieldset] \
                                                   + '<tr><td colspan="2">' + HTML + '</td></tr>'

        else:
            self.no_fieldset = self.no_fieldset + HTML + self.separator

        return

    def add_drop_down_list(self, label, name, list):
        """Add a drop down list to the form or the current fieldset (if any).
           list is a list of values to select from.
        """

        label_html = '<label for="' \
                    + name \
                    + '">' \
                    + label \
                    + '</label>'

        list_html = '<select name="' \
                    + name  \
                    + '" size="1">'

        for value in list:
            list_html = list_html + '<option>' + value + '</option>'

        list_html = list_html + '</select>'

        if self.current_fieldset:

            self.fieldsets[self.current_fieldset] = self.fieldsets[self.current_fieldset] \
                                                   + build_table_row( [ label_html , list_html ] )

        else:
            self.no_fieldset = self.no_fieldset + label_html + list_html + self.separator

        return

    def add_hidden(self, name, value):
        """Add a new hidden element to the form.
        """

        self.hidden = self.hidden + '<input type="hidden" name="' \
                   + name  \
                   + '" value="'  \
                   + value  \
                   + '">'

        return

    def __str__(self):
        """Return the HTML form as a string.
        """

        # Use enctype="multipart/form-data" to be able to upload files with
        # <input type="file">
        #
        HTML = '<form action="' \
               + self.action \
               + '" method="' \
               + self.method \
               + '" enctype="multipart/form-data">'

        HTML = HTML + self.no_fieldset

        for legend in self.fieldsets.keys():
            HTML = HTML + '<fieldset><legend>' \
                   + legend \
                   + '</legend><table>' \
                   + self.fieldsets[legend] \
                   + '</table></fieldset>'

        HTML = HTML + self.hidden + '<button type="submit">' + self.submit_label + '</button></form>'

        return(HTML)
