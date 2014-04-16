# -----------------------------------------------------------------------
# project 3/WCDB(phase2)/RunWCDB.py
# Author: Xiaoqin LI
# Description:
  #At least 10 acceptance tests (separated by one blank line)
  #with at least 500 lines total, in the files RunWCDB.in and RunWCDB.out
# Date: 04/03/2014
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
    #---------- a list to save the filenames----------
<<<<<<< HEAD
    xml_filename_list = ['GottaGitThat-WCDB.xml'] \
                        # 'UtNonObliviscar-WCDB.xml']#, \
                         #'SeekWolves-WCDB.xml', \
=======
    xml_filename_list = ['GottaGitThat-WCDB.xml',\
                         'SeekWolves-WCDB.xml', \
                         'UtNonObliviscar-WCDB.xml']#, \
>>>>>>> c7688e72567cf5a3f441e4b0fc271c35c3520a6b
                        # 'BashKetchum-WCDB.xml', \
                        # 'Brigadeiros-WCDB.xml', \                         
                        # 'EJADK-WCDB.xml', \
##                         'TeamRocket-WCDB.xml', \  # their data does not have kind tag
                       #  'Databosses-WCDB.xml']
    WCDB.wcdb_solve(sys.stdin, sys.stdout,xml_filename_list)
    #----------------------------------------

main()

