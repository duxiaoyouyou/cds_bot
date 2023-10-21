from dataclasses import dataclass

@dataclass
class FieldDescription:
    field_description: str
    field_name_description: dict

@dataclass
class FamilyMemberSupplement:
    country_code: str
    cds_fields: str 
    source_table_name: str
   
   
@dataclass
class FamilyMemberTP:
    country_code: str
    additional_data_fields: str 
    
    
@dataclass
class FamilyMemberRootTP:
    country_code: str
    
    
@dataclass
class Behavior:
    country_code: str

    




