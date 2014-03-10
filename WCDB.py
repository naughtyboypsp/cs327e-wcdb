# ---------------------------------------------------------------------------
# projects/WCDB(phase1)/WCDB.py
# Author: Xiaoqin LI
# Description:
  #Create an import/export facility from the XML into Element Tree and back.
  #The input is guaranteed to have validated XML.
  #The import facility must import from a file.
  #The export facility must export to a file.
  #Import/export the XML on only the ten crises, ten organizations,
  #and ten people of the group.
# Date: 03/09/2014
# ----------------------------------------------------------------------------

# -------
# imports
# -------

import sys
import xml.etree.ElementTree as ET

# ----------
# wcdb_read
# ----------

def wcdb_read (r) :
    """
    reads an input from a file which have a single top tag
    creates an element tree from string
    """
    
    imported_str_data = r.read()
    assert(type(imported_str_data) is str)
    data_tree = ET.fromstring(imported_str_data)
    assert(type(data_tree) is ET.Element)
    return data_tree

# ----------
# wcdb_write
# ----------

def wcdb_write (w, data_tree):
    """
    converts an element string to a string data
    exports the string data 
    """
    data_exported_string = ET.tostring(data_tree,encoding = "unicode", method = "xml")
    w.write(data_exported_string)

# ----------
# wcdb_solve
# ----------

def wcdb_solve (stdin, stdout) :
    """
    stdin is a reader
    stdout is a writer
    """
    imported_tree = wcdb_read (stdin)
    wcdb_write (stdout, imported_tree)
