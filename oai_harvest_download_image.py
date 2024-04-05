from sickle import Sickle
from sickle.iterator import OAIResponseIterator,OAIItemIterator
import xml.etree.ElementTree as ET
from xml.etree import cElementTree as ElementTree
from urllib.request import urlretrieve
import os
import subprocess


class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})

sickle = Sickle('http://mint-oai.ails.ece.ntua.gr/fashion/oai?', iterator = OAIItemIterator)
# sickle = Sickle('http://mint-oai.ails.ece.ntua.gr/fashion/oai?', iterator=OAIResponseIterator)

# records = sickle.ListRecords(metadataPrefix='rdf')

# sets = sickle.ListSets


# records = sickle.ListRecords(metadataPrefix='rdf', set='1045', ignore_deleted=True) # Shoe or no shoes
# records = sickle.ListRecords(metadataPrefix='rdf', set='1008') # MISSONI
# records = sickle.ListRecords(metadataPrefix='rdf', set='1018') # Peloponnesian Folklore Foundation
# records = sickle.ListRecords(metadataPrefix='rdf', set='1002') # Pitti Immagine
# records = sickle.ListRecords(metadataPrefix='rdf', set='1052') # Modemuseum Hasselt
# records = sickle.ListRecords(metadataPrefix='rdf', set='1031') # Museum of Applied Art
# records = sickle.ListRecords(metadataPrefix='rdf', set='1049') # University of Antwerp
# records = sickle.ListRecords(metadataPrefix='rdf', set='1046') # Israel Museum, Jerusalem
# records = sickle.ListRecords(metadataPrefix='rdf', set='1030') # MUDE - Museum of Design and Fashion
# records = sickle.ListRecords(metadataPrefix='rdf', set='1029') # Les Arts Décoratifs

# records = sickle.ListRecords(metadataPrefix='edm_fp', set='1045')
# print(type(records))
# i =0 
# parent_dir = "/data/data1/users/ksismanis/testoai"
# directory = "1045"
# path = os.path.join(parent_dir, directory)
# try:
#     os.mkdir(path)
# except OSError as error:
#     print(error) 
# print("Directory '%s' created" %directory) 
# urls = []
# for record in records:
#     try:
#         # print(record.header.xml.find('{http://www.openarchives.org/OAI/2.0/}datestamp').text)
#         # print(record)
#         i=i+1
#         print("number of records:"+ str(i))
#         if records.resumption_token and not records.resumption_token.token:
#         # resumption token with empty body means last response    
#             break
#         print(records.resumption_token)
#         root = ElementTree.XML(record.raw)
#         xmldict = XmlDictConfig(root)
#         meta = xmldict['{http://www.openarchives.org/OAI/2.0/}metadata']
#         rdf = meta['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF']
#         procho = rdf['{http://www.europeana.eu/schemas/edm/}ProvidedCHO']
#         # print(procho)
#         # for key in procho:
#         #     print(key)
#         rdfabout = procho['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']
#         # identifier = procho['{http://purl.org/dc/elements/1.1/}identifier']
#         agg = rdf['{http://www.openarchives.org/ore/terms/}Aggregation']
#         isshownby = agg['{http://www.europeana.eu/schemas/edm/}isShownBy']
#         url = isshownby['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']
#         urls.append(url)
#     except StopIteration:
#         pass

# print("size of urls " + str(len(urls)))
# for record in records:
#     try:
#         i=i+1
#         print(i)
#         root = ElementTree.XML(records.raw)
#         xmldict = XmlDictConfig(root)
#         meta = xmldict['{http://www.openarchives.org/OAI/2.0/}metadata']
#         rdf = meta['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF']
#         procho = rdf['{http://www.europeana.eu/schemas/edm/}ProvidedCHO']
#         print(procho)
#         # for key in procho:
#         #     print(key)
#         rdfabout = procho['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']
#         # identifier = procho['{http://purl.org/dc/elements/1.1/}identifier']
#         agg = rdf['{http://www.openarchives.org/ore/terms/}Aggregation']
#         isshownby = agg['{http://www.europeana.eu/schemas/edm/}isShownBy']
#         url = isshownby['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']
#         print(rdfabout,url)
#         # path, headers = urlretrieve(url,url.split('/')[-1])
#         # for name, value in headers.items():
#         #     print(name, value)
#         subprocess.call(["wget","-c", "-P","1045", url])
#     except StopIteration:
#         pass



# tree  = ET.parse(records.next().raw)

# ------------- one file example---------------------------






#------------------------------- all files ------------------------

# orglist = [1045,1008,1018,1002,1052,1031,1049,1046,1030,1029]
# orglist = [1031,1049,1046,1030,1029]
# orglist = [1018]
orglist = [1045]

for org in orglist:
    i =0 
    parent_dir = "/data/data1/users/ksismanis/testoai"
    directory = str(org)
    path = os.path.join(parent_dir, directory)
    try:
        os.mkdir(path)
    except OSError as error:
        print(error) 
    print("Directory '%s' created" %directory) 
    records = sickle.ListRecords(metadataPrefix='rdf', set=str(org)) # iterate orgs
    # urls = {}
    urls = []
    record_count = 0
    no_isShownBys = 0
    isShownBys = 0
    for record in records:
        try:
            root = ElementTree.XML(record.raw)
        except StopIteration:
            pass
        xmldict = XmlDictConfig(root)
        meta = xmldict['{http://www.openarchives.org/OAI/2.0/}metadata']
        rdf = meta['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF']
        procho = rdf['{http://www.europeana.eu/schemas/edm/}ProvidedCHO']
        # identifier = procho['{http://purl.org/dc/elements/1.1/}identifier']
        rdfabout = procho['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']
        agg = rdf['{http://www.openarchives.org/ore/terms/}Aggregation']
        try:
            isshownby = agg['{http://www.europeana.eu/schemas/edm/}isShownBy']
            url = isshownby['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']
            # print(url)
            isShownBys = isShownBys +1
        except KeyError:
            print("link not found for record: ", rdfabout)
            no_isShownBys = no_isShownBys+1
            continue
        # print(isshownby['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'])
        # urls[rdfabout] = url
        urls.append(url)
        record_count = record_count+1
    print("Numbers of records retrieved for "  + str(org) + " is " + str(record_count) )
    print("Numbers of isShownbys and noisShownbys retrieved for "  + str(org) + " is " + str(isShownBys) + ' ' + str(no_isShownBys) )

    parent_dir = "/data/data1/users/ksismanis/testoai"
    # for key in urls:
    #     url = urls[key]
    for url in urls:
        # url = urls[key]
        # print(url)
        # directory = str(org)
        # path = os.path.join(parent_dir, directory)
        # try:
        #     os.mkdir(path)
        #     # print("Directory '%s' created" %directory) 
        # except OSError as error:
        #     print(error) 
        # subprocess.call(["wget","-nc -P", str(org), url])
        FNULL = open(os.devnull, 'w')
        retcode = subprocess.call(["wget","-nc","-P", str(org),"-O",url.split("/")[-2]+'_'+url.split("/")[-1], url], stdout=FNULL, stderr=subprocess.STDOUT)
        # print(url, "downloaded")


# print(urls)