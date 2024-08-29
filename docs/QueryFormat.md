# Purpose

The goal of a query is to establish what the user is asking of the application

Queries can be nested in a tree form, with boolean logic applied

We need to save the queries to files. This means we need a string representation of a Query

# The .ACMQ filetype

Every atom (Clause) will be enclosed in parens if it is an API query

Every Boolean Operator will be prefixed with $

Boolean clauses will be enclosed in curly braces {}

Every queryType (begins with/ endswith .etc) will be enclosed with []

Every fieldtype will be prefixed with %

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

```

```

###
