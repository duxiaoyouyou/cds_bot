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
        print(f"field_description_str sent: {field_description_str}")
         
        fieldDescription = FieldDescription(field_description_str, self.field_descriptions)
        prompt = self.generate_file_with_template('naming.jinga2', fieldDescription)
          
        response_message_content = self.get_response_message_content(prompt)

        # # Split the response into individual descriptions  
        # response_descriptions = response_message_content.split('\n')  
  
        # # Remove any empty strings from the list  
        # response_descriptions = [desc for desc in response_descriptions if desc]  
  
        # # Create a dictionary that pairs each field name with its corresponding description  
        # cds_fields = ""
        # for field_name, field_desc_camel in zip(self.field_descriptions.keys(), response_descriptions):  
        #     # Remove the leading number and period from each description  
        #     field_desc_camel = field_desc_camel.split('. ', 1)[-1]  
        #     #result[field_name] = field_desc_camel  
        #     cds_fields += f"{field_name}: {field_desc_camel}\n" 
            
        return response_message_content

        
    def generate_cds_code_familyMemberSupplement(self) -> str:  
        cds_fields = self.cds_fields.replace(':', ' as ').replace(".", "")
        familyMemberSupplement = FamilyMemberSupplement(self.country_code, cds_fields, self.source_table_name)
        prompt = self.generate_prompt_with_template('familyMemberSupplement.jinga2', familyMemberSupplement)
        
        example = f"""Here is an example of the code I want to generate with country code US and source table pa0106: \
                @AbapCatalog.viewEnhancementCategory: [#NONE] \n
                @AccessControl.authorizationCheck: #NOT_REQUIRED \n
                @EndUserText.label: 'HCM US - Related Persons' \n
                @Metadata.ignorePropagatedAnnotations: true \n
                @ObjectModel.usageType:{{ \n
                    serviceQuality: #X, \n
                    sizeCategory: #S, \n
                    dataClass: #MIXED \n
                }} \n
                define view entity I_US_HCMFamilyMemberSupplement \n
                    as select from pa0106 \n
                {{ \n
                    key pernr as HCMPersonnelNumber, \n
                    key subty as HCMSubtype \n
                }}
                """
        prompt += example            
        prompt += f"""
                Please generate ABAP CDS view for these field names and descriptions, following the example code.
                Ensure do NOT provide anything else other than the code. \
                """  
        return self.get_response_message_content(prompt)
    
    
    def generate_cds_code_familyMemberTP(self) -> str:         
        familyMemberTP = FamilyMemberTP(self.country_code.upper(), self.cds_fields)
        prompt = self.generate_prompt_with_template('familyMemberTP.jinga2', familyMemberTP) 
        return self.get_response_message_content(prompt)    

   
    def generate_cds_code_behavior(self) -> str:  
        behavior = Behavior(self.country_code)
        prompt = self.generate_prompt_with_template('behavior.jinga2', behavior)      
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


