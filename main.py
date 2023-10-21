import openai    
import streamlit as st    
import os
from src.xml_comparator import XMLComparator    
from src.table_definition import TableDefinition
from src.cds_generator import CDSGenerator
from src.code_integrator import CodeIntegrator 

openai.api_key = "9f32e291dbd248c2b4372647bd937577" #os.getenv("API_KEY")    
openai.api_base = "https://miles-playground.openai.azure.com" #os.getenv("API_BASE")W    
openai.api_type = "azure"    
openai.api_version = "2023-07-01-preview"  

  
st.title("Welcome to CDS Bot ^O^")    
  
# Initialize chat history    
if "messages" not in st.session_state:    
    st.session_state.messages = []    

if "country_code" not in st.session_state:
    st.session_state.country_code = ""

if "country_fields" not in st.session_state:
    st.session_state.country_fields = None

if "cdsGenerator" not in st.session_state:
    st.session_state.cdsGenerator = None
    
    

with st.chat_message("assistant"):    
    st.markdown('Hello! I will help you to generate the CDS views of your country version.')      
  
# Display chat messages from history on app rerun    
for message in st.session_state.messages:    
    with st.chat_message(message["role"]):    
        st.markdown(message["content"])    
  
  
config_dir = 'src/resources/config_fiori2.0'
table_definition_dir = 'src/resources/table_definition'
cds_view_dir = 'src/resources/cds_view'
core_file = f'{config_dir}/HRPAO_DTL_FORM_IT0021_XX.xml'   
   
        
# Accept user input      
if user_input := st.chat_input("Enter your request here:"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})  
            
    # Display user message in chat message container    
    if st.session_state.country_code == "":
        st.session_state.country_code = user_input.upper()
        country_code = st.session_state.country_code   
        
        xmlComparator = XMLComparator(core_file, f'{config_dir}/HRPAO_DTL_FORM_IT0021_{country_code.upper()}.xml' )    
        country_delta_fields = xmlComparator.get_country_delta_fields()
        core_delta_fields = xmlComparator.get_core_delta_fields()
        common_fields = xmlComparator.get_common_fields()
        
        country_fields = xmlComparator.get_country_fields()
        st.session_state.country_fields = country_fields
      
        content = f"""
            **common fields in both core and country version:**\n
            {common_fields}\n
            **country specific fields:**\n
            {country_delta_fields}\n
            **core fields missing in configuration:**\n
            {core_delta_fields}
            """ 
        with st.chat_message("assistant"):
            st.markdown(content)
        st.session_state.messages.append({"role": "assistant", "content": content})    
 
    else:
        country_code = st.session_state.country_code
        if st.session_state.cdsGenerator == None:     
            if country_code.upper() == 'SG': 
                src_tab_name = "p0412"
            elif country_code.upper() == 'BR':
                src_tab_name = "p0397"
            else:
                src_tab_name = "pa0106"
            table_def = TableDefinition(f'{table_definition_dir}/{src_tab_name}.txt')
            field_descriptions = table_def.get_descriptions(st.session_state.country_fields)  
            st.session_state.cdsGenerator = CDSGenerator(country_code, src_tab_name, field_descriptions, openai)  
        cdsGenerator = st.session_state.cdsGenerator
            
        if("nam" in user_input or "NAM" in user_input or "field" in user_input or "FIELD" in user_input):
            cds_fields = cdsGenerator.get_cds_fields()
            content = f"""
                **cds field names generated following global field naming convensions:**\n
                {cds_fields}\n
                """
            with st.chat_message("assistant"):
                st.markdown(content)
            st.session_state.messages.append({"role": "assistant", "content": content})    
            
 
        elif("view" in user_input or "VIEW" in user_input):
            cds_view_code = cdsGenerator.generate_cds_code_familyMemberSupplement()
            output_filepath_supplement = f'{cds_view_dir}/{country_code.lower()}/I_{country_code.upper()}_HCMFamilyMemberSupplement'
            codeIntegrator = CodeIntegrator(output_filepath_supplement)  
            codeIntegrator.createFile(cds_view_code)    
            
            cds_view_code = cdsGenerator.generate_cds_code_familyMemberTP()
            output_filepath_familyMemberTP = f'{cds_view_dir}/{country_code.lower()}/I_{country_code.upper()}_HCMFamilyMemberTP'
            codeIntegrator = CodeIntegrator(output_filepath_familyMemberTP)  
            codeIntegrator.createFile(cds_view_code)    
            
            content = f"""
                **cds view generated in:**\n
                {output_filepath_supplement}\n
                **cds view generated in:**\n
                {output_filepath_familyMemberTP}
                """
            with st.chat_message("assistant"):
                st.markdown(content)
                st.session_state.messages.append({"role": "assistant", "content": content})    
     
        else:
            pass
           
            
           
        
    
