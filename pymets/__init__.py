# Define all the METS namespaces in a dictionary.
NSMAP = {
    'mets': 'http://www.loc.gov/METS/',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xlink': 'http://www.w3.org/1999/xlink',
    }

# Create the prependable xsi namespace.
XSI = "{%s}" % NSMAP['xsi']

# Create the prependable xlink namespace.
XLINK = "{%s}" % NSMAP['xlink']
