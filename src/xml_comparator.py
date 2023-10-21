import xml.etree.ElementTree as ET        
import os      
      
class XMLComparator:        
    def __init__(self, fileCore, fileCountry):        
        self.treeCore = ET.parse(fileCore)        
        self.treeCountry = ET.parse(fileCountry)       
        self.fieldsCore = self.get_field_names(self.treeCore)   
        self.fieldsCountry = self.get_field_names(self.treeCountry)   
          
        
    def get_field_names(self, tree):        
        names = []      
        for elem in tree.iter('NAME'):     
            if elem.text not in names:  
                names.append(elem.text)      
        return names      
        
        
    def get_country_delta_fields(self):      
        return [item for item in self.fieldsCountry if item not in self.fieldsCore]  
      
      
    def get_core_delta_fields(self):          
        return [item for item in self.fieldsCore if item not in self.fieldsCountry]  
      
      
    def get_common_fields(self):      
        return [item for item in self.fieldsCore if item in self.fieldsCountry]    
  
  
    def get_country_fields(self):  
        return self.fieldsCountry  
