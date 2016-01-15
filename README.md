Somtoday api
============

A python and php wrapper for the api somtoday uses in their mobile app

It uses a GPL licence, wich is summarized [here](http://choosealicense.com/licenses/gpl-2.0/).

The school abbreveations can be found [here](http://servers.somtoday.nl)

Python
===========

Installation
============
1. Extract into a folder
2. ``python setup.py install``
3. ???
4. SUCCES!

Examples
===========
```python
From somtoday import * #import everything this module has to offer

som=Somtoday("henk","mypassword","myschool","dembrin") #create a new somtoday object

for vak in som.gethomework(): #print the subject for you have homework for in the coming 2 weeks.
    print vak["vak"]

som.changehomeworkstatus("6374673","7364736", True)#mark homework done
```
Footnote
=======
questions? ricktrein@hotmail.com

PHP
=========
The PHP wrapper has moved to a repository and the wrapper will be maintained by Rick Bakker. (@RickBakkr)

You can find the new repo here:
https://github.com/RickBakkr/SOMtoday
