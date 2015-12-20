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
Stephan Meijer was feeling inspirated and rewrote this api in PHP.
His wrapper however didn't work anymore, so I, Rick Bakker (@RickBakkr) fixed the file.

Installation
============
1. Download the file
2. Put it in the same folder as the script you would like to use it in
3. ``include "Somtoday.php"``
4. Make a neat gun for the people who are still alive!

Examples
===========
```PHP
include 'Somtoday.php';

$som = SOMtodayUser("henk","mypassword","myschool","dembrin")

$som->changeHomeworkStatus("6374673","7364736", True)#mark homework done
```

Footnote
=========
questions? rickbakkr@gmail.com
Only send proper mails. Inappropriate e-mails will be deleted immediately.
