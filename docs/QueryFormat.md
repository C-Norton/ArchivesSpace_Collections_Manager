# Purpose

The goal of a query is to establish what the user is asking of the application

Queries can be nested in a tree form, with boolean logic applied

We need to save the queries to files. This means we need a string representation of a Query

# The .ACMQ filetype

Every atom (Clause) will be enclosed in parens if it is an API query

Every Boolean Operator will be prefixed with $

Every QueryType will be prefixed with &

Boolean clauses will be enclosed in curly braces {}

Every queryType (begins with/ endswith .etc) will be enclosed with []

Every ResourceField will be prefixed with %

Every recordtype will be prefixed with #

Regular Expressions will be enclosed in graves ``

All user text inputs will be enclosed in double quotes ""

A naked IF will signal the start of the file

A naked THEN will signal the action to be taken

Acceptable actions are disclosed via BARE WORDS

DELETE_RECORD

DUPLICATE_RECORD

DELETE_NOTE (of type)

CREATE_NOTE (of type) 

REPLACE_NOTE (of type)

Replace and create note will both have an = sign after them specifying the note contents

Note flags: a flag is specified by - then the flagname, and equals sign, then the flag value


-type=

-part=single/multi

-subtype=

-publish=true/false

-content=""


All reserved characters (including backslash) can be escaped using backslash \


Examples:


Lev wishes to add a Statement on Offensive Materials to all finding aids save some exceptions
```
For all finding aids except those detailed below, add the following note:

Type = Scope and Contents
Label = Statement on Offensive Materials
Publish? = yes
Content = This collection may contain materials, items, or language which researchers may find offensive and objectionable. Researchers with questions or concerns should contact the department at rbscp@library.rochester.edu. 
Exceptions
A.A31 (already done)
A.M85
A.P23
A.P24
A.W22
A.W23
A.W25
A.W66
D.122
D.184
D.185
D.231
D.236
D.237
D.258
D.287
D.307
D.325
D.332
D.346
D.358
D.383
D.386
D.472
D.48
D.486
D.49
D.500
D.504
D.528
D.541
D.553
D.58
D.602
D.608
D.612
D.620
D.623
D.624
D.626
D.640
```
This would take the form
### QUERY
IF {{%identifier {$NOT &EQUALS "A.A31"}}$AND {%identifier {$NOT &EQUALS "A.M85" }}} THEN
