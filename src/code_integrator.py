import os  
from jinja2 import Environment, FileSystemLoader


class CodeIntegrator:  
    def __init__(self, output_filepath): 
        self.output_filepath = output_filepath  
  
  
    def insert_after(self, target_string, code, input_filepath):  
        with open(input_filepath, 'r') as file:  
            lines = file.readlines()  
  
        # Find the line number of the first line containing the target string  
        line_number = next((i for i, line in enumerate(lines) if target_string in line), None)  
  
        if line_number is not None:  
            # Insert the code after the target line  
            lines.insert(line_number + 1, code + '\n')  
  
            # Check if the output directory exists, if not, create it  
            output_dir = os.path.dirname(self.output_filepath)  
            if not os.path.exists(output_dir):  
                os.makedirs(output_dir)  
  
            # Check if the output file exists, if so, remove it  
            if os.path.exists(self.output_filepath):  
                os.remove(self.output_filepath)  
  
            with open(self.output_filepath, 'w') as file:  
                file.writelines(lines)  
        else:  
            print(f"No line containing '{target_string}' was found in the file.")  
  
  
    def createFile(self, code):  
        # Check if the output directory exists, if not, create it  
            output_dir = os.path.dirname(self.output_filepath)  
            if not os.path.exists(output_dir):  
                os.makedirs(output_dir)  
  
            # Check if the output file exists, if so, remove it  
            if os.path.exists(self.output_filepath):  
                os.remove(self.output_filepath)  
  
            with open(self.output_filepath, 'w') as file:  
                file.writelines(code)
                


    def handle_with_template(template_file_name: str, calculation_detail):
        environment = Environment(loader=FileSystemLoader('resources/prompts'))
        template = environment.get_template(template_file_name)
        return template.render(detail=calculation_detail)





