'''quickhtml - Python classes to quickly create HTML documents

   Originating from the Building Block 2 CMS

   Outsourced on 14 Feb 2009

   Copyright 2009, 2012 Florian Berger <fberger@florian-berger.de>
'''

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

def build_table_row(DataList):
    '''This method returns a HTML table row containing the table data from the list given.
    '''

    HTML = '<tr>'

    for Data in DataList:
        HTML = HTML + '<td>' + Data + '</td>'

    HTML = HTML + '</tr>'

    return(HTML)

class Page:
    '''This is a helper class to easily create HTML documents.

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
    '''

    def __init__(self, title, css = "", body = "", link_dict = None):
        '''Initialize the document with a title, an optional CSS section to be put in <style></style> and optional body content.

           body, if given, must be a string containing valid HTML.

           link_dict is an optional dictionary to create <link> elements in the
           HTML head. It must contain relation identifiers pointing to URIs,
           as {"stylesheet" : "/stylesheet.css"}.
        '''

        self.title = title
        self.css = css
        self.body = body

        if link_dict is None:

            self.link_dict = {}

        else:
            self.link_dict = link_dict

    def append(self, HTML):
        '''Append HTML to the body of the document.
        '''

        self.body = self.body + HTML

    def __str__(self):
        '''Return the complete HTML document.
        '''

        return('<html><head><title>'
               + self.title
               + '</title><style type="text/css">'
               + self.css
               + '</style></head><body>'
               + self.body
               + '</body></html>')

class Form:
    '''This is a helper class to quickly create HTML forms.
    '''

    def __init__(self, Action, Method, Separator, SubmitLabel):
        '''Initialize the form.
           Action must be an URI to call and Method must be GET or POST.
           Separator separates the fieldset elements.
           SubmitLabel is the value for the submit element.
        '''

        # TODO: Do we need to specify Action
        # at all, or does POST suffice?
        #
        self.Action = Action
        self.Method = Method
        self.Separator = Separator
        self.SubmitLabel = SubmitLabel
        self.Fieldsets = {}
        self.CurrentFieldset = ''
        self.Hidden = ''
        self.NoFieldset = ''

    def add_fieldset(self, Legend):
        '''Add a new fieldset and make it the current.'''

        self.Fieldsets[Legend] = ''
        self.CurrentFieldset = Legend

    def add_input(self, Label, Type, Name, Value = '', Checked = ''):
        '''Add a new input element.
           If there is a current fieldset, add it there.
           The optional arguments Value, Checked are there for creating
           checkboxes.
           They are used by the proxy method add_checkbox(). Normal call is

           add_input(self, Label, Type, Name)
        '''

        LabelHTML = '<label for="' \
                    + Name \
                    + '">' \
                    + Label \
                    + '</label>'

        InputHTML = '<input type="' \
                    + Type \
                    + '" name="' \
                    + Name

        if Value:
            InputHTML = InputHTML + '" value="' + Value

        if Checked:
            InputHTML = InputHTML + '" checked="checked'

        InputHTML = InputHTML + '" id="'  \
                              + Name  \
                              + '">'

        if self.CurrentFieldset:

            self.Fieldsets[self.CurrentFieldset] = self.Fieldsets[self.CurrentFieldset] \
                                                   + build_table_row( [ LabelHTML , InputHTML ] )

        else:
            self.NoFieldset = self.NoFieldset + LabelHTML + InputHTML + self.Separator

    def add_checkbox(self, Label, Name, Value, Checked):
        '''Add a checkbox.
           This method acts as a proxy to add_input()
        '''

        self.add_input(Label, 'checkbox', Name, Value, Checked)

    def add_textarea(self, Name, Content):
        '''Add a text area to the form or the current fieldset (if any).
        '''

        HTML = '<textarea name="' \
               + Name  \
               + '" rows="' \
               + str(ROWS) \
               +'" cols="' \
               + str(COLS) \
               +'">' \
               + Content \
               + '</textarea>'

        if self.CurrentFieldset:

            self.Fieldsets[self.CurrentFieldset] = self.Fieldsets[self.CurrentFieldset] \
                                                   + '<tr><td colspan="2">' + HTML + '</td></tr>'

        else:
            self.NoFieldset = self.NoFieldset + HTML + self.Separator

    def add_drop_down_list(self, Label, Name, List):
        '''Add a drop down list to the form or the current fieldset (if any).
           List is a list of values to select from.
        '''

        LabelHTML = '<label for="' \
                    + Name \
                    + '">' \
                    + Label \
                    + '</label>'

        ListHTML = '<select name="' \
                    + Name  \
                    + '" size="1">'

        for Value in List:
            ListHTML = ListHTML + '<option>' + Value + '</option>'

        ListHTML = ListHTML + '</select>'

        if self.CurrentFieldset:

            self.Fieldsets[self.CurrentFieldset] = self.Fieldsets[self.CurrentFieldset] \
                                                   + build_table_row( [ LabelHTML , ListHTML ] )

        else:
            self.NoFieldset = self.NoFieldset + LabelHTML + ListHTML + self.Separator

    def add_hidden(self, Name, Value):
        '''Add a new hidden element to the form.
        '''

        self.Hidden = self.Hidden + '<input type="hidden" name="' \
                   + Name  \
                   + '" value="'  \
                   + Value  \
                   + '">'

    def __str__(self):
        '''Return the HTML form as a string.
        '''

        # Use enctype="multipart/form-data" to be able to upload files with
        # <input type="file">
        #
        HTML = '<form action="' \
               + self.Action \
               + '" method="' \
               + self.Method \
               + '" enctype="multipart/form-data">'

        HTML = HTML + self.NoFieldset

        for Legend in self.Fieldsets.keys():
            HTML = HTML + '<fieldset><legend>' \
                   + Legend \
                   + '</legend><table>' \
                   + self.Fieldsets[Legend] \
                   + '</table></fieldset>'

        HTML = HTML + self.Hidden + '<button type="submit">' + self.SubmitLabel + '</button></form>'

        return(HTML)
