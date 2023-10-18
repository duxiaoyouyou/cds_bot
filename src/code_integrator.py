import os  
  
class CodeInserter:  
    def __init__(self, input_filepath, output_filepath):  
        self.input_filepath = input_filepath  
        self.output_filepath = output_filepath  
  
    def insert_after(self, target_string, code):  
        with open(self.input_filepath, 'r') as file:  
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
  

# Usage  
#inserter = CodeInserter(f'resources/cdsViews/core/I_HCM_ESSFamilyMemberTP', 'src/resources/cdsViews/sg/I_SG_HCM_ESSFamilyMemberTP')  
input_filepath = os.path.join(os.getcwd(), 'src\\resources\\cdsViews\\core\\I_HCM_ESSFamilyMemberTP')  
output_filepath = os.path.join(os.getcwd(), 'src\\resources\\cdsViews\\sg\\I_SG_HCM_ESSFamilyMemberTP')  
inserter = CodeInserter(input_filepath, output_filepath)  
inserter.insert_after('as select from I_HCM_ESSFamilyMember', 'cds_country_version')  

