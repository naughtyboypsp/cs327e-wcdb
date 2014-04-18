all:

clean:
	rm -f *.pyc
	rm -f RunWCDB.out
	rm -f RunWCDB.tmp
	rm -f TestWCDB.out
	rm -f WCDB.html

diff: RunWCDB.in RunWCDB.py WCDB.py
	RunWCDB.py < RunWCDB.in > RunWCDB.tmp
	diff RunWCDB.out RunWCDB.tmp
	rm RunWCDB.tmp

WCDB.html: WCDB.py
	pydoc -w WCDB

RunWCDB.out: RunWCDB.in RunWCDB.py WCDB.py
	RunWCDB.py < RunWCDB.in > RunWCDB.out

TestWCDB.out: TestWCDB.py WCDB.py
	TestWCDB.py >& TestWCDB.out
