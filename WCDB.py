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
	assert(type(data_tree) is ET.Element)
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
            crisisId text COLLATE utf8_unicode_ci NOT NULL,
            name text COLLATE utf8_unicode_ci NOT NULL,
            kind enum('Natural Disaster','War / Conflict','Act of Terrorism','Human Error Disaster','Assassination / Shooting') COLLATE utf8_unicode_ci NOT NULL,
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
            damageInUSD bigint(20) unsigned DEFAULT NULL,
            reparationCost bigint(20) unsigned DEFAULT NULL,
            regulatoryChanges varchar(250) COLLATE utf8_unicode_ci DEFAULT NULL,
            PRIMARY KEY (crisisId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
    # he defines crisisID as string in schema, now it becomes a bigint, I got lost, anyway, just following at this time being
    
    t = wcdb_query(
            login,
            """
            CREATE TABLE Orgs (
            orgsId bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            name text COLLATE utf8_unicode_ci NOT NULL,
            kind enum('Corporation','Government Agency','Military Force','Intergovernmental Agency','Intergovernmental Public Health Agency', 'Nonprofit / Humanitarian Organization') COLLATE utf8_unicode_ci NOT NULL,
            streetAddress text COLLATE utf8_unicode_ci DEFAULT NULL,
            city text COLLATE utf8_unicode_ci DEFAULT NULL,
            stateOrProvince text COLLATE utf8_unicode_ci DEFAULT NULL,
            postalCode text COLLATE utf8_unicode_ci DEFAULT NULL,
            country text COLLATE utf8_unicode_ci DEFAULT NULL,
            foundingMission text COLLATE utf8_unicode_ci DEFAULT NULL,
            datefounded datetime NOT NULL,
            majorEvents text COLLATE utf8_unicode_ci DEFAULT NULL,
            PRIMARY KEY (orgsId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE People (
            peopleId bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            name text COLLATE utf8_unicode_ci NOT NULL,
            kind enum('President','Celebrity','Actor/Actress','Musician','Politician', 'CEO','Humanitarian','Perpetrator','Regular Worker') COLLATE utf8_unicode_ci NOT NULL,
            streetAddress text COLLATE utf8_unicode_ci DEFAULT NULL,
            city text COLLATE utf8_unicode_ci DEFAULT NULL,
            stateOrProvince text COLLATE utf8_unicode_ci DEFAULT NULL,
            postalCode text COLLATE utf8_unicode_ci DEFAULT NULL,
            country text COLLATE utf8_unicode_ci DEFAULT NULL,
            

            PRIMARY KEY (peopleId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE Resources (
            resourceId bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            resource text COLLATE utf8_unicode_ci NOT NULL,
            PRIMARY KEY (resourceId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)

    t = wcdb_query(
            login,
            """
            CREATE TABLE CrisisResources (
            crisisId bigint(20) unsigned NOT NULL,
            resourceId bigint(20) unsigned NOT NULL,
            PRIMARY KEY (crisisId,resourceID)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)

    t = wcdb_query(
            login,
            """
            CREATE TABLE WaysToHelp (
            helpId bigint(20) unsigned NOT NULL,
            wayToHelp text COLLATE utf8_unicode_ci NOT NULL,
            PRIMARY KEY (helpId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)

    t = wcdb_query(
            login,
            """
            CREATE TABLE CrisisWaysToHelp (
            crisisId bigint(20) unsigned NOT NULL,
            helpId bigint(20) unsigned NOT NULL,
            PRIMARY KEY (crisisId, helpId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
    
    t = wcdb_query(
            login,
            """
            CREATE TABLE ContactInfos (
            contactInfoId bigint(20) unsigned NOT NULL,
            phoneNumber text COLLATE utf8_unicode_ci DEFAULT NULL,
            emailAddress text COLLATE utf8_unicode_ci DEFAULT NULL,
            facebookUrlId bigint(20) unsigned DEFAULT NULL,
            twitterUrlId bigint(20) unsigned DEFAULT NULL,
            websiteUrlId  bigint(20) unsigned DEFAULT NULL,
            PRIMARY KEY (contactInfoId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE orgContactInfos (
            orgsId bigint(20) unsigned NOT NULL,
            contactInfoId bigint(20) unsigned NOT NULL,
            PRIMARY KEY (orgsId, ContactInfoId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE Citations (
            citationId bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            citation text COLLATE utf8_unicode_ci NOT NULL,
            PRIMARY KEY (citationId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE CrisisCitations (
            citationId bigint(20) unsigned NOT NULL,
            crisisId bigint(20) unsigned NOT NULL,
            PRIMARY KEY (citationId, crisisId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)

    t = wcdb_query(
            login,
            """
            CREATE TABLE OrgCitations (
            orgId bigint(20) unsigned NOT NULL,
            citationId bigint(20) unsigned NOT NULL,
            PRIMARY KEY (orgId, citationId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
    
    t = wcdb_query(
            login,
            """
            CREATE TABLE PersonCitations (
            personId bigint(20) unsigned NOT NULL,
            citationId bigint(20) unsigned NOT NULL,
            PRIMARY KEY (personId, citationId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE Urls (
            urlId bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            type text COLLATE utf8_unicode_ci NOT NULL,
            urlAddress text COLLATE utf8_unicode_ci NOT NULL,
            PRIMARY KEY (urlId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE CrisisUrls (
            crisisId bigint(20) unsigned NOT NULL,
            urlId bigint(20) unsigned NOT NULL,
            PRIMARY KEY (crisisId, urlId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE OrgUrls (
            orgId bigint(20) unsigned NOT NULL,
            urlId bigint(20) unsigned NOT NULL,
            PRIMARY KEY (orgId, urlId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE PersonUrls (
            personId bigint(20) unsigned NOT NULL,
            urlId bigint(20) unsigned NOT NULL,
            PRIMARY KEY (personId, urlId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE CrisisOrgs (
            crisisId bigint(20) unsigned NOT NULL,
            orgId bigint(20) unsigned NOT NULL,
            PRIMARY KEY (crisisId, orgId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)

    t = wcdb_query(
            login,
            """
            CREATE TABLE CrisisPeople (
            crisisId bigint(20) unsigned NOT NULL,
            personId bigint(20) unsigned NOT NULL,
            PRIMARY KEY (crisisId, personId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE OrgPeople (
            orgId bigint(20) unsigned NOT NULL,
            personId bigint(20) unsigned NOT NULL,
            PRIMARY KEY (orgId, personId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)

# ----------
# data import
# ----------
def wcdb_import(login, tree):
    """
    Iterating through crisis tags in crises tag and import into DB: table Crises 
    """
    # based on the discussion with Robert in class, we think it is better to put all input stuff in one function.
    #-----------------import crises table-------------------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./crises/crisis")
    #Iterates over Children of crises
    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1       
    #QueryInserting Loop
    for i in range(0,counter):
        #Queryinseting - Crisis Table
        dict_entry = inserts_list[i]       
##        # stupid dict is not ordered, otherwise we won't write such a long line!
##        for entry in dict_entry:
##        !!!!!comment: (1)int value can't be 'null' in xml, just leave it as empty. (2)If you have a huge number more than 10 digits, you need to modify type from
##        int to bigint 20. (3) I= if define ID as bigint(20), it has to been digits only, CRI001 is not digit only!!!!
        s = (dict_entry.get('crisisId'),dict_entry.get('name'),dict_entry.get('kind'),dict_entry.get('streetAddress','Null'),dict_entry.get('city','Null'),\
             dict_entry.get('stateOrProvince','Null'),dict_entry.get('postalCode','Null'),dict_entry.get('country','Null'),dict_entry.get('dateAndTime','Null'),\
             dict_entry.get('fatalities','Null'),dict_entry.get('injuries','Null'),dict_entry.get('populationIll','Null'),\
             dict_entry.get('populationDisplaced','Null'),dict_entry.get('environmentalImpact','Null'),dict_entry.get('politicalChanges','Null'),\
             dict_entry.get('culturalChanges','Null'),dict_entry.get('jobsLost','Null'),dict_entry.get('damageInUSD','Null'),\
             dict_entry.get('reparationCost','Null'),dict_entry.get('regulatoryChanges','Null'))
    #-------------this "s" is too long, right? you guys can help me think about other data structure other than dictionary> Dictionary is not ordered but we need to
        # insert each element in order so we can't iterate a dictionary, if you guys have better idea let me know.
        s = 'insert into Crises Values' + str(s) + ';'
        s =s.replace('None', 'Null')
        print('aa')
        t = wcdb_query(login,s)
##            

            
    

    return
    
def wcdb_solve(r,w):
    """
    r is a reader
    w is a writer
    login: Logs into DB, tree: Generates Element Tree,
    createDB(login): Creates Tables in DB,
    """
    
    login_var = wcdb_login(*a)
    tree = wcdb_read (r)
    createDB(login_var)
    wcdb_import(login_var, tree)

def main():
    r = open('compiled.xml', 'r')
    w = open('RunWCDB.out.xml', 'w')
    wcdb_solve(r,w)

        
main()
