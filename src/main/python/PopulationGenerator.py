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

    populationFile = open("/Users/markuswienkemeier/Desktop/Uni/BA_neu/MatSim/my-matsim-example-project/scenarios/Salzkotten/Population", "w")
    populationFile.write('<?xml version="1.0" ?> \n <!DOCTYPE plans SYSTEM "http://www.matsim.org/files/dtd/plans_v4.dtd"> \n <plans xml:lang="de-CH"> \n')
    populationFile.close()
    populationFile = open("/Users/markuswienkemeier/Desktop/Uni/BA_neu/MatSim/my-matsim-example-project/scenarios/Salzkotten/Population", "a")
    
    for i in range(size):
        person = ET.Element("person", id=str(i))
        plan = ET.SubElement(person, "plan")
        act = getRandomNode(nodeIdList, "home", plan, "6:00")
        act = getRandomNode(nodeIdList, "home", plan, "16:00")
        act = getRandomNode(nodeIdList, "home", plan, False)
        
        rough_string = ET.tostring(person)
        
        populationFile.write(minidom.parseString(rough_string).toprettyxml(indent="    ", newl="\n"))
        
        
                        
        
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
    
