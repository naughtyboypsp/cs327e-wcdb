#!/usr/bin/env python

# ---------------------------
# projects/WCDB(phase2)/WCDB2.py
# Author Xiaoqin LI
# last updated date: 03/30/2014

# -------
# imports
# -------

import sys
import _mysql
#import lxml.etree as ET  # a few posts online said it works better, but I have not installed this module so far.
import xml.etree.ElementTree as ET

# --------
# DB Login
# --------

   #[host, un, pw, database]
##a = ["z","lxq0906","XXXXXXXXX","cs327e_lxq0906"] # my account on CS computer

a = ["localhost","root","121314","cs327e-wcdb"]

def wcdb_login ( host, un, pw, database ) :
    """takes credentials and logs into DB"""
        login = _mysql.connect(
			host = host,
			user = un,
			passwd = pw,
			db = database)
	assert (str(type(login)) == "<type '_mysql.connection'>")
	return login

# --------
# DB query
# --------

def wcdb_query (login, s):
    """Logs into DB and runs provided string as query"""
        assert (str(type(login)) == "<type '_mysql.connection'>")
	assert (type(s) is str)
	login.query(s)
	r = login.use_result()
	if r is None :
		return None
	assert (str(type(r)) == "<type '_mysql.result'>")
	t = r.fetch_row(maxrows = 0)
	assert (type(t) is tuple)
	return t

# ----------
# wcdb_read
# ---------- 

def wcdb_read (r):
	"""
	reads an input
	creates an element tree from string
	"""
	imported_str_data = r.read()
	assert(type(imported_str_data) is str)
	data_tree = ET.fromstring(imported_str_data)
	return data_tree

# ----------
# create DB
# ----------

def createDB(login):
        """Create Needed Databases, dropping if needed"""
        t = wcdb_query(login, "drop table if exists Student;")
        assert(t is None)
        
        wcdb_query(login, "drop table if exists crises;")
	wcdb_query(login, "drop table if exists orgs;")
	wcdb_query(login, "drop table if exists people")
	wcdb_query(login, "drop table if exists resources;")
	wcdb_query(login, "drop table if exists crisisResources;")
	wcdb_query(login, "drop table if exists waysToHelp;")
	wcdb_query(login, "drop table if exists crisisWaysToHelp;")
	wcdb_query(login, "drop table if exists contactInfos;")
	wcdb_query(login, "drop table if exists orgContactInfos;")
	wcdb_query(login, "drop table if exists citations;")
	wcdb_query(login, "drop table if exists crisisCitations;")
	wcdb_query(login, "drop table if exists orgCitations;")
	wcdb_query(login, "drop table if exists personCitations;")
	wcdb_query(login, "drop table if exists urls;")
	wcdb_query(login, "drop table if exists crisisUrls;")
	wcdb_query(login, "drop table if exists orgUrls;")
	wcdb_query(login, "drop table if exists personUrls;")
	wcdb_query(login, "drop table if exists crisisOrgs;")
	wcdb_query(login, "drop table if exists crisisPeople;")
	wcdb_query(login, "drop table if exists orgPeople;")

       
        ##-----------------------------##
        # so many tables.... so many join.... you guys can help out, for creating these tables,
        # here I write first two instances, you guys can add more based on my instance and Adrian's MYSQL schema
        ##-----------------------------##
        # for table crises
        # Adrian's SQL set it as enumerate...he set it in schema...what makes 'kind' so different...anyway...
        # I just follow this but not sure if it works
	t = wcdb_query(
                login,
		"""
                CREATE TABLE Crises (
                crisisId bigint(20) unsigned NOT NULL AUTO_INCREMENT,
                name text COLLATE utf8_unicode_ci NOT NULL,
                kind enum('Natural Disaster','War / Conflict','Act of Terrorism','Human Error Distaster','Assassination / Shooting') COLLATE utf8_unicode_ci NOT NULL,
                streetAddress text COLLATE utf8_unicode_ci DEFAULT NULL,
                city text COLLATE utf8_unicode_ci DEFAULT NULL,
                stateOrProvince text COLLATE utf8_unicode_ci DEFAULT NULL,
                postalCode text COLLATE utf8_unicode_ci DEFAULT NULL,
                country text COLLATE utf8_unicode_ci DEFAULT NULL,
                dateAndTime datetime NOT NULL,
                fatalities int unsigned DEFAULT NULL,
                injuries int unsigned DEFAULT NULL,
                populationIll int unsigned DEFAULT NULL,
                populationDisplaced int unsigned DEFAULT NULL,
                environmentalImpact varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL,
                politicalChanges text COLLATE utf8_unicode_ci DEFAULT NULL,
                culturalChanges text COLLATE utf8_unicode_ci DEFAULT NULL,
                jobsLost int unsigned DEFAULT NULL,
                damageInUsd int unsigned DEFAULT NULL,
                reparationCost int(11) unsigned DEFAULT NULL,
                regulatoryChanges varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL,
                PRIMARY KEY (crisisId)
                )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
                """)
        # he defines crisisID in schema, now it becomes a bigint, I got lost, anyway, just following at this time being
	t = wcdb_query(
                login,
		"""
                CREATE TABLE CrisisCitations (
                crisisId bigint(20) unsigned NOT NULL,
                citationId bigint(20) unsigned NOT NULL,
                PRIMARY KEY (crisisId,citationId)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
                """) 



def main():
        login_var = wcdb_login(*a) # we just learned this, so....

        
main()
