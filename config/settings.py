from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    qdrant_host: str
    qdrant_port: int

    class Config:
        env_file = ".env"


settings = Settings() 

ALLOWED_TYPES = {                                                              
    "application/pdf",                                                         
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    # .docx                                                                       
                                                                               
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",  
    #.pptx 

      "text/html",                                                               
      "text/plain",                                                      
      "image/png",
      "image/jpeg",
      "image/tiff",                                                              
      "image/bmp",
  }                                                                              
                                                                               
DOCLING_ALLOWED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                                                                 
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
      "text/html",                                                               
      "image/png",                                                             
      "image/jpeg",
      "image/tiff",
      "image/bmp",                                                               
  }