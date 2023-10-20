from dataclasses import dataclass

@dataclass
class FieldDescription:
    field_description: str


@dataclass
class FamilyMemberSupplement:
    country_code: str
    field_name_description: str
    source_table_name: str
   
   
@dataclass
class FamilyMemberTP:
    country_code: str
    field_name_description: str  
    
    
@dataclass
class FamilyMemberRootTP:
    country_code: str
    




