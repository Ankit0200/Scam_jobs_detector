from pydantic import BaseModel,HttpUrl
class JobLink(BaseModel):
    url: HttpUrl
class jobdescription(BaseModel):
    description: str
