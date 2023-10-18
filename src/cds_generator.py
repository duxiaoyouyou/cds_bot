import openai

class CDSGenerator:  
    def __init__(self, llm: openai):  
        self.llm = llm  
  
    def generate_cds_code(self, input: dict) -> str:
        # Generate the prompt  
        prompt = f"""I have a list of field names and their corresponding descriptions. 
        I want to generate ABAP CDS view fields for each of them. Here is an example of the code I want to generate:\n\n"""  
        
        prompt += "define view entity I_US_HCMFamilyMemberSupplement\n  as select from pa0106\n{\n"  
        prompt += "  key pernr as HCMPersonnelNumber,\n"  
        prompt += "  key subty as HCMSubtype,\n"  
        prompt += "  // Add more fields here\n"  
        prompt += "}\n\n"  
        
        prompt = f"""
        I have a list of field names and their corresponding descriptions. \
        I want to generate ABAP CDS view fields for each of them. \
            
        Here is an example of the code I want to generate delimited by triple quotes. \
        
        The user provides his input delimited by triple quotes. \
        \"\"\" {input} \"\"\" \    
        You will return the employee ID.
        Your answer will be in a consistent format, following the examples delimited by triple hyphens below . \
        --- 
            input: I am working in SAP, my ID is i033961 \
            i033961 \
            input: I am with ID i518639 \
            i518639 \  
        --- 
        Please only return employee id. \
        Ensure do NOT provide anything else, such as expressions. \
       """
       
        prompt += "Here are the field names and descriptions:\n\n"  
        
        for i, (field_name, description) in enumerate(input.items(), 1):  
            prompt += f"{i}. {field_name}: {description}\n"  
        
        prompt += "\nPlease generate ABAP CDS view fields for these field names and descriptions, following the example code."  
        
        # Now you can send `prompt` to the OpenAI API  
        messages = [ {"role": "user", "content": prompt} ]  
        response = self.llm.ChatCompletion.create(  
            engine="gpt-4",  
            messages=messages,  
            temperature=0.01  
        )  
        response_message_content = response['choices'][0]['message']['content']  
        print("cds name generated: " + response_message_content)  
  
  

    def generate_cds_name(self, input: dict) -> dict:  
        # Generate the prompt  
        prompt = f"I have a list of descriptions and I want to convert them into camel case and shorten them to less than 30 characters. Here are the descriptions:\n\n"  
        for i, description in enumerate(input.values(), 1):  
            prompt += f"{i}. {description}\n"  
  
        prompt += "\nPlease convert these descriptions into camel case and shorten them to less than 30 characters."  
  
        messages = [ {"role": "user", "content": prompt} ]  
        response = self.llm.ChatCompletion.create(  
            engine="gpt-4",  
            messages=messages,  
            temperature=0.01  
        )  
        response_message_content = response['choices'][0]['message']['content']  
        print("cds name generated: " + response_message_content)  
  
        # Split the response into individual descriptions  
        response_descriptions = response_message_content.split('\n')  
  
        # Remove any empty strings from the list  
        response_descriptions = [desc for desc in response_descriptions if desc]  
  
        # Create a dictionary that pairs each field name with its corresponding description  
        result = {}  
        for field_name, field_desc_camel in zip(input.keys(), response_descriptions):  
            # Remove the leading number and period from each description  
            field_desc_camel = field_desc_camel.split('. ', 1)[-1]  
            result[field_name] = field_desc_camel  
  
        return result  
