# -----------------------------------------------------------------------
# project 3/WCDB(phase1)/RunWCDB.py
# Author: Xiaoqin LI
# Description:
  #At least 10 acceptance tests (separated by one blank line)
  #with at least 500 lines total, in the files RunWCDB.in and RunWCDB.out
# Date: 03/09/2014
# -----------------------------------------------------------------------

"""
To run the program
    % python3/python RunWCDB.py < RunWCDB.in > RunWCDB.out

To document the program
    % pydoc -w WCDB
"""

# -------
# imports
# -------

import sys
import WCDB

#--------Main fuction--------------------
def main():
    WCDB.wcdb_solve(sys.stdin, sys.stdout)
#------------------------------=---------

main()
