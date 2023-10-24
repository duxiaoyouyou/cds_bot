import xml.etree.ElementTree as ET        
import os      
      
class XMLComparatorDeviation:       
    def __init__(self):      
        self.deviation_dir = "src/resources/deviation"  
        pass     
        
        
    def get_country_delta_fields(self):      
        return list(eval(open(f'{self.deviation_dir}/country_delta_fields.txt').read()))
      
      
    def get_core_delta_fields(self):          
        return list(eval(open(f'{self.deviation_dir}/core_delta_fields.txt').read() ))
      
      
    def get_common_fields(self):      
        return list(eval(open(f'{self.deviation_dir}/common_fields.txt').read() ))
      
  
    def get_country_fields(self):  
        return list(eval(open(f'{self.deviation_dir}/country_fields.txt').read()))
 
 
    def get_content(self):
        return str(open(f'{self.deviation_dir}/content.txt').read())
 
