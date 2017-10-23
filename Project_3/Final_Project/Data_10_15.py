# Following code is for Project 3 'Wrangle OpenStreetMap Data' 

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

OSM_PATH = "adelaide_australia.osm"

# Programmatic Pieces of Code Below

# clean_value() cleans all values in any piece of the osm file
# we will be running this through all functions used
# to break up the osm file with clean_value fxn

def clean_value(string):
    '''
    Takes string as argument
    1) makes everything lower case
    2) replaces empty spaces with underscores
    '''
    clean_string = string.lower()
    if " " in clean_string:
        clean_string = clean_string.replace(" ", "_")
    return clean_string

# clean_key() cleans a specific key's value in the list of associated keys  
# and values in OSM file with mapping dictionary

key_mapping = {
    "postal_code": "postcode",
    "postcode:source": "postcode",
    "postal_address": "address"
    }

# the keys in key_mapping are only what I have identified that can be simplified
# a standardized restructuring of all keys could also be useful for this dataset

def clean_key(string):
    if string in key_mapping:
        new_string = key_mapping.get(string)
        return clean_value(new_string)
    else:
        return clean_value(string)

# clean_website() standardizes and cleans the beginnning (http://www) 
# and end (.com.au) for all 'website' key values

def clean_website(string):
    string = clean_value(string)
    string_list = string.split('.')
    count = 0

# cleaning the beginning of any website with www or http in name
    for entry in string_list:
        if 'www' in entry:
            string_list[count] = 'http://www'
        elif 'http' in entry:
            http_alone = entry.find('//') + 2
            string_list[count] = entry[0:http_alone] + 'www.' + entry[http_alone:]
        elif '/' in entry:
            cut_string = entry.find('/')
            string_list[count] = entry[0:cut_string]
        count += 1

    string_join = '.'.join(string_list)
    string_list = string_join.split('.')

# cleaning the end of the website based on the length of the list of values
# in a list when splitting the website based on '.'
    if len(string_list) > 3:
        if string_list[3] == 'au':
            string_list = string_list[:4]
        elif string_list[3] == 'com':
            string_list = string_list[:4]
            string_list.append('au')
        elif string_list[2] == 'com':
            string_list = string_list[:3]
            string_list.append('au')
        elif string_list[3] == 'org':
            string_list.append('au')
        elif string_list[2] == 'org':
            string_list = string_list[:3]
            string_list.append('au')
        elif string_list[4] == 'au':
            string_list = string_list[:5]
    elif len(string_list) <= 3:
        if 'http://www' not in string_list:
            string_list.insert(0,'http://www')
        else:
            pass

# searching for any https values and standardizing it to 'http'
    count = 0
    for entry in string_list:
        if 'https' in entry:
            string_list[count] = 'http://www'
        count += 1

# returning the end result of all the cleaning steps
    return '.'.join(string_list)

# filter_key() returns correct string for the 'key' value 
# for node & way tags in OSM File

def filter_key(string):
    string = clean_value(string)
    if len(string.split(":"))==1:
        return string
    elif len(string.split(":"))==2:
        return string.split(":")[1]
    elif len(string.split(":"))==3:
        return string.split(":")[1]+":"+string.split(":")[2]

# filter_type() returns correct string for the 'type' value in way_nodes

def filter_type(string):
    string = clean_value(string)
    if len(string.split(":"))>=2:
        return string.split(":")[0]
    else:
        return 'regular'

# following code taken from Case Study: OpenStreetMap Data
# and customized for this final project - I have hashed out
# the validation step so code runs quicker

# shape_element() will run through adelaide_australia.osm file
# and create xml structured doc that can be read and written into csvs

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    if element.tag == 'node':
        for attrName, attrValue in element.attrib.items():
            #If attributes are in FIELDS
            if attrName in node_attr_fields:
                node_attribs[attrName] = attrValue
        
        for child in element.iter('tag'):
            # if child.tag == 'tag':
                tag_node = {}
                if problem_chars.search(child.attrib["k"]):
                    continue
                # LOWER_COLON.search(child.attrib["k"]):
                else:
                    tag_node['id'] = element.attrib['id']
                    tag_node['type'] = filter_type(child.attrib['k'])
                    key = filter_key(child.attrib['k'])
                    tag_node['key'] = key
                    if key in key_mapping:
                        tag_node['key'] = clean_key(key)
                    elif key == 'website':
                        tag_node['value'] = clean_website(child.attrib['v'])
                    else:
                        tag_node['value'] = clean_value(child.attrib['v'])
                tags.append(tag_node) 
        return {'node': node_attribs, 'node_tags': tags}

            
    elif element.tag == 'way':
        for attrName, attrValue in element.attrib.items():
            #If attributes are in FIELDS
            if attrName in way_attr_fields:
                    way_attribs[attrName] = attrValue
        
        for child in element.iter('tag'):
            tag_way = {}
            if problem_chars.search(child.attrib["k"]):
                continue
            # LOWER_COLON.search(child.attrib["k"]):
            else: 
                tag_way['id'] = element.attrib['id']
                tag_way['type'] = filter_type(child.attrib['k'])
                key = filter_key(child.attrib['k'])
                tag_way['key'] = key
                if key in key_mapping:
                    tag_way['key'] = clean_key(key)
                elif key == 'website':
                    tag_way['value'] = clean_website(child.attrib['v'])
                else:
                    tag_way['value'] = clean_value(child.attrib['v'])
            tags.append(tag_way)
        
        count = -1
        for child in element.iter('nd'):    
            tag = {}
            count += 1
            tag['id'] = element.attrib['id']
            tag['node_id'] = child.attrib['ref']
            tag['position'] = count
            way_nodes.append(tag)
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# process_map() writes the outputs from shape_element() to csvs

# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                # if validate is True:
                #     validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)
