#!/usr/bin/env python

# ---------------------------
# projects/WCDB(phase2)/WCDB2.py
# Author Xiaoqin LI
# last updated date: 04/01/2014

# -------
# imports
# -------

import sys
import _mysql
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
from _mysql_exceptions import OperationalError


# --------
# DB Login
# --------

def wcdb_login ( host, un, pw, database ) :
    """takes credentials and logs into DB"""
    try:
        login = _mysql.connect(
                            host = host,
                            user = un,
                            passwd = pw,
                            db = database)
    except OperationalError:
        login = None
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
# create DB
# ----------

def createDB(login):
    """
    Create Needed Databases,
    dropping if needed
    """
    t = wcdb_query(login, "drop table if exists Student;")
    assert(t is None)
    wcdb_query(login, "drop table if exists CrisisOrgs;")
    wcdb_query(login, "drop table if exists CrisisPeople;")
    wcdb_query(login, "drop table if exists OrgPeople;")
    wcdb_query(login, "drop table if exists CrisisCitations;")
    wcdb_query(login, "drop table if exists OrgCitations;")
    wcdb_query(login, "drop table if exists PersonCitations;")
    wcdb_query(login, "drop table if exists CrisisResources;")
    wcdb_query(login, "drop table if exists CrisisWaysToHelp;")
    wcdb_query(login, "drop table if exists OrgContactInfos;")  
    wcdb_query(login, "drop table if exists CrisisUrls;")
    wcdb_query(login, "drop table if exists OrgUrls;")
    wcdb_query(login, "drop table if exists PersonUrls;")
    
    wcdb_query(login, "drop table if exists Crises;")
    wcdb_query(login, "drop table if exists Orgs;")
    wcdb_query(login, "drop table if exists People")
    wcdb_query(login, "drop table if exists Resources;")    
    wcdb_query(login, "drop table if exists WaysToHelp;")   
    wcdb_query(login, "drop table if exists ContactInfos;")    
    wcdb_query(login, "drop table if exists Citations;")  
    wcdb_query(login, "drop table if exists Urls;")   
    
    ##--------------Create Needed Databases---------------##
    t = wcdb_query(
            login,
            """
            CREATE TABLE Crises (
            crisisId varchar(10) COLLATE utf8_unicode_ci NOT NULL,
            name varchar(100) COLLATE utf8_unicode_ci NOT NULL,
            kind enum('Natural Disaster','War / Conflict','Act of Terrorism','Human Error Disaster','Assassination / Shooting') COLLATE utf8_unicode_ci NOT NULL,
            streetAddress varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
            city varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
            stateOrProvince varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
            country varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
            dateAndTime datetime NOT NULL,
            fatalities bigint(12) unsigned NULL,
            injuries bigint(12) unsigned NULL,
            populationIll bigint(12) unsigned NULL,
            populationDisplaced bigint(12) unsigned NULL,
            environmentalImpact text COLLATE utf8_unicode_ci DEFAULT NULL,
            politicalChanges text COLLATE utf8_unicode_ci DEFAULT NULL,
            culturalChanges text COLLATE utf8_unicode_ci DEFAULT NULL,
            jobsLost bigint(12) unsigned NULL,
            damageInUSD bigint(12) unsigned NULL,
            reparationCost bigint(12) unsigned NULL,
            regulatoryChanges text COLLATE utf8_unicode_ci DEFAULT NULL,
            PRIMARY KEY (crisisId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
    
    t = wcdb_query(
            login,
            """
            CREATE TABLE Orgs (
            orgId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            name varchar(100) COLLATE utf8_unicode_ci NOT NULL,
            kind enum('Corporation','Government Agency','Military Force','Intergovernmental Agency','Intergovernmental Public Health Agency', 'Nonprofit / Humanitarian Organization') COLLATE utf8_unicode_ci NOT NULL,
            streetAddress varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
            city varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
            stateOrProvince varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
            postalCode varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
            country varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
            foundingMission text COLLATE utf8_unicode_ci DEFAULT NULL,
            datefounded datetime DEFAULT NULL,
            majorEvents text COLLATE utf8_unicode_ci DEFAULT NULL,
            PRIMARY KEY (orgId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE People (
            personId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            name varchar(100) COLLATE utf8_unicode_ci NOT NULL,
            kind enum('President','Celebrity','Actor/Actress','Musician','Politician', 'CEO','Humanitarian','Perpetrator','Regular Worker') COLLATE utf8_unicode_ci NOT NULL,
            streetAddress varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
            city varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
            stateOrProvince varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
            postalCode varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
            country varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
            PRIMARY KEY (personId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE Resources (
            resourceId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            resource text COLLATE utf8_unicode_ci NOT NULL,
            PRIMARY KEY (resourceId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)

    t = wcdb_query(
            login,
            """
            CREATE TABLE CrisisResources (
            crisisId varchar(10) COLLATE utf8_unicode_ci NOT NULL,
            resourceId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            FOREIGN KEY (crisisId) REFERENCES Crises(crisisId),
            FOREIGN KEY (resourceId) REFERENCES Resources(resourceId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """)

    t = wcdb_query(
            login,
            """
            CREATE TABLE WaysToHelp (
            helpId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            wayToHelp text COLLATE utf8_unicode_ci NOT NULL,
            PRIMARY KEY (helpId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)

    t = wcdb_query(
            login,
            """
            CREATE TABLE CrisisWaysToHelp (
            crisisId varchar(10) COLLATE utf8_unicode_ci NOT NULL,
            helpId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            FOREIGN KEY (crisisId) REFERENCES Crises(crisisId),
            FOREIGN KEY (helpId) REFERENCES WaysToHelp(helpId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """)
    
    t = wcdb_query(
            login,
            """
            CREATE TABLE ContactInfos (
            contactInfoId int(6) unsigned NOT NULL AUTO_INCREMENT,
            phoneNumber varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
            emailAddress varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
            facebookUrlId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            twitterUrlId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            websiteUrlId  varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            PRIMARY KEY (contactInfoId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE OrgContactInfos (
            orgId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            contactInfoId int(6) unsigned NOT NULL,
            FOREIGN KEY (orgId) REFERENCES Orgs(orgId),
            FOREIGN KEY (contactInfoId) REFERENCES ContactInfos(contactInfoId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE Citations (
            citationId int(6) unsigned NOT NULL AUTO_INCREMENT,
            citation text COLLATE utf8_unicode_ci NOT NULL,
            PRIMARY KEY (citationId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE CrisisCitations (
            citationId int(6) unsigned NOT NULL,
            crisisId varchar(20) COLLATE utf8_unicode_ci NOT NULL,    
            FOREIGN KEY (citationId) REFERENCES Citations(citationId),
            FOREIGN KEY (crisisId) REFERENCES Crises(crisisId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """)

    t = wcdb_query(
            login,
            """
            CREATE TABLE OrgCitations (
            orgId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            citationId int(6) unsigned NOT NULL,
            FOREIGN KEY (orgId) REFERENCES Orgs(orgId),
            FOREIGN KEY (citationId) REFERENCES Citations(citationId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """)
    
    t = wcdb_query(
            login,
            """
            CREATE TABLE PersonCitations (
            personId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            citationId int(6) unsigned NOT NULL,
            FOREIGN KEY (personId) REFERENCES People(personId),
            FOREIGN KEY (citationId) REFERENCES Citations(citationId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE Urls (
            urlId int(6) unsigned NOT NULL AUTO_INCREMENT,
            type enum('Image','Video','Map','SocialNetwork','Website','ExternalLink') COLLATE utf8_unicode_ci NOT NULL,
            urlAddress text COLLATE utf8_unicode_ci NOT NULL,
            PRIMARY KEY (urlId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE CrisisUrls (
            crisisId varchar(10) COLLATE utf8_unicode_ci NOT NULL,
            urlId int(6) unsigned NOT NULL,
            FOREIGN KEY (crisisId) REFERENCES Crises(crisisId),
            FOREIGN KEY (urlId) REFERENCES Urls(urlId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE OrgUrls (
            orgId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            urlId int(6) unsigned NOT NULL,
            FOREIGN KEY (orgId) REFERENCES Orgs(orgId),
            FOREIGN KEY (urlId) REFERENCES Urls(urlId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE PersonUrls (
            personId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            urlId int(6) unsigned NOT NULL,
            FOREIGN KEY (personId) REFERENCES People(personId),
            FOREIGN KEY (urlId) REFERENCES Urls(urlId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE CrisisOrgs (
            crisisId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            orgId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            FOREIGN KEY (crisisId) REFERENCES Crises(crisisId),
            FOREIGN KEY (orgId) REFERENCES Orgs(orgId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """)

    t = wcdb_query(
            login,
            """
            CREATE TABLE CrisisPeople (
            crisisId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            personId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            FOREIGN KEY (crisisId) REFERENCES Crises(crisisId),
            FOREIGN KEY (personId) REFERENCES People(personId)
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """)
            
    t = wcdb_query(
            login,
            """
            CREATE TABLE OrgPeople (
            orgId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            personId varchar(20) COLLATE utf8_unicode_ci NOT NULL,
            FOREIGN KEY (orgId) REFERENCES Orgs(orgId),
            FOREIGN KEY (personId) REFERENCES People(personId) 
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
            """)

# -----------
# data import
# -----------

global crises_id_list
crises_id_list = []
global orgs_id_list
orgs_id_list = []
global people_id_list
people_id_list = []
global resources_id_list
resources_id_list = []
global waysToHelp_id_list
waysToHelp_id_list = []

def wcdb_import(login,tree):
    """
    Iterating through crisis tags in crises tag and import into DB: table Crises
    """
    #-----------------import crises table-------------------------------------------
    inserts_list = [] #this is a list of dictionaries with each dictionary being a row in crises
    counter = 0
    root_list = tree.findall("./crises/crisis")
	global crises_id_list
	
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
        dict_entry = inserts_list[i]
        #--------------to check if current one is a duplicate----------

        if dict_entry['crisisId'] in crises_id_list:
            continue
        #--------------------------------------------------------------   
        crises_id_list.append(dict_entry['crisisId'])  # save this id in the global list, next time check if the current instance we are dealing is in this list
        s = (dict_entry.get('crisisId'), dict_entry.get('name'),dict_entry.get('kind'),dict_entry.get('streetAddress','Null'),dict_entry.get('city','Null'),\
                 dict_entry.get('stateOrProvince','Null'),dict_entry.get('country','Null'),dict_entry.get('dateAndTime','Null'),\
                 dict_entry.get('fatalities','Null'),dict_entry.get('injuries','Null'),dict_entry.get('populationIll','Null'),\
                 dict_entry.get('populationDisplaced','Null'),dict_entry.get('environmentalImpact','Null'),dict_entry.get('politicalChanges','Null'),\
                 dict_entry.get('culturalChanges','Null'),dict_entry.get('jobsLost','Null'),dict_entry.get('damageInUSD','Null'),\
                 dict_entry.get('reparationCost','Null'),dict_entry.get('regulatoryChanges','Null'))
        s = 'insert into Crises Values' + str(s) + ';'
        s =s.replace('None', 'Null')       
        t = wcdb_query(login,s)

        
    #------------------import orgs table-------------------------------
    #-----------This is gonna be similar to crisistable, so no more valuable comments------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./orgs/org")
	global orgs_id_list
	
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
        dict_entry = inserts_list[i]
		
        #--------------to check if current one is a duplicate----------	
        if dict_entry['orgId'] in orgs_id_list:
            continue
        #--------------------------------------------------------------   
        orgs_id_list.append(dict_entry['orgId'])
        s = (dict_entry.get('orgId'),dict_entry.get('name'),dict_entry.get('kind'),dict_entry.get('streetAddress','Null'),dict_entry.get('city','Null'),\
             dict_entry.get('stateOrProvince','Null'),dict_entry.get('postalCode','Null'),dict_entry.get('country','Null'),dict_entry.get('foundingMission','Null'),\
             dict_entry.get('dateFounded','Null'),dict_entry.get('majorEvents','Null'))
        s = 'insert into Orgs  Values' + str(s) + ';'
        s =s.replace('None', 'Null')
        t = wcdb_query(login,s)
            
    #------------------import people table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./people/person")
    global people_id_list
	
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
        dict_entry = inserts_list[i]
		
        #--------------to check if current one is a duplicate----------	
        if dict_entry['personId'] in people_id_list:
            continue
        #--------------------------------------------------------------     
        people_id_list.append(dict_entry['personId'])
        s = (dict_entry.get('personId'), dict_entry.get('name'),dict_entry.get('kind'),dict_entry.get('streetAddress','Null'),dict_entry.get('city','Null'),\
             dict_entry.get('stateOrProvince','Null'),dict_entry.get('postalCode','Null'),dict_entry.get('country','Null'))
        s = 'insert into People Values' + str(s) + ';'
        s =s.replace('None', 'Null')
        t = wcdb_query(login,s)
            
    #------------------import resources table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./resources/resourcePair")
    global resources_id_list
	
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
        dict_entry = inserts_list[i]
		
        #--------------to check if current one is a duplicate----------	
        if dict_entry['resourceId'] in resources_id_list:
            continue
        #--------------------------------------------------------------     
		
		resources_id_list.append(dict_entry['resourceId'])
        s = (dict_entry.get('resourceId'),dict_entry.get('resource'))
        s = 'insert into Resources Values' + str(s) + ';'
        s =s.replace('None', 'Null')
        t = wcdb_query(login,s)


    #------------------import crisisResources table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./crisisResources/crisisResourcePair")

    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1

    for i in range(0,counter):
        dict_entry = inserts_list[i]     
        s = (dict_entry.get('crisisId'),dict_entry.get('resourceId'))
        s = 'insert into CrisisResources Values' + str(s) + ';'
        s =s.replace('None', 'Null')
        t = wcdb_query(login,s)

    #------------------import waysToHelp table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./waysToHelp/wayToHelpPair")
    global waysToHelp_id_list
	
    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1

    for i in range(0,counter):
        dict_entry = inserts_list[i]    
		
		#--------------to check if current one is a duplicate----------	
        if dict_entry['helpId'] in waysToHelp_id_list:
            continue
        #--------------------------------------------------------------  
		
		waysToHelp_id_list.append(dict_entry['helpId'])
        s = (dict_entry.get('helpId'),dict_entry.get('wayToHelp'))
        s = 'insert into WaysToHelp Values' + str(s) + ';'
        t = wcdb_query(login,s)

    #------------------import crisisWaysToHelp table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./crisisWaysToHelp/crisisWayToHelpPair")
    
    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1
    
    for i in range(0,counter):
        dict_entry = inserts_list[i]       
        s = (dict_entry.get('crisisId'),dict_entry.get('helpId'))
        s = 'insert into CrisisWaysToHelp Values' + str(s) + ';'
        t = wcdb_query(login,s)

    #------------------import contactInfos table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./contactInfos/contactInfo")

    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1

    for i in range(0,counter):
        #Queryinseting - Crisis Table
        dict_entry = inserts_list[i]    
        s = (dict_entry.get('contactInfoId'),dict_entry.get('phoneNumber'), dict_entry.get('emailAddress'),\
        dict_entry.get('facebookUrlId'), dict_entry.get('twitterUrlId'), dict_entry.get('websiteUrlId'))
        s = 'insert into ContactInfos Values' + str(s) + ';'
        s =s.replace('None', 'Null')
        t = wcdb_query(login,s)
        
    #------------------import orgContactInfos table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./orgContactInfos/orgContactInfoPair")

    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1

    for i in range(0,counter):
        dict_entry = inserts_list[i]
        s = (dict_entry.get('orgId'),dict_entry.get('contactInfoId'))
        s = 'insert into OrgContactInfos Values' + str(s) + ';'
        s =s.replace('None', 'Null')
        t = wcdb_query(login,s)   

    #------------------import citations table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./citations/citationPair")
    citationIds = {}        # create a dict to save its old and new ID for joint table.

    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1
		
    for i in range(0,counter):
        #Queryinseting - Crisis Table 
        dict_entry = inserts_list[i]
        #--------------to check if current one is a duplicate----------
        s = (dict_entry.get('citation'))  # only one col here, as a result: 's' is no longer a tuple, it is a string, and you really need to do the following:
        s = s.encode('utf8') # some groups' data have weird stuff which can't be interpret as an ascii code, so you need to add this in like urls insertion as well as those with long text content
        s = 'insert into Citations (citation) Values' + "(\""+ str(s) +"\")"+ ';'
        t = wcdb_query(login,s)
        newID = login.insert_id()
        citationIds[dict_entry['citationId']] = newID
            
    #------------------import crisisCitations table---------------------------------
    #-this is a joint table, be careful to make sure you insert the right new IDs---
    inserts_list = []
    counter = 0
    root_list = tree.findall("./crisisCitations/crisisCitationPair")

    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1

    for i in range(0,counter):
        dict_entry = inserts_list[i]
		s = 'insert into CrisisCitations (citationId, crisisID) Values (' + \
                str(citationIds[dict_entry['citationId']]) + ', ' + "'"+ str(dict_entry.get('crisisId')) + "'"+ ')' + ';'
        s =s.replace('None', 'Null')
        t = wcdb_query(login,s)
#        citationId = dict_entry['citationId'] # get its old ID from the tree
#        crisisId = dict_entry['crisisId'] # get its old ID from the tree
        #----do not forget to check something like this on any joint tables:
        #----you want to make sure the one you are inserting in this joint table is not a duplicate instance in other tables
#        if citationId in citationIds and crisisId in crisisIds:  # if we want add rows in joint table for a duplicates, change "and" to "or" in this line
        #------------------------------------------------------------------
        #--------------insert new IDs based on what we have saved in citationIds dicts--------------
            #s = 'insert into CrisisCitations (citationId, crisisID) Values (' + \
            #    str(citationIds[dict_entry['citationId']]) + ', ' + "'"+ str(dict_entry.get('crisisId')) + "'"+ ')' + ';'
            #print(s)
            #s =s.replace('None', 'Null')
            #t = wcdb_query(login,s)

    #------------------import orgCitations table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./orgCitations/orgCitationPair")

    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1

    for i in range(0,counter):
        dict_entry = inserts_list[i]
        s = (dict_entry.get('orgId'),citationIds[dict_entry['citationId']])
        s = 'insert into OrgCitations Values' + str(s) + ';'
        s =s.replace('None', 'Null')
        t = wcdb_query(login,s)

    #------------------import personCitations table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./personCitations/personCitationPair")

    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1

    for i in range(0,counter):
        dict_entry = inserts_list[i]       
        s = (dict_entry.get('personId'), citationIds[dict_entry['citationId']])
        s = 'insert into PersonCitations Values' + str(s) + ';'
        s =s.replace('None', 'Null')
        t = wcdb_query(login,s)

    #------------------import urls table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./urls/url")
    urlIds = {}        # create a dict to save its old and new ID for joint table.

    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1
		
    for i in range(0,counter):
        #Queryinseting - Crisis Table 
        dict_entry = inserts_list[i]
        #--------------to check if current one is a duplicate----------
        s = dict_entry.get('type')   # only one col here, as a result: 's' is no longer a tuple, it is a string, and you really need to do the following:
        u = dict_entry.get('urlAddress')
		u = u.encode('utf8') # some groups' data have weird stuff which can't be interpret as an ascii code, so you need to add this in like urls insertion as well as those with long text content
        s = 'insert into Urls (type, urlAddress) Values' + "(" + str(s) + ', ' + "\"" + str(u) + "\")"+ ';'
        t = wcdb_query(login,s)
        newID = login.insert_id()
        urlIds[dict_entry['urlId']] = newID

    #------------------import crisisUrls table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./crisisUrls/crisisUrlPair")

    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1

    for i in range(0,counter):
        dict_entry = inserts_list[i]      
		s = 'insert into CrisisUrls Values (' + "'" + str(dict_entry.get('crisisId')) + "'" + ', ' + str(urlIds[dict_entry['urlId']]) + ');'
        t = wcdb_query(login,s)


    #------------------import orgUrls table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./orgUrls/orgUrlPair")

    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1

    for i in range(0,counter):
        dict_entry = inserts_list[i]
        s = 'insert into OrgUrls Values (' + "'" + str(dict_entry.get('orgId')) + "', " + str(urlIds[dict_entry['urlId']]) + ');'
        t = wcdb_query(login,s)

    #------------------import personUrls table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./personUrls/personUrlPair")

    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1

    for i in range(0,counter):
        dict_entry = inserts_list[i]
        s = 'insert into PersonUrls Values (' + "'" str(dict_entry.get('personId')) + "'," + str(urlIds[dict_entry['urlId']]) + ');'
        t = wcdb_query(login,s)

    #------------------import crisisOrgs table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./crisisOrgs/crisisOrgPair")

    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1

    for i in range(0,counter):
        dict_entry = inserts_list[i]
        s = (dict_entry.get('crisisId'),dict_entry.get('orgId'))
        s = 'insert into CrisisOrgs Values' + str(s) + ';'
        s =s.replace('None', 'Null')
        t = wcdb_query(login,s)

    #------------------import crisisPeople table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./crisisPeople/crisisPersonPair")

    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1

    for i in range(0,counter):
        dict_entry = inserts_list[i]       
        s = (dict_entry.get('crisisId'),dict_entry.get('personId'))
        s = 'insert into CrisisPeople Values' + str(s) + ';'
        s =s.replace('None', 'Null')
        t = wcdb_query(login,s)
	
    #------------------import orgPeople table-------------------------------
    inserts_list = []
    counter = 0
    root_list = tree.findall("./orgPeople/orgPersonPair")

    for parent in root_list:
        insert_entry = {}
        #Iterates over Children
        for child in parent:
            if child.getchildren() == []:
                insert_entry[child.tag] = child.text
        inserts_list.append(insert_entry)
        counter += 1

    for i in range(0,counter):
        dict_entry = inserts_list[i]      
        s = (dict_entry.get('orgId'),dict_entry.get('personId'))
        s = 'insert into OrgPeople Values' + str(s) + ';'
        s =s.replace('None', 'Null')
        t = wcdb_query(login,s)
        
#--------------------end of import----------------
        
##def wcdb_import(login, tree):
##    crises_import(login, tree)
##    return None

# -------------
# data export
# -------------
def tree_builder(tag, content = ''):
	"""builds 1 xml tree """
	builder = ET.TreeBuilder()
	
	builder.start(tag, {})
	builder.data(content)
	builder.end(tag)
	
	return builder.close()
    
def wcdb_export(login):
    """Generates ElementTree from DB
    root: <root></root>
    crises_tree: <crises></crises>
    """
    root = tree_builder('root')
    
    # -------------Crisis Export-------------
    tree_counter = 0
    crises_tree = ET.Element('crises') ##  or  crises_tree = tree_builder('crises'), either way seems to work.
    root.append(crises_tree)   
    
    crises = wcdb_query(
        login, 
	""" select *
	from Crises;
	""")
    crises_tag_tuple = wcdb_query(
        login, 
	""" show columns
	from Crises;
	""")
    for i in range(len(crises)):
        crisis_tree = ET.Element('crisis')
        root[tree_counter].append(crisis_tree)
        assert (type(crises[i]) is tuple)
        tag_counter = 0
        for entry in crises[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(crises_tag_tuple[tag_counter][0],entry))
            tag_counter += 1
    
    # -------------orgs Export-------------
    tree_counter += 1
    orgs_tree = ET.Element('orgs') ##  or  crises_tree = tree_builder('crises'), either way seems to work.
    root.append(orgs_tree)      
    orgs = wcdb_query(
        login, 
        """ select *
        from Orgs;
        """)
    orgs_tag_tuple = wcdb_query(
        login, 
        """ show columns
        from Orgs;
        """)
    for i in range(len(orgs)):
        orgs_tree = ET.Element('org')
        root[tree_counter].append(orgs_tree)
        assert (type(orgs[i]) is tuple)
        tag_counter = 0
        for entry in orgs[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(orgs_tag_tuple[tag_counter][0],entry))
            tag_counter += 1
            
    # -------------people Export-------------
    tree_counter += 1
    people_tree = ET.Element('people') ##  or  crises_tree = tree_builder('crises'), either way seems to work.
    root.append(people_tree)   
    people = wcdb_query(
        login, 
    """ select *
    from People;
    """)
    people_tag_tuple = wcdb_query(
        login, 
    """ show columns
    from People;
    """)
    for i in range(len(people)):
        people_tree = ET.Element('person')
        root[tree_counter].append(people_tree)
        assert (type(people[i]) is tuple)
        tag_counter = 0
        for entry in people[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(people_tag_tuple[tag_counter][0],entry))
            tag_counter += 1

   # -------------resources Export-------------
    tree_counter += 1
    resources_tree = ET.Element('resources') ##  or  crises_tree = tree_builder('crises'), either way seems to work.
    root.append(resources_tree)    
    resources = wcdb_query(
        login, 
    """ select *
    from Resources;
    """)
    resources_tag_tuple = wcdb_query(
        login, 
    """ show columns
    from Resources;
    """)
    for i in range(len(resources)):
        resources_tree = ET.Element('resourcePair')
        root[tree_counter].append(resources_tree)
        assert (type(resources[i]) is tuple)
        tag_counter = 0
        for entry in resources[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(resources_tag_tuple[tag_counter][0],entry))
            tag_counter += 1

    # -------------crisisResources Export-------------
    tree_counter += 1
    crisisResources_tree = ET.Element('crisisResources') ##  or  crises_tree = tree_builder('crises'), either way seems to work.
    root.append(crisisResources_tree)     
    crisisResources = wcdb_query(
        login, 
    """ select *
    from CrisisResources;
    """)
    crisisResources_tag_tuple = wcdb_query(
        login, 
    """ show columns
    from CrisisResources;
    """)
    for i in range(len(crisisResources)):
        crisisResources_tree = ET.Element('crisisResourcePair')
        root[tree_counter].append(crisisResources_tree)
        assert (type(crisisResources[i]) is tuple)
        tag_counter = 0
        for entry in crisisResources[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(crisisResources_tag_tuple[tag_counter][0],entry))
            tag_counter += 1

    # -------------waysToHelp Export-------------
    tree_counter += 1
    waysToHelp_tree = ET.Element('waysToHelp') ##  or  crises_tree = tree_builder('crises'), either way seems to work.
    root.append(waysToHelp_tree)   
    waysToHelp = wcdb_query(
        login, 
    """ select *
    from WaysToHelp;
    """)
    waysToHelp_tag_tuple = wcdb_query(
        login, 
    """ show columns
    from WaysToHelp;
    """)
    for i in range(len(waysToHelp)):
        waysToHelp_tree = ET.Element('wayToHelpPair')
        root[tree_counter].append(waysToHelp_tree)
        assert (type(waysToHelp[i]) is tuple)
        tag_counter = 0
        for entry in waysToHelp[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(waysToHelp_tag_tuple[tag_counter][0],entry))
            tag_counter += 1

    # -------------crisisWaysToHelp Export-------------
    tree_counter += 1
    crisisWaysToHelp_tree = ET.Element('crisisWaysToHelp') ##  or  crises_tree = tree_builder('crises'), either way seems to work.
    root.append(crisisWaysToHelp_tree)   
    crisisWaysToHelp = wcdb_query(
        login, 
    """ select *
    from CrisisWaysToHelp;
    """)
    crisisWaysToHelp_tag_tuple = wcdb_query(
        login, 
    """ show columns
    from CrisisWaysToHelp;
    """)
    for i in range(len(crisisWaysToHelp)):
        crisisWaysToHelp_tree = ET.Element('crisisWayToHelpPair')
        root[tree_counter].append(crisisWaysToHelp_tree)
        assert (type(crisisWaysToHelp[i]) is tuple)
        tag_counter = 0
        for entry in crisisWaysToHelp[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(crisisWaysToHelp_tag_tuple[tag_counter][0],entry))
            tag_counter += 1

    # -------------contactInfos Export-------------
    tree_counter += 1
    contactInfos_tree = ET.Element('contactInfos') ##  or  crises_tree = tree_builder('crises'), either way seems to work.
    root.append(contactInfos_tree)     
    contactInfos = wcdb_query(
        login, 
    """ select *
    from ContactInfos;
    """)
    contactInfos_tag_tuple = wcdb_query(
        login, 
    """ show columns
    from ContactInfos;
    """)
    for i in range(len(contactInfos)):
        contactInfos_tree = ET.Element('contactInfos')
        root[tree_counter].append(contactInfos_tree)
        assert (type(contactInfos[i]) is tuple)
        tag_counter = 0
        for entry in contactInfos[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(contactInfos_tag_tuple[tag_counter][0],entry))
            tag_counter += 1

    # -------------orgContactInfos Export-------------
    tree_counter += 1
    orgContactInfos_tree = ET.Element('orgContactInfos') ##  or  crises_tree = tree_builder('crises'), either way seems to work.
    root.append(orgContactInfos_tree)   
    orgContactInfos = wcdb_query(
        login, 
    """ select *
    from OrgContactInfos;
    """)
    orgContactInfos_tag_tuple = wcdb_query(
        login, 
    """ show columns
    from OrgContactInfos;
    """)
    for i in range(len(orgContactInfos)):
        orgContactInfos_tree = ET.Element('orgContactInfoPair')
        root[tree_counter].append(orgContactInfos_tree)
        assert (type(orgContactInfos[i]) is tuple)
        tag_counter = 0
        for entry in orgContactInfos[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(orgContactInfos_tag_tuple[tag_counter][0],entry))
            tag_counter += 1
            
    # -------------citations Export-------------
    tree_counter += 1
    citations_tree = ET.Element('citations') ##  or  citations_tree = tree_builder('citations'), either way seems to work.
    root.append(citations_tree)     
    citations = wcdb_query(
        login, 
	""" select *
	from Citations;
	""")
    citations_tag_tuple = wcdb_query(
        login, 
	""" show columns
	from Citations;
	""")
    for i in range(len(citations)):
        citationPair_tree = ET.Element('citationPair')
        root[tree_counter].append(citationPair_tree)
        assert (type(citations[i]) is tuple)
        tag_counter = 0
        for entry in citations[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(citations_tag_tuple[tag_counter][0],entry))
            tag_counter += 1
            
    # -------------crisisCitations Export-------------
    tree_counter += 1			
    crisisCitations_tree = ET.Element('crisisCitations') ##  or  crisisCitations_tree = tree_builder('crisisCitations'), either way seems to work.
    root.append(crisisCitations_tree)   
    crisisCitations = wcdb_query(
        login, 
	""" select *
	from CrisisCitations;
	""")
    crisisCitations_tag_tuple = wcdb_query(
        login, 
	""" show columns
	from CrisisCitations;
	""")
    for i in range(len(crisisCitations)):
        crisisCitationPair_tree = ET.Element('crisisCitationPair')
        root[tree_counter].append(crisisCitationPair_tree)
        assert (type(crisisCitations[i]) is tuple)
        tag_counter = 0
        for entry in crisisCitations[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(crisisCitations_tag_tuple[tag_counter][0],entry))
            tag_counter += 1
            
    # -------------orgCitations Export-------------
    tree_counter += 1			
    orgCitations_tree = ET.Element('orgCitations') ##  or  orgCitations_tree = tree_builder('orgCitations'), either way seems to work.
    root.append(orgCitations_tree)   
    orgCitations = wcdb_query(
        login, 
	""" select *
	from OrgCitations;
	""")
    orgCitations_tag_tuple = wcdb_query(
        login, 
	""" show columns
	from OrgCitations;
	""")
    for i in range(len(orgCitations)):
        orgCitationPair_tree = ET.Element('orgCitationPair')
        root[tree_counter].append(orgCitationPair_tree)
        assert (type(orgCitations[i]) is tuple)
        tag_counter = 0
        for entry in orgCitations[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(orgCitations_tag_tuple[tag_counter][0],entry))
            tag_counter += 1
            
    # -------------personCitations Export-------------
    tree_counter += 1			
    personCitations_tree = ET.Element('personCitations') ##  or  personCitations_tree = tree_builder('personCitations'), either way seems to work.
    root.append(personCitations_tree)     
    personCitations = wcdb_query(
        login, 
	""" select *
	from PersonCitations;
	""")
    personCitations_tag_tuple = wcdb_query(
        login, 
	""" show columns
	from PersonCitations;
	""")
    for i in range(len(personCitations)):
        personCitationPair_tree = ET.Element('personCitationPair')
        root[tree_counter].append(personCitationPair_tree)
        assert (type(personCitations[i]) is tuple)
        tag_counter = 0
        for entry in personCitations[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(personCitations_tag_tuple[tag_counter][0],entry))
            tag_counter += 1
            
    # -------------urls Export-------------
    tree_counter += 1	
    urls_tree = ET.Element('urls') ##  or  urls_tree = tree_builder('urls'), either way seems to work.
    root.append(urls_tree)   
    urls = wcdb_query(
        login, 
	""" select *
	from Urls;
	""")
    urls_tag_tuple = wcdb_query(
        login, 
	""" show columns
	from Urls;
	""")
    for i in range(len(urls)):
        url_tree = ET.Element('url')
        root[tree_counter].append(url_tree)
        assert (type(urls[i]) is tuple)
        tag_counter = 0
        for entry in urls[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(urls_tag_tuple[tag_counter][0],entry))
            tag_counter += 1

    # -------------crisisUrls Export-------------
    tree_counter += 1			
    crisisUrls_tree = ET.Element('crisisUrls') ##  or  crisisUrls_tree = tree_builder('crisisUrls'), either way seems to work.
    root.append(crisisUrls_tree)     
    crisisUrls = wcdb_query(
        login, 
	""" select *
	from CrisisUrls;
	""")
    crisisUrls_tag_tuple = wcdb_query(
        login, 
	""" show columns
	from CrisisUrls;
	""")
    for i in range(len(crisisUrls)):
        crisisUrlPair_tree = ET.Element('crisisUrlPair')
        root[tree_counter].append(crisisUrlPair_tree)
        assert (type(crisisUrls[i]) is tuple)
        tag_counter = 0
        for entry in crisisUrls[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(crisisUrls_tag_tuple[tag_counter][0],entry))
            tag_counter += 1

    # -------------orgUrls Export-------------
    tree_counter += 1				
    orgUrls_tree = ET.Element('orgUrls') ##  or  orgUrls_tree = tree_builder('orgUrls'), either way seems to work.
    root.append(orgUrls_tree)   
    orgUrls = wcdb_query(
        login, 
	""" select *
	from OrgUrls;
	""")
    orgUrls_tag_tuple = wcdb_query(
        login, 
	""" show columns
	from OrgUrls;
	""")
    for i in range(len(orgUrls)):
        orgUrlPair_tree = ET.Element('orgUrlPair')
        root[tree_counter].append(orgUrlPair_tree)
        assert (type(orgUrls[i]) is tuple)
        tag_counter = 0
        for entry in orgUrls[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(orgUrls_tag_tuple[tag_counter][0],entry))
            tag_counter += 1
            
    # -------------personUrls Export-------------
    tree_counter += 1			
    personUrls_tree = ET.Element('personUrls') ##  or  personUrls_tree = tree_builder('personUrls'), either way seems to work.
    root.append(personUrls_tree)    
    personUrls = wcdb_query(
        login, 
	""" select *
	from PersonUrls;
	""")
    personUrls_tag_tuple = wcdb_query(
        login, 
	""" show columns
	from PersonUrls;
	""")
    for i in range(len(personUrls)):
        personUrlPair_tree = ET.Element('personUrlPair')
        root[tree_counter].append(personUrlPair_tree)
        assert (type(personUrls[i]) is tuple)
        tag_counter = 0
        for entry in personUrls[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(personUrls_tag_tuple[tag_counter][0],entry))
            tag_counter += 1
            
    # -------------crisisOrgs Export-------------
    tree_counter += 1
    crisisOrgs_tree = ET.Element('crisisOrgs') ##  or  crisisOrgs_tree = tree_builder('crisisOrgs'), either way seems to work.
    root.append(crisisOrgs_tree)   
    crisisOrgs = wcdb_query(
        login, 
	""" select *
	from CrisisOrgs;
	""")
    crisisOrgs_tag_tuple = wcdb_query(
        login, 
	""" show columns
	from CrisisOrgs;
	""")
    for i in range(len(crisisOrgs)):
        crisisOrgPair_tree = ET.Element('crisisOrgPair')
        root[tree_counter].append(crisisOrgPair_tree)
        assert (type(crisisOrgs[i]) is tuple)
        tag_counter = 0
        for entry in crisisOrgs[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(crisisOrgs_tag_tuple[tag_counter][0],entry))
            tag_counter += 1
            
    # -------------crisisPeople Export-------------
    tree_counter += 1		
    crisisPeople_tree = ET.Element('crisisPeople') ##  or  crisisPeople_tree = tree_builder('crisisPeople'), either way seems to work.
    root.append(crisisPeople_tree)   
    crisisPeople = wcdb_query(
        login, 
	""" select *
	from CrisisPeople;
	""")
    crisisPeople_tag_tuple = wcdb_query(
        login, 
	""" show columns
	from CrisisPeople;
	""")
    for i in range(len(crisisPeople)):
        crisisPersonPair_tree = ET.Element('crisisPersonPair')
        root[tree_counter].append(crisisPersonPair_tree)
        assert (type(crisisPeople[i]) is tuple)
        tag_counter = 0
        for entry in crisisPeople[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(crisisPeople_tag_tuple[tag_counter][0],entry))
            tag_counter += 1
            
    # -------------orgPeople Export-------------
    tree_counter += 1		
    orgPeople_tree = ET.Element('orgPeople') ##  or  orgPeople_tree = tree_builder('orgPeople'), either way seems to work.
    root.append(orgPeople_tree)   
    orgPeople = wcdb_query(
        login, 
	""" select *
	from OrgPeople;
	""")
    orgPeople_tag_tuple = wcdb_query(
        login, 
	""" show columns
	from OrgPeople;
	""")
    for i in range(len(orgPeople)):
        orgPersonPair_tree = ET.Element('orgPersonPair')
        root[tree_counter].append(orgPersonPair_tree)
        assert (type(orgPeople[i]) is tuple)
        tag_counter = 0
        for entry in orgPeople[i]:
            if entry == None:
                entry = 'NULL'
            root[tree_counter][i].append(tree_builder(orgPeople_tag_tuple[tag_counter][0],entry))
            tag_counter += 1
            
    return root
#------------------end of export-------------------------

# ----------
# wcdb_read
# ---------- 

def wcdb_read (stdin,flag,filename=" "):
    """
    reads xml_filename_list
    creates an element tree from string
    flag is for reading choices
    default filename is empty space
    """
    if flag == True:
        imported_str_data = str(stdin.read())
##        imported_str_data = imported_str_data.decode('utf-8')
        assert(type(imported_str_data) is str)
        data_tree = ET.fromstring(imported_str_data)
        assert(type(data_tree) is ET.Element)
        return data_tree
    
    else:
    #---- instead of Stdin and Stdout as arguments, this read function now only read filename---------
        r = open(filename, 'r')      
        imported_str_data = str(r.read())
        assert(type(imported_str_data) is str)
        data_tree = ET.fromstring(imported_str_data)
        assert(type(data_tree) is ET.Element)
        print(data_tree)  # for debugging fake, it tells you which file do bugs come from.
        return data_tree    
    
# ------------
# wcdb_write
# ------------
def wcdb_write (w, data_tree):
    """
    converts an element string to a string data
    exports the string data 
    """
    rough_exported_string = ET.tostring(data_tree, encoding='utf-8', method = "xml")
    assert(type(rough_exported_string) is str)
    reparsed = minidom.parseString(rough_exported_string)
    pretty_exported_string = reparsed.toprettyxml(indent="\t")
    w.write(pretty_exported_string)

# ------------
# wcdb_solve
# ------------
def wcdb_solve(r,w,xml_filename_list):
    """
    r is a reader
    w is a writer
    login: Logs into DB, tree: Generates Element Tree,
    createDB(login): Creates Tables in DB,
    wcdb_import: import data from xml to databases
    wcdb_export: export data from databases to xml
    """   
    a = ("z","joshen","pb6bKYnCDs","cs327e_joshen")
#    a = ("localhost", "root", "121314", "cs327e-wcdb")
    login_var = wcdb_login(*a)
    #-------------for acceptance tests-----------------

    createDB(login_var)
    r_flag = True
    data_tree = wcdb_read(r,r_flag)
    wcdb_import(login_var, data_tree)
    export_data = wcdb_export(login_var)
    wcdb_write (w, export_data)
    
    #----for real data from 8 groups-------------------

    #crises_id_list = []
    #orgs_id_list = []
    #people_id_list = []
    #citation_list = []

    createDB(login_var)
    r_flag = False
    for filename in xml_filename_list:
        data_tree = wcdb_read(r,r_flag,filename)
        wcdb_import(login_var, data_tree)       
    #export_data = wcdb_export(login_var)
    #write = open('WCDB.out.xml', 'w')
    #wcdb_write (write, export_data)
    #write.close()

