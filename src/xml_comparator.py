import xml.etree.ElementTree as ET      
import os    
    
class XMLComparator:      
    def __init__(self, file1, file2):      
        self.tree1 = ET.parse(file1)      
        self.tree2 = ET.parse(file2)      
      
    def get_names(self, tree):      
        names = set()    
        for elem in tree.iter('NAME'):    
            # Add the NAME to the set    
            names.add(elem.text)    
        return names    
      
    def get_country_delta_fields(self):      
        names1 = self.get_names(self.tree1)      
        names2 = self.get_names(self.tree2)      
        return names2 - names1
    
    def get_core_delta_fields(self):      
        names1 = self.get_names(self.tree1)      
        names2 = self.get_names(self.tree2)      
        return names1 - names2
