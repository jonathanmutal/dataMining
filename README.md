Data Mining 2017
================


Instalation
-----------

1. Soft needed:

    - Git
    - Pip
    - Python>=3.4
    - Virtualenv

       How to install?

        sudo apt-get install git python-pip python3 python3-tk virtualenv


2. Make and activate a new [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html). Strongly recommend [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation).

       You can install with a simple line:

        sudo pip install virtualenvwrapper

       After that you must add a new line at the end of the file ``.bashrc (~/.bashrc)``

        [[ -s "/usr/local/bin/virtualenvwrapper.sh" ]] && source "/usr/local/bin/virtualenvwrapper.sh"

       How to make and active our virtualenv?

        mkvirtualenv --system-site-packages --python=/usr/bin/python3 pln-2017

3. Download the code:

       How?

        git clone https://github.com/joni115/dataMining.git

       Install it

        cd dataMining
        pip install -r requirements.txt
