import openai

class CDSGenerator:  
    def __init__(self, llm: openai):  
        self.llm = llm  
  
    def generate_cds_name(self, input: dict) -> dict:  
        # Generate the prompt  
        prompt = "I have a list of descriptions and I want to convert them into camel case and shorten them to less than 30 characters. Here are the descriptions:\n\n"  
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
