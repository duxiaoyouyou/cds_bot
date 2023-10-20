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
  
with st.chat_message("assistant"):    
    st.markdown('Hello! I will help you to generate the CDS views of your country version.')      
  
# Display chat messages from history on app rerun    
for message in st.session_state.messages:    
    with st.chat_message(message["role"]):    
        st.markdown(message["content"])    
  
# Accept user input    
country_code = st.chat_input("Enter your country code here:")  
  
config_dir = 'src/resources/config_fiori2.0'
table_definition_dir = 'src/resources/table_definition'
cds_view_dir = 'src/resources/cds_view'

# Check if the user has entered a country code
if country_code:  
    # Display user message in chat message container    
    with st.chat_message("user"):    
        st.markdown(country_code)    
  
    st.session_state.messages.append({"role": "user", "content": country_code})  
  
    
    core_file = f'{config_dir}/HRPAO_DTL_FORM_IT0021_XX.xml'   
    xmlComparator = XMLComparator(core_file, f'{config_dir}/HRPAO_DTL_FORM_IT0021_{country_code.upper()}.xml' )    
    country_delta_fields = xmlComparator.get_country_delta_fields()
    core_delta_fields = xmlComparator.get_core_delta_fields()
    common_fields = xmlComparator.get_common_fields()
      
    if country_code.upper() == 'SG': 
        src_tab_name = "p0412"
    elif country_code.upper() == 'BR':
        src_tab_name = "p0397"
    else:
        src_tab_name = "pa0106"
    table_def = TableDefinition(f'{table_definition_dir}/{src_tab_name}.txt')
        
    field_descriptions = table_def.get_descriptions(country_delta_fields)  
    
    cdsGenerator = CDSGenerator(country_code, src_tab_name, field_descriptions, openai)  
    
    cds_code_supplement = cdsGenerator.generate_cds_code_familyMemberSupplement()
    output_filepath = f'{cds_view_dir}/{country_code.lower()}/I_{country_code.upper()}_HCMFamilyMemberSupplement'
    codeIntegrator = CodeIntegrator(output_filepath)  
    codeIntegrator.createFile(cds_code_supplement)  

    # Add the comparison result to the chat history 
    st.session_state.messages.append({"role": "assistant", "content": f"country specific fields: \n {str(country_delta_fields)}"})  
    st.session_state.messages.append({"role": "assistant", "content": f"core delta fields:\n {str(core_delta_fields)}"})    
    st.session_state.messages.append({"role": "assistant", "content": f"cds view supplement generated:\n {cds_code_supplement}"})    
    
    # Display the comparison result in a chat message container    
    with st.chat_message("assistant"):
        st.markdown("**common fields in core and country version:**")
        st.markdown(str(common_fields))
        st.markdown("**country specific fields:**")
        st.markdown(str(country_delta_fields))
        st.markdown("**core fields missing in configuration:**")
        st.markdown(str(core_delta_fields))
        st.markdown(f"**cds view I_{country_code.upper()}_HCMFamilyMemberSupplement generated:**")
        st.markdown(cds_code_supplement)
        