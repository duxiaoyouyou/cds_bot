import pandas as pd  
  
class ExcelHandler:  
    def __init__(self, input_dict, delimiter, excel_dir, output_file_name, second_column_name):  
        self.input_dict = input_dict  
        self.delimiter = delimiter  
        self.excel_dir = excel_dir  
        self.output_file_name = f'{excel_dir}/{output_file_name}.xlsx'  
        self.second_column_name = second_column_name 
  
   
    def process_string(self, input_string):  
        lines = input_string.split('\n')  
        data = [[item.strip() for item in line.split(self.delimiter)] for line in lines if line.strip()]  
        df = pd.DataFrame(data, columns=['Field', self.second_column_name])  
        return df 
     

    def convert_to_excel(self):  
        with pd.ExcelWriter(self.output_file_name) as writer:  
            for sheet_name, input_string in self.input_dict.items():  
                df = self.process_string(input_string)  
                df.to_excel(writer, sheet_name=sheet_name, index=False)  
                
   
