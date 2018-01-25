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
# DocStrings and DocStringsGui created by Grorco<Grorco.Linux@gmail.com> 2016

import sys
import inspect
import json


"""Prints out doc strings and attributes for modules, classes, etc.."""

def print_mod():
    """Prints out a list of available modules and returns a list of them"""
    modList = []
    for key in sys.modules.keys():
        modList.append(key + '\n')
        print(key)
    return modList
        
def print_mod_doc(key):
    """Prints out the doc string for a named module"""
    print(sys.modules.get(key))
    print(sys.modules.get(key).__doc__)
    
def print_all_mod_doc(setup = False):
    """Prints out the name and doc string for all available modules"""

    print(sys.modules)
    moddict = {}

    for key in sys.modules.keys():
        print(key)
        try:
            print(sys.modules.get(key).__doc__)
            moddict[key] = [str(sys.modules.get(key).__doc__), {}]
        except AttributeError:
            pass

    return moddict

def print_attr(key):
    """Prints the attributes for modules, classes, etc.."""
    
    print(dir(key))

def print_attr_doc(mod, attr):
    """Print the doc string for the attribute of a class"""
    x = sys.modules.get(mod)
    attrDocStr = getattr(x,attr).__doc__
    print(getattr(x,attr).__doc__)

    return attrDocStr
    

def print_type(x):
    """Print whether a module attribute is a class, or function, \n otherwise ignore"""
    x = sys.modules.get(x)
    attrList = []
    try:
        for attr in dir(x):
            if inspect.isclass(getattr(x,attr)):

                print(attr, ' is a class type')
                attrList.append(['Class: ', str(attr)])

            elif inspect.isfunction(getattr(x,attr)):
                print(attr, ' is a function type')
                attrList.append(['Function: ', str(attr)])

    except TypeError:
        print(x, 'has no type')
    return attrList
        


