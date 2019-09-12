from lxml.etree import iterparse
from pymets import mets_structure


class PymetsException(Exception):
    """Base exception for pymets."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "%s" % (self.value,)


"""
    How to use pymets:
    Create a METS object (attributes are required to match what's in each elements self.atts)
    from pymets.metsdoc import PYMETS_DISPATCH
    mets_root_element = PYMETS_DISPATCH['mets'](attributes=attributes)
    mets_fileSec_element = PYMETS_DISPATCH['fileSec'](attributes=attributes, content=content)
    mets_root_element.add_child(mets_fileSec_element)
"""
PYMETS_DISPATCH = {
    'mets': mets_structure.Mets,
    'metsHdr': mets_structure.MetsHdr,
    'agent': mets_structure.Agent,
    'name': mets_structure.Name,
    'note': mets_structure.Note,
    'altRecordID': mets_structure.AltRecordID,
    'dmdSec': mets_structure.DmdSec,
    'mdRef': mets_structure.MdRef,
    'amdSec': mets_structure.AmdSec,
    'techMD': mets_structure.TechMD,
    'rightsMD': mets_structure.RightsMD,
    'sourceMD': mets_structure.SourceMD,
    'digiprovMD': mets_structure.DigiprovMD,
    'mdWrap': mets_structure.MdWrap,
    'xmlData': mets_structure.XMLData,
    'fileSec': mets_structure.FileSec,
    'fileGrp': mets_structure.FileGrp,
    'file': mets_structure.File,
    'FLocat': mets_structure.FLocat,
    'structMap': mets_structure.StructMap,
    'div': mets_structure.Div,
    'fptr': mets_structure.Fptr,
    'par': mets_structure.Par,
    'area': mets_structure.Area,
    'structLink': mets_structure.StructLink,
    'smLink': mets_structure.SmLink,
    'behaviorSec': mets_structure.BehaviorSec,
    'behavior': mets_structure.Behavior,
    'interfaceDef': mets_structure.InterfaceDef,
    'mechanism': mets_structure.Mechanism,
    }


def metsxml2py(mets_filename, loose=False):
    """Take a METS XML filename and parse it into a Python object.

    You can also pass this a string as input like so:
       import io
       metsxml2py(io.BytesIO(mets_string.encode('utf-8'))
    """
    # Create a stack to hold parents.
    parent_stack = []
    # Use the memory efficient iterparse to open the file and loop through elements.
    for event, element in iterparse(mets_filename, events=("start", "end")):
        # If the element exists in mets
        if element.tag in PYMETS_DISPATCH:
            # If it is the opening tag of the element
            if event == 'start':
                if element.text is not None:
                    content = element.text.strip()
                else:
                    content = ''
                # If the element has attributes and content.
                if len(element.attrib) > 0 and content != '':
                    # Add the element to the parent stack.
                    parent_stack.append(
                        PYMETS_DISPATCH[element.tag](
                            attributes=element.attrib,
                            content=element.text,
                            )
                        )
                # If the element has attributes.
                elif len(element.attrib) > 0:
                    # Add the element to the parent stack.
                    parent_stack.append(
                        PYMETS_DISPATCH[element.tag](attributes=element.attrib)
                        )
                # If the element has content.
                elif content != '':
                    # Add the element to the parent stack.
                    parent_stack.append(
                        PYMETS_DISPATCH[element.tag](content=element.text)
                        )
                # If the element has no content or attributes.
                else:
                    # Add the element to the parent stack.
                    parent_stack.append(PYMETS_DISPATCH[element.tag]())
            # If it is the closing tag of the element.
            elif event == 'end':
                # Take the element off the parent stack and append it to its own parent.
                child = parent_stack.pop()
                if len(parent_stack) > 0:
                    parent_stack[-1].add_child(child)
                # If it doesn't have a parent, it must be the root element.
                else:
                    # Return the root element.
                    return child
        else:
            if loose:
                continue
            else:
                raise PymetsException("Element \"%s\" not found in mets dispatch." % (element.tag))
