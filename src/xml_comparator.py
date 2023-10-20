import xml.etree.ElementTree as ET      
import os    
    
class XMLComparator:      
    def __init__(self, fileCore, fileCountry):      
        self.treeCore = ET.parse(fileCore)      
        self.treeCountry = ET.parse(fileCountry)     
        self.fieldsCore = self.get_field_names(self.treeCore) 
        self.fieldsCountry = self.get_field_names(self.treeCountry) 
        
      
    def get_field_names(self, tree):      
        names = set()    
        for elem in tree.iter('NAME'):   
            names.add(elem.text)    
        return names    
      
      
    def get_country_delta_fields(self):    
        return self.fieldsCountry - self.fieldsCore
    
    
    def get_core_delta_fields(self):        
        return self.fieldsCore - self.fieldsCountry
    
    
    def get_common_fields(self):    
        return self.fieldsCore.intersection(self.fieldsCountry)  

