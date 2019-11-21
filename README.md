pymets [![Build Status](https://travis-ci.org/unt-libraries/pymets.svg?branch=master)](https://travis-ci.org/unt-libraries/pymets)
=========

Python module for reading and writing METS files.

```python
>>> import io
>>> from pymets import mets_structure, metsdoc
>>> # To create a METS object
>>> attributes = {
    'TYPE': 'archival information package',
    'OBJID': 'ark:/67531/12345',
    }
>>> m = mets_structure.Mets(attributes=attributes)
>>> m.add_child(mets_structure.MetsHdr())
>>> print(m.create_xml_string())
b'<?xml version="1.0" encoding="UTF-8"?>
<mets xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:mets="http://www.loc.gov/METS/" 
xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
TYPE="archival information package" OBJID="ark:/67531/12345">
  <metsHdr/>
</mets>'

>>> # To convert METS XML to Python object 
>>> mets_string = """<?xml version="1.0" encoding="UTF-8"?> 
<mets><metsHdr CREATEDATE="2012-07-17T22:24:35Z" LASTMODDATE="2012-07-17T22:24:35Z" ID="hdr_00001">
    <agent TYPE="ORGANIZATION" ROLE="CREATOR">
        <name>UNT Libraries: Digital Projects Unit</name>
    </agent>
  </metsHdr>
</mets>"""
>>> res = metsdoc.metsxml2py(io.BytesIO(mets_string.encode('utf-8')))
```

Requirements
-------------
* Python 3.6 - 3.7

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

[Madhulika Bayyavarapu](https://github.com/madhulika95b)

If you have questions about the project feel free to contact Mark Phillips at mark.phillips@unt.edu.
