import xml.etree.ElementTree as ET

def get_Row(row, *attributes):
	"""this function will get the specified attributes from a row from the xml
	and return it as a tuple of type str"""
	assert(type(row) is ET.Element)
	
	data = {}
	for element in row:
		data[element.tag] = element.text
	"""the part above makes a dictionary of all the tags and their text for a given row"""
	
	query_entry = ()
	for attribute in attributes:
		query_entry += (data.get(attribute),)
	"""then we build a tuple of the all of the values that we desire using the dictionary"""
	
	s = str(query_entry)
	s.replace('None', 'NULL')
	"""since we might not have every value we want in the dictionary, we want to replace the 
	None's with Nulls before making it part of an SQL query, much like our original code"""
	
	return s
	
"""below is an example of how i thought it could run for the crises table"""

def wcdb_import(login,tree):
    #-----------------import crises table-------------------------------------------
	crisisIds = {}
    root_list = tree.findall("./crises/crisis")

    for parent in root_list:

		entries = get_Row(parent, 'name', 'kind', 'streetAddress', 'city', 'stateOrProvince', 'country', 'dateAndTime', 'fatalities',\
			'injuries', 'populationIll', 'populationDisplaced', 'environmentalImpact', 'politicalChanges', 'culturalChanges', 'jobsLost',\
			'damageInUSD', 'reparationCost', 'regulatoryChanges')
		
		query = 'insert into Crises (name, kind, streetAddress, city, stateOrProvince, country, dateAndTime, fatalities,\
			injuries, populationIll, populationDisplaced, environmentalImpact, politicalChanges, culturalChanges, jobsLost,\
			damageInUSD, reparationCost, regulatoryChanges) Values ' + entries + ';'
			     
        t = wcdb_query(login, query)
		newID = login.insert_id()
		
		crisisIds[parent[0].text] = newID
		
	#-----------------import citation table-------------------------------------------
	citationIds = {}
	root_list = tree.findall("./citations/citationPair")
	
	for parent in root_list:
		entries = get_Row(parent, 'citation')
		
		query = 'insert into Citations (citation) Values ' + entries + ';'
		
		t = wcdb_query(login, query)
		newID = login.insert_id()
		
		citationIds[parent[0].text] = newID
		
	#-----------------import crisis citation table-------------------------------------------
    root_list = tree.findall("./crisisCitations/crisisCitationPair")
	
	for pair in root_list:
		citationId = pair[0].text
		crisisId = pair[1].text
		query = 'insert into CrisisCitations (citationId, crisisId) Values (' + str(citationIds[citationId]) + ', ' + str(crisisIds[crisisId]) + ';'
		
		t = wcdb_query(login, query)