class TableDefinition:  
    def __init__(self, filename):  
        self.field_dict = self.create_field_dict(filename)
  
    def create_field_dict(self, filename):  
        field_dict = {}  
        with open(filename, 'r') as file:  
            for line in file:  
                parts = line.split('\t')  
                if len(parts) >= 2:  
                    field_dict[parts[0]] = parts[-1].strip() 
        return field_dict  
  
    
    def get_descriptions(self, field_names):  
        return {field: self.field_dict[field] for field in field_names if self.field_dict.get(field)}  

  
