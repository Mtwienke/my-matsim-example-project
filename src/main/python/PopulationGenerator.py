import xml.etree.ElementTree as ET
from xml.dom import minidom
import random

def generateNodeList(filePath):
    tree = ET.parse(filePath)
    root = tree.getroot()
    NodeIdList = []
    
    for child in root[0]:
        NodeIdList.append((child.attrib['x'], child.attrib['y']))
        
    return NodeIdList
    
def createPopulation(size):
    
    nodeIdList = generateNodeList("/Users/markuswienkemeier/Desktop/Uni/BA_neu/MatSim/my-matsim-example-project/scenarios/Salzkotten/matsim-network.xml")
    
    populationFilePath = "/Users/markuswienkemeier/Desktop/Uni/BA_neu/MatSim/my-matsim-example-project/scenarios/Salzkotten/Population.xml"
    populationFile = open(populationFilePath, "w")
    populationFile.write('<?xml version="1.0" ?> \n<!DOCTYPE plans SYSTEM "http://www.matsim.org/files/dtd/plans_v4.dtd"> \n')
    populationFile.close()
    populationFile = open(populationFilePath, "a")
    
    ET.register_namespace("xml", "http://www.w3.org/XML/1998/namespace")
    root = ET.Element("plans", {"{http://www.w3.org/XML/1998/namespace}lang": "de"})
    
    for i in range(size):
        person = ET.SubElement(root, "person", id=str(i))
        plan = ET.SubElement(person, "plan")
        act = getRandomNode(nodeIdList, "home", plan, "6:00")
        act = getRandomNode(nodeIdList, "work", plan, "16:00")
        act = getRandomNode(nodeIdList, "home", plan, False)
        
        #rough_string = ET.tostring(population, encoding="unicode")
        #populationFile.write(ET.tostring(person, encoding="unicode",))
    formatted_xml_string = prettifyXML(root)
    #formatted_without_root = '\n'.join(line for line in formatted_xml_string if line.strip() and "population" not in line)
    finalXML = '\n'.join(formatted_xml_string)
    populationFile.write(finalXML)
    """populationFile.close()
    populationFile = open(populationFilePath, "r")
    parsedXML = minidom.parse(populationFilePath)
    populationFile.close()
    populationFile = open(populationFilePath, "w")
    populationFile.write(parsedXML.toprettyxml())"""
        
def prettifyXML(element):
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    # Generate pretty XML without the declaration
    return reparsed.toprettyxml().splitlines()[1:]
                        
        
def getRandomNode(NodeList, nodeType, parentElement, endTime):
    listlength=len(NodeList)
    match nodeType:
        case "home":
            start, end = int(0), int(listlength/2)
            actType = "h"
        case "work":
            start, end = int(listlength/2), int(listlength/2+listlength/4)
            actType = "w"
        case _:
            start, end = int(listlength/2+listlength/4), int(listlength)
            actType = "l"
    usedList = NodeList[start:end]
    node = random.choice(usedList)
    if endTime:
        element = ET.SubElement(parentElement, "act", type=actType, x=node[0], y = node[1], end_time=endTime)
    else:
        element = ET.SubElement(parentElement, "act", type=actType, x=node[0], y = node[1])
    return element
    
createPopulation(10)    
    
