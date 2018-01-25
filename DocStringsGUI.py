#!/usr/bin/python3.5
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# DocStrings and DocStringsGui created by Grorco <Grorco.Linux@gmail.com> 2016
# Main trunk at https://github.com/Grorco-Linux/DocStrings/


"""DocStringsGui is a graphical interpretation of DocStrings using PyQt5"""


import sys
import os
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QDialog, QTabBar, QCheckBox, QMenuBar, QMenu, QFileDialog,
                             QTextEdit, QGridLayout, QApplication, QListWidget, QLineEdit)
from PyQt5.QtCore import (QCoreApplication)
import PyQt5.QtCore as QtCore
import DocStrings
import DocStringSetup
import json
import copy



class DocStringsGUI(QWidget):
    
    def __init__(self):
        super().__init__()

        self.mod_dict_setup()

        # Make a list for new windows created and a var to keep track of how many there are
        self.pop_list = []
        self.pop_amount = 0
        # Setup child widgets
        self.child_setup()

        # Make connections
        self.mod_name_listbox.itemSelectionChanged.connect(self.doc_str_change)
        self.mod_name_listbox.itemSelectionChanged.connect(self.attr_list_change)
        self.attr_name_listbox.itemSelectionChanged.connect(self.doc_str_change_attr)
        self.exitButton.clicked.connect(self.exit)
        self.editButton.clicked.connect(self.save_changes)
        self.popButton.clicked.connect(self.window_pop)
        self.favButton.clicked.connect(self.fav)
        self.search_line.textChanged[str].connect(self.search)
        self.tabs.tabBarClicked.connect(self.get_tabs)
        # Size, place, and show the Window
        self.mod_name_listbox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.resize(1300, 300)
        self.show()

    def mod_dict_setup(self):
        # modDocList contains a dictionary of mod names, with their classes and functions and doc strings.
        self.mod_doc_dict = check_file()
        # A shallow copy so the user can make changes without muking it up.
        self.user_dict = copy.copy(self.mod_doc_dict)
        try:
            with open('usrdict.json', 'r') as f:
                f.close()
        except:
            with open('usrdict.json', 'w') as f:
                json.dump(self.user_dict, f)
            f.close()

    def get_tabs(self):
        self.mod_name_listbox.clear()
        if self.tabs.currentIndex() == 0:
            for key in self.mod_doc_dict.keys():
                if '*' in key:
                    self.mod_name_listbox.addItem(key)
        else:
            for key in self.mod_doc_dict.keys():
                self.mod_name_listbox.addItem(key)

        self.mod_name_listbox.sortItems()

    def search(self):
        self.mod_name_listbox.clear()
        # Search for all tab.
        if self.tabs.currentIndex() == 0:
            if self.search_line.text() == '':
                for key in self.mod_doc_dict.keys():
                    self.mod_name_listbox.addItem(key)
            else:
                if self.doc_checkbox.isChecked():
                    for key in self.mod_doc_dict.keys():
                        if self.search_line.text() in self.mod_doc_dict[key][0]:
                            self.mod_name_listbox.addItem(key)

                for key in self.mod_doc_dict.keys():
                    if self.search_line.text() in key:
                        self.mod_name_listbox.addItem(key)

        # Search for Favorites tab.
        else:
            for key in self.mod_doc_dict.keys():
                if '*' in key and self.search_line.text() in key:
                    self.mod_name_listbox.addItem(key)
        self.mod_name_listbox.sortItems()


    def fav(self):
        if not self.mod_name_listbox.currentItem().text().startswith('*'):
            self.user_dict[str('*' + self.mod_name_listbox.currentItem().text())
                              ] = self.user_dict.pop(self.mod_name_listbox.currentItem().text())
            self.mod_doc_dict[str('*' + self.mod_name_listbox.currentItem().text())
                              ] = self.mod_doc_dict.pop(self.mod_name_listbox.currentItem().text())
            self.mod_name_listbox.currentItem().setText('*' + self.mod_name_listbox.currentItem().text())
        else:
            self.user_dict[self.mod_name_listbox.currentItem().text().replace('*', '')
                              ] = self.user_dict.pop(self.mod_name_listbox.currentItem().text())
            self.mod_doc_dict[self.mod_name_listbox.currentItem().text().replace('*', '')
                              ] = self.mod_doc_dict.pop(str(self.mod_name_listbox.currentItem().text()))
            self.mod_name_listbox.currentItem().setText(str(self.mod_name_listbox.currentItem().text()).replace('*', ''))


        with open('usrdict.json', 'w') as f:
            json.dump(self.user_dict, f)
        f.close()
    def window_pop(self):

        try:
            self.pop_list.append(PopWindow(self.doc_str_textbox.toPlainText(), self.pop_window_title).exec_())
        except:
            self.doc_str_textbox.setText('Please select a module, class, or function before trying to pop the window!')

    def save_changes(self):
        # Delete usrdict.json to reset changes
        try:
            if self.mod_doc_dict[self.mod_name_listbox.currentItem().text()
                               ][1][self.attr_name_listbox.currentItem().text().split(' ', 2)[1]][1] is not None:
                modname = self.attr_name_listbox.currentItem().text().split(' ', 2)[1]
                self.user_dict[self.mod_name_listbox.currentItem().text()][1][modname][1] = self.doc_str_textbox.toPlainText()
        except AttributeError:
            try:
                self.user_dict[self.mod_name_listbox.currentItem().text()][0] = self.doc_str_textbox.toPlainText()
            except AttributeError:
                pass
        with open('usrdict.json', 'w') as f:
            json.dump(self.user_dict, f)
        f.close()

    def doc_str_change(self):
        # change the docStr text to match the selected mod
        self.doc_str_textbox.setText(self.mod_doc_dict[self.mod_name_listbox.currentItem().text()][0])
        self.pop_window_title = self.mod_name_listbox.currentItem().text()

    def doc_str_change_attr(self):
        # change the doc_str text to match the selected attr
        mod = self.mod_name_listbox.currentItem().text()
        attr = self.attr_name_listbox.currentItem().text().split(' ', 2)[1]
        self.pop_window_title = mod + ': ' + self.attr_name_listbox.currentItem().text()
        try:
            doc_str = self.mod_doc_dict[mod][1][attr][1]
        except KeyError:
            doc_str = 'None'
        self.doc_str_textbox.setText(doc_str)

    def attr_list_change(self):
        # If the attr listbox isn't empty, empty it then fill it
        self.attr_name_listbox.clear()
        # Make a list of attributes for the selected module from self.mod_doc_dict
        attr_name_list = self.mod_doc_dict[self.mod_name_listbox.currentItem().text()][1]
        for i in attr_name_list.keys():
            self.attr_name_listbox.addItem(str(attr_name_list[i][0]) + str(i))
        self.attr_name_listbox.sortItems()

    def child_setup(self):
        # Set window title and make the labels and doc_str_textbox
        self.setWindowTitle('DocStrings GUI!')
        self.modNamelbl = QLabel('Module Names')
        self.attrlbl = QLabel('Attributes')
        self.docStrlbl = QLabel('Doc Strings')
        self.doc_str_textbox = QTextEdit(self)
        # Make the list boxes
        self.mod_name_listbox = QListWidget(self)
        self.attr_name_listbox = QListWidget(self)
        self.populate_childs()

    def populate_childs(self):
        # Add items, then sort them
        for mod in self.mod_doc_dict.keys():
            self.mod_name_listbox.addItem(mod)
        self.mod_name_listbox.sortItems()
        # Set the size of the list boxes
        self.mod_name_listbox.setFixedSize(350, 500)
        self.attr_name_listbox.setFixedSize(350, 500)
        self.doc_str_textbox.setFixedSize(500, 500)
        # Create buttons
        self.favButton = QPushButton('Favorite')
        self.popButton = QPushButton('POP!')
        self.editButton = QPushButton('Save Edit')
        self.exitButton = QPushButton('Exit')
        # Create Search Bar
        self.search_line = QLineEdit('Search')
        self.tabs = QTabBar()
        self.tabs.addTab('All')
        self.tabs.addTab('Favorites')
        self.doc_checkbox = QCheckBox('Include Doc Strings in search')

    def exit(self):
        if mainWindow.pop_amount is not 0:
            mainWindow.setHidden(True)
        else:
            QCoreApplication.instance().exit()
    def menu_setup(self):
        self.menubar = MenuBar()




    def grid_setup(self):

        #  ---TitleBar--------------------------------|
        #  modNamelbl-------attNameListbox---docStrlbl|0
        #  modNamelistbox---attNameListbox--docStrText|1
        #  modNamelistbox---attNameListbox--docStrText|2
        #  modNamelistbox---attNameListbox--docStrText|3
        #  modNamelistbox---attNameListbox--docStrText|4
        #  modNamelistbox---attNameListbox--docStrText|5
        #  -------------------------------------------|6
        #  ----favbtn---popbtn----addbtn---exitbtn----|7
        #  ________________StatusBar__________________|8
        # 0   1    2    3    4    5    6    7    8

        # Make the grid and set spacing then place widgets in it

        self.grid = QGridLayout()
        self.grid.setSpacing(1)

        label = QLabel()
        self.grid.addWidget(label)
        self.grid.addWidget(self.menubar, 0,1,1,40)
        self.grid.addWidget(self.doc_checkbox, 7, 6)
        self.grid.addWidget(self.tabs, 1, 3)
        self.grid.addWidget(self.modNamelbl, 1, 1)
        self.grid.addWidget(self.attrlbl, 1, 4)
        self.grid.addWidget(self.docStrlbl, 1, 7)
        self.grid.addWidget(self.mod_name_listbox, 2, 1, 5, 3)
        self.grid.addWidget(self.attr_name_listbox, 2, 4, 5, 3)
        self.grid.addWidget(self.doc_str_textbox, 2, 7, 5, 3)
        self.grid.addWidget(self.favButton, 7, 2)
        self.grid.addWidget(self.popButton, 7, 7)
        self.grid.addWidget(self.editButton, 7, 8)
        self.grid.addWidget(self.exitButton, 7, 9)
        self.grid.addWidget(self.search_line, 8, 6)
        # Change the layout to the grid
        self.setLayout(self.grid)

class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()

        # Make all of the menus
        self.file_menu = MenuFile()
        self.addMenu(self.file_menu)
        self.edit_menu = MenuEdit()
        self.addMenu(self.edit_menu)
        self.options_menu = MenuOptions()
        self.addMenu(self.options_menu)



class MenuOptions(QMenu):
    def __init__(self):
        super().__init__('&Options')

        # Add actions and their connections to the menu
        self.addpath = self.addAction('Add Path...')
        self.addpath.triggered.connect(self.add_path)

    def add_path(self):
        self.path_window = [QFileDialog().getExistingDirectory(caption='Add Path')]
        print(self.path_window)
        DocStringSetup.main(self.path_window)
        DocStringSetup.modlist()
        mainWindow.mod_dict_setup()
        mainWindow.populate_childs()


class MenuFile(QMenu):
    def __init__(self):
        super().__init__('&File')

        # Add actions and their connections to the menu
        exit_action = self.addAction('Exit')
        exit_action.triggered.connect(mainWindow.exit)

    def exit(self):
        if mainWindow.pop_amount is not 0:
            mainWindow.setHidden(True)
        else:
            QCoreApplication.instance().exit()


class MenuEdit(QMenu):
    def __init__(self):
        super().__init__('&Edit')

        # Add actions and their connections to the menu
        self.save_change_action = self.addAction('Save Changes')
        self.save_change_action.triggered.connect(mainWindow.save_changes)



class PopWindow(QDialog):
    def __init__(self, doc_str_text='', pop_window_title=''):
        super().__init__()
        mainWindow.pop_amount += 1
        self.setWindowTitle(pop_window_title)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.DocStr = QTextEdit()
        self.DocStr.setText(doc_str_text)
        self.resize(300, 300)
        self.pop_grid = QGridLayout()
        self.pop_grid.addWidget(self.DocStr)
        self.setLayout(self.pop_grid)

        self.show()

    def closeEvent(self, event):
        mainWindow.pop_amount -= 1
        event.accept()



# import DocStringSetup first to insure modlist.py exist and is up to date
def check_file():
    while True:

        try:
            with open('usrdict.json', 'r') as f:
                try:
                    moddict = json.load(f)
                    return moddict
                    break
                # if the file is empty the ValueError will be thrown
                except ValueError:
                    moddict = {}
                    return moddict
                    break
        except FileNotFoundError:
            try:
                with open('moddict.json', 'r') as f:

                    try:
                        moddict = json.load(f)
                        return moddict
                        break
                    # if the file is empty the ValueError will be thrown
                    except ValueError:
                        moddict = {}
                        return moddict
                        break

            except FileNotFoundError:
                # Creates the file
                import DocStringSetup
                DocStringSetup.main(sys.path)
                DocStringSetup.modlist()
                pass

        
if __name__ == '__main__':
    try:
        check_file()
    except:
        pass
    sys.stdout = open(os.devnull, 'w')
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    mainWindow = DocStringsGUI()
    mainWindow.menu_setup()
    mainWindow.grid_setup()

    sys.exit(app.exec_())
