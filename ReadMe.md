# What is this project?
ArchivesSpace BulkEdit UI is intended to assist academic librarians and archivists with their work. More specifically, for those using [ArchivesSpace](https://archivesspace.org/), an archives management tool, in performing major data management operations that the program itself does not support. ArchivesSpace is open-source, and can be [found on github here](https://github.com/archivesspace/archivesspace). This program came about from the need to perform several operations of this nature as part of a migration project for the University of Rochester, for which I was a major technical resource. I adapted the code I used to perform these operations into this tool so that we could have reusable tooling should the need arise in the future.
# Who is this project by?
This project was coded in whole by Channing Norton, in collaboration with the University of Rochester, River Campus Libraries. Any future pull requests will, of course, be appropriately credited.
# Who is this project for?
This project is intended for use by archivists, librarians, and digital content managers in the academic space. This project is only really useful if you are running ArchivesSpace
# Project Status
This project is still in the early development phases. It is not yet ready for use or outside contribution. Please check back in early January 2024.
# Running the Project - For End Users

# Running and Debugging the project - For Programmers
The code entry point is in main.py. You MUST be using CPython, not any other implementation. At the moment, the only _supported_ editor is [JetBrains PyCharm](https://www.jetbrains.com/pycharm/), but it should be trivial to get the project working in your editor of choice.
# Technologies Used
[ArchivesSpace Rest API](https://archivesspace.github.io/archivesspace/api/#introduction), [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake), [Keyring](https://pypi.org/project/keyring/),[Python 3.12](https://www.python.org/), [TKinter](https://docs.python.org/3/library/tkinter.html#module-tkinter)
# Feature Requests and Support
At the moment, create an issue on GitHub. I may eventually tie this to a jira queue, but that's a while off still.
# Contributing

# License
The code in this project is distributed under the [Mozilla Public License](https://www.mozilla.org/en-US/MPL/2.0/).