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


  
core_file = f'src/resources/HRESS_CC_PER_DTL_FAMILY_XX.xml'   
  
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
src_tab_name = "pa0106"
  
# Check if the user has entered a country code
if country_code:  
    # Display user message in chat message container    
    with st.chat_message("user"):    
        st.markdown(country_code)    
  
    st.session_state.messages.append({"role": "user", "content": country_code})  
  
    xmlComparator = XMLComparator(core_file, f'src/resources/HRESS_CC_PER_DTL_FAMILY_{country_code.upper()}.xml' )    
    country_delta_fields = xmlComparator.get_country_delta_fields()
    core_delta_fields = xmlComparator.get_core_delta_fields()
      
    if country_code.upper() == 'SG': 
        src_tab_name = "p0412"
    else:
        src_tab_name = "pa0106"
    table_def = TableDefinition(f'src/resources/{src_tab_name}.txt')
        
    field_name_descriptions = table_def.get_descriptions(country_delta_fields)  
    
    cdsGenerator = CDSGenerator(openai)  
    cds_field_names = cdsGenerator.generate_cds_name(field_name_descriptions)  
    
     
    cds_code = cdsGenerator.generate_cds_code(country_code, cds_field_names, src_tab_name)
    output_filepath = os.path.join(os.getcwd(), 'src\\resources\\cdsViews\\sg\\I_SG_HCMFamilyMemberSupplement')  
    codeIntegrator = CodeIntegrator(output_filepath)  
    codeIntegrator.createFile(cds_code)  

    # Add the comparison result to the chat history 
    st.session_state.messages.append({"role": "assistant", "content": "country_delta_fields with proposed cds field names"})  
    for key, value in cds_field_names.items():    
        st.session_state.messages.append({"role": "assistant", "content": f"{key}: {value}"})    
    st.session_state.messages.append({"role": "assistant", "content": f"core delta fields:\n {str(core_delta_fields)}"})    
    st.session_state.messages.append({"role": "assistant", "content": f"cds code generated:\n {cds_code}"})    

    
    # Display the comparison result in a chat message container    
    with st.chat_message("assistant"):   
        # st.markdown("country_delta_fields with proposed cds field names:") 
        # for key, value in cds_field_names.items():  
        #     st.markdown(f"{key}: {value}") 
        st.markdown("core delta fields missing in country configuration:")
        st.markdown(str(core_delta_fields))
        st.markdown("cds code generated:")
        st.markdown(cds_code)
        