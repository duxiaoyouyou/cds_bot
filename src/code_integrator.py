class CodeIntegrator:  
    def __init__(self, filepath):  
        self.filepath = filepath  
  
    def insert_after(self, target_line, code):  
        with open(self.filepath, 'r') as file:  
            lines = file.readlines()  
  
        # Find the line number of the target line  
        line_number = next((i for i, line in enumerate(lines) if target_line in line), None)  
  
        if line_number is not None:  
            # Insert the code after the target line  
            lines.insert(line_number + 1, code + '\n')  
  
            with open(self.filepath, 'w') as file:  
                file.writelines(lines)  
        else:  
            print(f"Target line '{target_line}' not found in the file.")  
  
# Usage  
inserter = CodeInserter('your_file_path_here')  
inserter.insert_after('your_target_line_here', 'your_code_here')  
