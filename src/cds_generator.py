import openai
from jinja2 import Environment, FileSystemLoader
from .cds_view_detail import FamilyMemberRootTP, FamilyMemberSupplement, FamilyMemberTP, FieldDescription, Behavior

class CDSGenerator:  
    def __init__(self,  country_code: str, source_table_name: str, field_descriptions: dict, llm: openai):  
        self.country_code = country_code
        self.source_table_name = source_table_name
        self.field_descriptions = field_descriptions
        self.llm = llm  
        self.cds_fields = self.generate_cds_fields()
    
    
    def get_cds_fields(self):
        return self.cds_fields
    
    
    def generate_cds_fields(self) -> dict:  
        field_description_str = ""
        for key, description in self.field_descriptions.items():  
            field_description_str += f"{key}: {description}\n"  
         
        fieldDescription = FieldDescription(field_description_str, self.field_descriptions)
        prompt = self.generate_file_with_template('naming.jinga2', fieldDescription)
          
        response_message_content = self.get_response_message_content(prompt)
        return response_message_content

        
    def generate_cds_code_familyMemberSupplement(self) -> str:  
        cds_fields = self.cds_fields.replace(':', ' as ').replace(".", "")
        familyMemberSupplement = FamilyMemberSupplement(self.country_code, cds_fields, self.source_table_name)
        cds_view_code = self.generate_file_with_template('familyMemberSupplement.jinga2', familyMemberSupplement)
        return cds_view_code 
    
    
    def generate_cds_code_familyMemberTP(self, country_delta_fields) -> str:  
        additional_data_fields = self.filter_and_transform(self.cds_fields, country_delta_fields)   
        familyMemberTP = FamilyMemberTP(self.country_code, additional_data_fields)
        cds_view_code = self.generate_file_with_template('familyMemberTP.jinga2', familyMemberTP) 
        return cds_view_code 
    
    
    def filter_and_transform(self, text, keys):    
        lines = text.split('\n')    
        d = {}    
        for line in lines:    
            if ':' in line:    
                parts = line.split(':')    
                d[parts[0].strip().lower()] = parts[1].strip()    
        keys = {k.lower() for k in keys if k is not None}  
        filtered_dict = {k: d[k] for k in keys if k in d}    
        transformed_lines = []    
        for k, v in filtered_dict.items():    
            transformed_line = '_AdditionalData.' + v + ' // ' + k + ';'    
            transformed_lines.append(transformed_line)    
        return '\n'.join(transformed_lines)    

   
    def generate_cds_code_behavior(self) -> str:  
        behavior = Behavior(self.country_code)
        prompt = self.generate_file_with_template('behavior.jinga2', behavior)      
        return self.get_response_message_content(prompt)    


    def get_response_message_content(self, prompt: str) -> str:
        # print("prompt sent to LLM:\n " + prompt)
        messages = [ {"role": "user", "content": prompt} ]  
        response = self.llm.ChatCompletion.create(  
            engine="gpt-4",  
            messages=messages,  
            temperature=0.01  
        )  
        response_message_content = response['choices'][0]['message']['content']  
        print("response from LLM generated:\n " + response_message_content)
        return response_message_content
 

    def generate_file_with_template(self, template_file_name: str, detail):
        environment = Environment(loader=FileSystemLoader('src/resources/templates'))
        template = environment.get_template(template_file_name)
        return template.render(detail = detail)


