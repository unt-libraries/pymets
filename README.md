pymets [![Build Status](https://travis-ci.org/unt-libraries/pymets.svg?branch=master)](https://travis-ci.org/unt-libraries/pymets)
=========

Python module for reading and writing METS files.

```python
>>> from pymets.metsdoc import PYMETS_DISPATCH
>>> attributes = {
            'TYPE': 'archival information package',
            'OBJID': 'ark:/67531/TEST'}
>>> mets_root_element = PYMETS_DISPATCH['mets'](attributes=attributes)
>>> mets_fileSec_element = PYMETS_DISPATCH['fileSec']
>>> mets_root_element.add_child(mets_fileSec_element)
>>> print(mets_root_element.atts)
{'TYPE': 'archival information package', 'OBJID': 'ark:/67531/TEST'}
```

Requirements
-------------
* python ~=3.7

Installation
-------------
This application can be installed by following the steps below:
```
$ git clone https://github.com/unt-libraries/pymets.git

$ cd pymets

$ python setup.py install
```

Testing
--------

Install tox on your system:

    $ pip install tox

To run the development tests, use the following command:

    $ tox


License
-------

See LICENSE.txt


Acknowledgements
----------------

_pymets_ was developed at the UNT Libraries and has been worked on by a number of developers over the years including:

Brandon Fredericks  

[Kurt Nordstrom](https://github.com/kurtnordstrom)  

[Lauren Ko](https://github.com/ldko)  

[Mark Phillips](https://github.com/vphill)  

If you have questions about the project feel free to contact Mark Phillips at mark.phillips@unt.edu.
