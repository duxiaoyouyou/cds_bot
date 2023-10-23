import openai    
import streamlit as st    
import os
from src.xml_comparator import XMLComparator    
from src.xml_comparator_mock import XMLComparatorMock
from src.table_definition import TableDefinition
from src.cds_generator import CDSGenerator
from src.code_integrator import CodeIntegrator 
import matplotlib.pyplot as plt  
import time
  

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

if "country_delta_fields" not in st.session_state:
    st.session_state.country_delta_fields = None

if "cdsGenerator" not in st.session_state:
    st.session_state.cdsGenerator = None
    
    

with st.chat_message("assistant"):    
    st.markdown('Hello! I will help you to generate the CDS views of your country version. Please enter your country code.')      
  
# Display chat messages from history on app rerun    
for message in st.session_state.messages:    
    with st.chat_message(message["role"]):    
        st.markdown(message["content"])    
  
  
table_definition_dir = "src/resources/table_definition"
cds_view_dir = "src/resources/cds_view"


config_dir = "src/resources/config_fiori2.0" #"src/resources/config_fiori1.0" #
config_prefix = "HRPAO_DTL_FORM_IT0021" #"HRESS_CC_PER_DTL_FAMILY" #
core_suffix = "XX"
core_file = f'{config_dir}/{config_prefix}_{core_suffix}.xml'   


if st.session_state.country_code == "":  
    user_input_prompt = "Enter your country code, which should be a two or three-letter, alphanumeric code:"  
else:  
    user_input_prompt = "Enter your request here:"  
 
        
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
        
        try:  
            xmlComparator = XMLComparatorMock() #XMLComparator(core_file, f'{config_dir}/{config_prefix}_{country_code.upper()}.xml')  
        except FileNotFoundError:  
            with st.chat_message("assistant"):  
                st.markdown('The country code you entered could not be found. Please try again.')  
            st.session_state.messages.append({"role": "assistant", "content": 'The country code you entered could not be found. Please try again.'})  
            st.session_state.country_code = ""  
        else:    
            time.sleep(6)
            # common_fields = xmlComparator.get_common_fields()
            # core_delta_fields = xmlComparator.get_core_delta_fields()
            country_delta_fields = xmlComparator.get_country_delta_fields()
            st.session_state.country_delta_fields = country_delta_fields 
            
            # country_fields = xmlComparator.get_country_fields()
            # st.session_state.country_fields = country_fields    
            
           
            if country_code.upper() == 'SG': 
                st.session_state.src_tab_name = "p0412"
                st.session_state.info_type = "0412"
            elif country_code.upper() == 'BR':
                st.session_state.src_tab_name = "p0397"
                st.session_state.info_type = "0397"
            else:
                st.session_state.src_tab_name = "pa0106"
                st.session_state.info_type = "0106"
            
            table_def = TableDefinition(f'{table_definition_dir}/{st.session_state.src_tab_name}.txt')
            st.session_state.field_descriptions = table_def.get_descriptions(country_delta_fields) 
            field_descriptions = st.session_state.field_descriptions
            
            # lower_case_desc_dict = {k.lower(): v for k, v in st.session_state.field_descriptions.items() if k is not None}    
            # exception_fields =  [key for key in country_fields if key is not None and key.lower() not in lower_case_desc_dict]  
            
            it_ctrl_content = f"""
            PERNR           Personnel Number

            INFTY Infotype

            SUBTY           Subtype

            OBJPS Object Identification

            SPRPS Lock Indicator for HR Master Data Record

            ENDDA          End Date

            BEGDA          Start Date

            SEQNR           Number of Infotype Record With Same Key

            AEDTM          Last Changed On

            UNAME         Name of Person Who Changed Object

            HISTO Historical Record Flag

            ITXEX            Text Exists for Infotype

            REFEX           Reference Fields Exist (Primary/Secondary Costs)

            ORDEX          Confirmation Fields Exist

            ITBLD Infotype Screen Control

            PREAS            Reason for Changing Master Data

            FLAG1            Reserved Field/Unused Field

            FLAG2            Reserved Field/Unused Field

            FLAG3            Reserved Field/Unused Field

            FLAG4            Reserved Field/Unused Field

            RESE1 Reserved Field/Unused Field of Length 2

            RESE2 Reserved Field/Unused Field of Length 2

            GRPVL           Grouping Value for Personnel Assignments
"""
            

            country_specific_content = f"""
            ENAME          Name of employer

            DESGN           Designation

            STRAS            Street and House Number

            LOCAT           2nd Address Line

            ORT01            City

            STATE            Region (State, Province, County)

            PSTLZ Postal Code

            LAND1           Country/Region Key

            TELNR           Telephone Number

            SNAME          School / Hospital

            STRT  Street and House Number

            LOCT  Street and House Number

            TELPH            Telephone Number

            CITY   City

            PSTCD            Postal Code

            LAND Country/Region Key

            LANDX          Name of Country/Region (Short)

            STAT1            Region (State, Province, County)

            PERID Personnel ID Number

            TAXNB          Tax ID

            PMRES           Residency type

            RACKY          Ethnic origin

            SPEMS           Spouse employment status

            PERMO          Modifier for Personnel Identifier

            SPUEM           Shared Parental Leave

            CONFN          Confinement Number

            CLCNO          Child Birth Certificate Number

            CLDTY           Child Type

            FCCSL            CCSL validity for last valid year

            SYCCL           CCL Entitlement (days) in Year of Birth

            SCCLB           CCL Start from Year of Birth

            SPAIM            Is spouse’s annual income more than $4,000

            QTSPL            Number of Shared Parental Leave (days)
            """
            
            content = f"""
            The investigation results are based on the following inputs:\n
            **Essential Inputs:**\n
            P0021: HR Master Record: Infotype 0021 (Family)\n
            P0412: Additional family-related information for SG\n
            HCMT_BSP_PA_SG_R0021: Fiori1&2 Screen Structure for Infotype 0021 for SG\n
            I_HCM_ESSFamilyMemberTP: Fiori3 core entity definition\n
            **Reference Information:**\n
            I_US_HCMFamilyMemberSupplement: Fiori3 US entity definition\n
            HRESS_CC_PER_DTL_FAMILY_SG.xml: Fiori1 XML for SG Family Infotype\n
            HRPAO_FORMREP_IT0021_SG.xml: Fiori2 XML for SG Family Infotype\n
            **Outputs:**\n
            **Infotype control field is identical between SG and standard versions. We don’t need to create these fields as they are already registered.**\n
            {it_ctrl_content}\n
            **Country Specific Fields to be used is as follows:**\n
            {country_specific_content}\n
            **The following fields are not in structure {st.session_state.src_tab_name} but better to include them into CDS-views since they are used in Fiori2 screen and defined in Fiori3 entity.**\n
            FGBOT           Birthplace
            """      
        
            # content = f"""
            #     **common fields in both core and country version:**\n
            #    # {common_fields}\n
            #     **country specific fields:**\n
            #     {country_delta_fields}\n
            #     **core fields missing in country configuration:**\n
            #     {core_delta_fields}\n
            #     **fields in country configuration but missing in source table:**\n
            #     {exception_fields}
            #     """
            
            with st.chat_message("assistant"):
                st.markdown(content)
            st.session_state.messages.append({"role": "assistant", "content": content})    
    
            # field_counts = {
            #     "common_fields": len(common_fields), 
            #     "country_delta_fields": len(country_delta_fields), 
            #     "core_delta_fields": len(core_delta_fields),
            #     "exception_fields": len(exception_fields),
            # }        
            # fig, ax = plt.subplots()  
            # ax.bar(field_counts.keys(), field_counts.values(), width=0.5)        
            # plt.xticks(rotation='horizontal')         
            # plt.xticks(fontsize=8)  
            # plt.yticks(fontsize=8)
            # st.pyplot(fig)

    else:
        country_code = st.session_state.country_code
        src_tab_name = st.session_state.src_tab_name
        info_type = st.session_state.info_type
        field_descriptions = st.session_state.field_descriptions
        
        if st.session_state.cdsGenerator == None:     
            st.session_state.cdsGenerator = CDSGenerator(country_code, src_tab_name, info_type, field_descriptions, openai)  
        cdsGenerator = st.session_state.cdsGenerator
            
        if("nam" in user_input or "NAM" in user_input):
            cds_fields_specific = cdsGenerator.get_cds_fields().replace(",","").replace(".", "")
            cds_fields_specific = f"""{cds_fields_specific}"""
            
            cds_fields_common = f"""
            pernr: HCMPersonnelNumber \n  
            subty: HCMSubtype   \n
            objps: HCMObjectIdentification  \n 
            sprps: HCMRecordIsLocked   \n
            endda: EndDate   \n
            begda: StartDate   \n
            aedtm: LastChangedDate  \n 
            uname: LastChangedByUser   \n
            itxex: HCMInfoTypeRecordHasText \n  
            itbld: HCMInfoTypeRecordScreenCtrl  \n 
            famsa: HCMFamilyMemberTypeCode   \n
            fanam: HCMFamilyMemberLastName   \n
            fgbna: HCMFamilyMemberBirthName   \n
            favor: HCMFamilyMemberFirstName   \n
            finit: HCMFamilyMemberInitials   \n
            fnmzu: HCMFamilyMemberOtherTitleCode   \n
            fana: HCMFamilyMemberNationalityCode   \n
            fana2: HCMFamilyMember2ndNatltyCode   \n
            fana3: HCMFamilyMember3rdNatltyCode   \n
            erbnr: HCMFamMbrRefPersnWorkAgreement  \n 
            fasex: HCMFamilyMemberGenderCode   \n
            fgbot: HCMFamilyMemberPlaceOfBrthName   \n
            fgbld: HCMFamilyMemberCntryOfBrthCode \n
            """
            content = f"""
                **Here is the complete list for SG Family fields for Fiori3 entity. \nFor country specific fields, you will need to register before use. \nI provide the reference fields name based on Fiori3 naming convention for your reference.**\n
                {cds_fields_common}\n
                {cds_fields_specific}\n
                """

            with st.chat_message("assistant"):
                st.markdown(content)
            st.session_state.messages.append({"role": "assistant", "content": content})    
 
        elif("view" in user_input or "VIEW" in user_input):
            cds_view_code = cdsGenerator.generate_cds_code_familyMemberSupplement()
            output_filepath_supplement = f'{cds_view_dir}/{country_code.lower()}/I_{country_code.upper()}_HCMFamilyMemberSupplement'
            codeIntegrator = CodeIntegrator(output_filepath_supplement)  
            codeIntegrator.createFile(cds_view_code)    
            
            cds_view_code = cdsGenerator.generate_cds_code_familyMemberTP(st.session_state.country_delta_fields)
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
           
            
           
        
    
