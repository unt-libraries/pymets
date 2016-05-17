from lxml.etree import Element, SubElement, tostring
from pymets import XLINK, XSI, NSMAP


class MetsStructureException(Exception):
    """Base exception for the METS Python structure."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "%s" % (self.value,)


def create_mets_xml_subelement(parent, element):
    """Create METS sub elements."""
    sub_element = SubElement(parent, element.tag)
    for attribute, value in element.atts.items():
        if not value:
            continue
        if not isinstance(value, str) and not isinstance(value, unicode):
            sub_element.set(attribute, str(value))
        else:
            sub_element.set(attribute, value)
    if element.content:
        sub_element.text = element.content
    for child in element.children:
        if element.tag == "xmlData":
            sub_element.append(child)
        else:
            create_mets_xml_subelement(sub_element, child)


class MetsBase(object):
    """Base object from which all METS element wrappers will inherit."""

    def __init__(self, **kwargs):
        # Set up the dispatcher to peform operations on keyword arguments.
        initial_dispatch = {
            'attributes': self.set_atts,
            'content': self.set_content,
            }

        # Set the element's tag to None if it isn't defined.
        self.tag = getattr(self, 'tag', None)

        # List of allowed child elements.
        self.contained_children = getattr(self, 'contained_children', [])

        # By default, objects don't have textual content.
        self.allows_content = getattr(self, 'allows_content', False)

        # Attributes of this particular element.
        self.atts = getattr(self, 'atts', {})

        # Textual content, if any.
        self.content = None

        # Child element wrappers go here
        self.children = []

        # Loop through the keyword arguments and set initial values using the initial dispatcher.
        if kwargs:
            for key, val in kwargs.items():
                if key in initial_dispatch:
                    # Call the dispatcher to peform actions based on the keyword arguments.
                    initial_dispatch[key](val)
                else:
                    raise MetsStructureException(
                        "Argument %s not valid" % (key))

    def set_atts(self, attribute_dict):
        """Set the attributes."""
        for name, value in attribute_dict.items():
            if name in self.atts.keys():
                self.atts[name] = value
            else:
                raise MetsStructureException(
                    "Attribute %s is not legal in this element!" % (name,))
        # Remove empty attributes.
        for key, value in self.atts.items():
            if value is None:
                del self.atts[key]

    def set_att(self, attName, attVal):
        """Set a single attribute."""
        # We need a way to check for validity here.
        self.atts[attName] = attVal

    def get_att(self, attName):
        """Get a single attribute, or None if it does not exist."""
        if attName in self.atts:
            return self.atts[attName]

        return None

    def add_child(self, child):
        """Add a child object to the current one.  It will check the
        contained_children list to make sure that the object is allowable, and
        throw an exception if not.
        """
        if child.tag in self.contained_children:
            self.children.append(child)
        else:
            raise MetsStructureException(
                "Invalid child type %s for parent %s." % (child.tag, self.tag)
            )

    def remove_child(self, child):
        """Remove a given child element from the children list."""
        newChildren = []
        for originalChild in self.children:
            if originalChild != child:
                newChildren.append(originalChild)

        self.children = newChildren

    def get_children(self, tag):
        """Given a tag name, return a list of child objects that
        match the tag.
        """
        childList = []
        for child in self.children:
            if child.tag == tag:
                childList.append(child)
        return childList

    def set_content(self, content):
        """Set textual content for the object/node.  It checks to make
        sure that the node is allowed to contain content and throws an
        exception if not.
        """
        if self.allows_content:
            self.content = content
        else:
            raise MetsStructureException(
                "Element %s does not allow textual content." % self.tag
            )


class Mets(MetsBase):
    """Wrapper for top level METS element."""
    tag = "mets"
    contained_children = ["metsHdr", "dmdSec", "amdSec", "fileSec", "structMap", "behaviorSec"]

    def __init__(self, **kwargs):
        self.atts = {"TYPE": None, "OBJID": None, "LABEL": None, XSI+"schemaLocation": None}
        super(Mets, self).__init__(**kwargs)

    def create_xml_file(self, mets_filename, nsmap=None):
        """Take a filename and a METS Python object, and create a METS file."""
        try:
            f = open(mets_filename, 'w')
            f.write(self.create_xml_string(nsmap).encode("utf-8"))
            f.close()
        except Exception, e:
            raise MetsStructureException(
                "Failed to create METS file. Filename: %s, %s" %
                (mets_filename, str(e))
            )

    def create_xml_string(self, nsmap=None):
        """Convert a METS elements list (list of MetsBase objects).

        Returns a METS XML document in a string which you can output into a
        file:
            mets_string = mets2xml(mets_root_element)
        """
        if not nsmap:
            nsmap = NSMAP
        root = Element(self.tag, nsmap=nsmap)
        for attribute, value in self.atts.items():
            root.set(attribute, str(value))
        # Create an XML structure from field list.
        for element in self.children:
            create_mets_xml_subelement(root, element)

        xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(root, pretty_print=True)

        return xml


class MetsHdr(MetsBase):
    """Wrapper for metsHdr element."""
    tag = "metsHdr"
    contained_children = ["agent",  "altRecordID"]

    def __init__(self, **kwargs):
        self.atts = {
            "RECORDSTATUS": None, "CREATEDATE": None,
            "LASTMODDATE": None, "ID": None}
        super(MetsHdr, self).__init__(**kwargs)


class Agent(MetsBase):
    tag = "agent"
    contained_children = ["name", "note"]

    def __init__(self, **kwargs):
        self.atts = {"ROLE": None,  "TYPE": None}
        super(Agent, self).__init__(**kwargs)


class Name(MetsBase):
    tag = "name"
    allows_content = True

    def __init__(self, **kwargs):
        super(Name, self).__init__(**kwargs)


class Note(MetsBase):
    tag = "note"
    allows_content = True

    def __init__(self, **kwargs):
        super(Note, self).__init__(**kwargs)


class AltRecordID(MetsBase):
    tag = "altRecordID"
    allows_content = True

    def __init__(self, **kwargs):
        self.atts = {"TYPE": None}
        super(AltRecordID, self).__init__(**kwargs)


class DmdSec(MetsBase):
    tag = "dmdSec"
    contained_children = ["mdRef", "mdWrap"]

    def __init__(self, **kwargs):
        self.atts = {"ID": None}
        super(DmdSec, self).__init__(**kwargs)


class MdRef(MetsBase):
    tag = "mdRef"
    allows_content = True

    def __init__(self, **kwargs):
        self.atts = {"LOCTYPE": None, "MDTYPE": None, "OTHERMDTYPE": None, XLINK+"href": None}
        super(MdRef, self).__init__(**kwargs)


class AmdSec(MetsBase):
    tag = "amdSec"
    contained_children = ["techMD", "rightsMD", "sourceMD", "digiprovMD"]

    def __init__(self, **kwargs):
        super(AmdSec, self).__init__(**kwargs)


class TechMD(MetsBase):
    tag = "techMD"
    contained_children = ["mdWrap", "mdRef"]

    def __init__(self, **kwargs):
        self.atts = {"ID": None}
        super(TechMD, self).__init__(**kwargs)


class RightsMD(MetsBase):
    tag = "rightsMD"
    contained_children = ["mdWrap", "mdRef"]

    def __init__(self, **kwargs):
        self.atts = {"ID": None}
        super(RightsMD, self).__init__(**kwargs)


class SourceMD(MetsBase):
    tag = "sourceMD"
    contained_children = ["mdWrap", "mdRef"]

    def __init__(self, **kwargs):
        self.atts = {"ID": None}
        super(SourceMD, self).__init__(**kwargs)


class DigiprovMD(MetsBase):
    tag = "digiprovMD"
    contained_children = ["mdWrap", "mdRef"]

    def __init__(self, **kwargs):
        self.atts = {"ID": None}
        super(DigiprovMD, self).__init__(**kwargs)


class MdWrap(MetsBase):
    tag = "mdWrap"
    contained_children = ["xmlData"]

    def __init__(self, **kwargs):
        self.atts = {"MDTYPE": None}
        super(MdWrap, self).__init__(**kwargs)


class XMLData(MetsBase):
    tag = "xmlData"
    allows_content = True

    def __init__(self, **kwargs):
        super(XMLData, self).__init__(**kwargs)

    def add_child(self, child):
        """Since this element is supposed to accommodate an arbitrary
        set of data, the add_child function is significantly less picky
        than the parent version.
        """
        self.children.append(child)


class FileSec(MetsBase):
    tag = "fileSec"
    contained_children = ["fileGrp"]

    def __init__(self, **kwargs):
        self.atts = {"ID": None}
        super(FileSec, self).__init__(**kwargs)


class FileGrp(MetsBase):
    tag = "fileGrp"
    contained_children = ["file", "fileGrp"]

    def __init__(self, **kwargs):
        self.atts = {"ID": None}
        super(FileGrp, self).__init__(**kwargs)


class File(MetsBase):
    tag = "file"
    contained_children = ["FLocat"]

    def __init__(self, **kwargs):
        self.atts = {
            "ID": None, "MIMETYPE": None,  "USE": None, "CREATED": None,
            "CHECKSUM": None, "CHECKSUMTYPE": None, "SIZE": None,
            "ADMID": None, "OWNERID": None}
        super(File, self).__init__(**kwargs)


class FLocat(MetsBase):
    tag = "FLocat"
    allows_content = True

    def __init__(self, **kwargs):
        self.atts = {"LOCTYPE": None,  XLINK+"href": None}
        super(FLocat, self).__init__(**kwargs)


class StructMap(MetsBase):
    tag = "structMap"
    contained_children = ["div"]

    def __init__(self, **kwargs):
        self.atts = {"ID": None}
        super(StructMap, self).__init__(**kwargs)


class Div(MetsBase):
    tag = "div"
    contained_children = ["mptr",  "fptr", "div"]

    def __init__(self, **kwargs):
        self.atts = {
            "DMDID": None, "TYPE": None, "ID": None, "ORDER": None,
            "ORDERLABEL": None, "LABEL": None, "ADMID": None,
            "CONTENTIDS": None}
        super(Div, self).__init__(**kwargs)


class Fptr(MetsBase):
    tag = "fptr"
    allows_content = True

    def __init__(self, **kwargs):
        self.atts = {"FILEID": None}
        super(Fptr, self).__init__(**kwargs)


class Par(MetsBase):
    tag = "par"
    contained_children = ["area", "seq"]

    def __init__(self, **kwargs):
        self.atts = {"ID": None}
        super(Par, self).__init__(**kwargs)


class Area(MetsBase):
    tag = "area"
    allows_content = True

    def __init__(self, **kwargs):
        self.atts = {
            "ID": None, "FILEID": None, "SHAPE": None, "COORDS": None,
            "BEGIN": None, "END": None, "BETYPE": None, "EXTENT": None,
            "EXTYPE": None, "ADMID": None, "CONTENT": None, "IDS": None}
        super(Area, self).__init__(**kwargs)


class StructLink(MetsBase):
    tag = "structLink"
    contained_children = ["smLink"]

    def __init__(self, **kwargs):
        self.atts = {"ID": None}
        super(StructLink, self).__init__(**kwargs)


class SmLink(MetsBase):
    tag = "smLink"
    allows_content = True

    def __init__(self, **kwargs):
        self.atts = {
            "ID": None, XLINK+"arcrole": None, XLINK+"title": None,
            XLINK+"actuate": None, XLINK+"to": None, XLINK+"from": None}
        super(SmLink, self).__init__(**kwargs)


class BehaviorSec(MetsBase):
    tag = "behaviorSec"
    contained_children = ["behaviorSec", "behavior"]

    def __init__(self, **kwargs):
        self.atts = {"ID": None, "CREATED": None, "LABEL": None}
        super(BehaviorSec, self).__init__(**kwargs)


class Behavior(MetsBase):
    tag = "behavior"
    contained_children = ["interfaceDef", "mechanism"]

    def __init__(self, **kwargs):
        self.atts = {"ID": None, "STRUCTID": None, "BTYPE": None,
                     "CREATED": None, "LABEL": None, "GROUPID": None,
                     "ADMID": None}
        super(Behavior, self).__init__(**kwargs)


class InterfaceDef(MetsBase):
    tag = "interfaceDef"
    allows_content = True

    def __init__(self, **kwargs):
        self.atts = {"ID": None, "LABEL": None, "LOCTYPE": None, "OTHERLOCTYPE": None}
        super(InterfaceDef, self).__init__(**kwargs)


class Mechanism(MetsBase):
    tag = "mechanism"
    allows_content = True

    def __init__(self, **kwargs):
        self.atts = {"ID": None, "LABEL": None, "LOCTYPE": None, "OTHERLOCTYPE": None}
        super(Mechanism, self).__init__(**kwargs)
