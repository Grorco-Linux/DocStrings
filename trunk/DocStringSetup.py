#!/usr/bin/python3.5
import sys
import os
from os import walk
import keyword

mods = []


def main(paths):
    for path in paths:
        for dirName, subdirList, fileList in walk(path):
            dirName = dirName.split(path, 1)[1].lstrip('/')
            if '-' not in dirName and not dirName.startswith('.') and not '__pycache__' in dirName:
                if '__init__.py' in fileList:
                    for file in fileList:
                        if file.endswith('.py') and not '__init__.py' in file and not '-' in file:
                            file = file.split('.')[0]
                            if file not in keyword.kwlist:
                                if dirName is '':
                                    mods.append(file)
                                else:
                                    mods.append(dirName.replace('/', '.') + '.' + file.split('.')[0])
                else:
                    for file in fileList:
                        if file.endswith('.py') and not '-' in file and 'DocString' not in file and 'modlist' \
                                not in file:
                            mods.append(file)
    if len(mods) is not 0:
        modlistfile = open('modlist.py', 'w')
        modlistfile.write(
"""
import sys
import os
import json
import DocStrings
from contextlib import contextmanager
import_error = 0

@contextmanager
def quiet():
    sys.stdout = sys.stderr = open(os.devnull, "w")
    try:
        yield
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

with quiet():\n""")

        for mod in mods:
            modlistfile.write('    try: \n')
            modlistfile.write("        import " + mod + " as a\n")
            modlistfile.write('    except: \n        import_error +=1 \n')
        modlistfile.write("""try:
    with open('usrdict.json', 'r') as f:
        usrdict = json.load(f)
except:
    print('no dict')
    usrdict = {}

mydict = DocStrings.print_all_mod_doc()
for mod in mydict:
    attrlist = DocStrings.print_type(mod)
    for attr in attrlist:
        attrdoc = DocStrings.print_attr_doc(str(mod), str(attr[1]))
        mydict[mod][1][attr[1]] = [str(attr[0]), str(attrdoc)]
print(import_error)
usrdict.update(mydict)
try:
    with open('usrdict.json', 'r') as f:
        f.close()
    with open('usrdict.json', 'w') as f:
        json.dump(usrdict, f)
        f.close()
except FileNotFoundError:
    moddictfile = open('moddict.json', 'w')
    json.dump(usrdict, moddictfile)
    moddictfile.close()
""")
        modlistfile.close()
    else:
        modlistfile = open('modlist.py', 'w')
        modlistfile.write('empty')
        modlistfile.close()

def modlist():
    import modlist
    os.remove(modlist.__file__)
if __name__ == '__main__':
    main(sys.path)
    modlist()