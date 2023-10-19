class BehaviorClassModifier:  
    def __init__(self, core_file, us_file):  
        with open(core_file, 'r') as file:  
            self.core_class = file.read()  
        with open(us_file, 'r') as file:  
            self.us_class = file.read()  
  
    def copy_methods(self):  
        core_methods = self.extract_methods(self.core_class)  
        us_methods = self.extract_methods(self.us_class)  
  
        for method_name, method_body in core_methods.items():  
            if method_name in us_methods:  
                self.us_class = self.us_class.replace(us_methods[method_name], method_body)  
  
        return self.us_class  
  
    def extract_methods(self, class_code):  
        methods = {}  
        lines = class_code.split('\n')  
        method_name = None  
        method_body = []  
  
        for line in lines:  
            if line.strip().startswith('METHOD'):  
                method_name = line.strip().split(' ')[1].split('.')[1]  
                method_body = [line]  
            elif line.strip() == 'ENDMETHOD.':  
                method_body.append(line)  
                methods[method_name] = '\n'.join(method_body)  
                method_name = None  
                method_body = []  
            elif method_name:  
                method_body.append(line)  
  
        return methods  
    
    
    def add_read_method(self, field_name, field_type):  
        method_template = f"""  
        METHODS read_{field_name} FOR READ BY {field_name}  
          IMPORTING keys FOR {field_name}  
          RESULT result.  
        """  
        self.us_class += method_template  
        
  
    def write_to_file(self, filename):  
        with open(filename, 'w') as file:  
            file.write(self.us_class)  
            
  
modifier = BehaviorClassModifier('core_class.abap', 'us_class.abap')  
modifier.copy_methods()  
modifier.write_to_file('new_us_class.abap')  
