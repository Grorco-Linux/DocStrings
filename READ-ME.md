CAUTION: This app will try to import every module and package from your sys.path
if you do not have the file moddict.json that was provided with this package.
When you open this any modules that do not include the if __name__ == '_main__'
statement will run any code they contain. However I have quieted the text output
and will be seeking a workaround for the rest. I will upload a copy of the JSON
file containing the dictionaries created from my sys.path. If you do not want this
to try to import everything you have keep this file with the others!

In my next version I will be implementing selective updates for that file and 
the ability to import missing modules the user dictionary created I will add a 
selective restore/ update to as well.

I hope that this will help people trying to learn python, as well as help even
the more experienced. Any suggestions are more than welcome, I wanted to try to 
keep this as simple to use as possible. I will probably end up adding menu's
to accommodate the future updates, but we will see.

I would like to give a special thanks to mandeep, _habnabit, The-Compiler, and all the
other people @ irc channel #python, and #pyqt for their help. 

-Grorco<grorco.linux@gmail.com>
