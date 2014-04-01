# ---------------------------------
# projects/WCDB(phase2)/TestWCDB.py
# Author: Xiaoqin LI
# Date: 04/01/2014
#----------------------------------

"""
To test the program:
python/python2 TestWCDB.py > TestWCDB.out
"""

# -------
# imports
# -------

import StringIO
import unittest
import sys
import _mysql
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
from WCDB import *

# ----------------------------------
# TestWCDB.py,  unit tests in total
# including some major corner tests 
# ----------------------------------

class TestWCDB(unittest.TestCase):
  # -----------------------------------
  # login fuction test 3 in total
  # first one shall be one of us 
  # -----------------------------------
  def test_wcdb_login1 (self):
    a = ("localhost","root","121314","cs327e-wcdb")
    login = wcdb_login(*a)
    self.assert_(str(type(login)) == "<type '_mysql.connection'>")

  def test_wcdb_login2 (self):
    a = ("localhost","root","121314","cs327e-wcdb")
    login = wcdb_login(*a)
    self.assert_(str(type(login)) != "<type '_mysql.connection'>")
        
  def test_wcdb_login3 (self):
    a = ("localhost","root","121314","cs327e-wcdb")
    login = wcdb_login(*a)
    self.assert_(str(type(login)) != "<type '_mysql.connection'>")

  def test_wcdb_login4 (self):
    a = ("localhost","root","121314","cs327e-wcdb")
    login = wcdb_login(*a)
    self.assert_(str(type(login)) != "<type '_mysql.connection'>")
  
  #-----------
  # test query
  #-----------

  
     
     
print("TestWCDB.py")
print("Done.")
unittest.main()


