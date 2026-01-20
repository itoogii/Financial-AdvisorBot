from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# Defined models for structured data below
class Persona(BaseModel):
    username: str = Field(description="username of the persona")
    full_name: str = Field(description="full name of the persona")
    age: int = Field(description="age of the persona")
    occupation: str = Field(description="occupation of the persona")
    goals: List[str] = Field(description="goals of the persona")
    challenges: List[str] = Field(description="challenges faced by the persona")
    gender: str = Field(description="gender of the persona")
    location: str = Field(description="location of the persona in US or UK")
    marital_status: str = Field(description="marital status of the persona")
    interests: List[str] = Field(description="interests and hobbies of the persona")
    speech_style: str = Field(description="speech style of the persona")
    financial_background: str = Field(description="financial background of the persona and financial literacy level, experience with investing")
    attitude: str = Field(description="attitude towards money and investing of the persona")
    qualities: str = Field(description="personal qualities summarizing their character and persona's attitude. Avoid getting too witty, as doing so may taint the persona as being too fun and not a useful tool")
    risk_tolerance: str = Field(description="investment risk tolerance level of the persona")
    extra_info: Optional[Dict[str, str]] = Field(description="any extra useful information about the persona, or memory of past experiences with financial advisors and investing")
    image_prompt: str = Field(description="prompt to generate an image representing the persona")

class PersonaList(BaseModel):
    personas: List[Persona] = Field(description="List of user personas")

class Scenario(BaseModel):
    persona: Persona = Field(description="Persona used in the scenario")
    title: str = Field(description="Title of the scenario")
    introduction: str = Field(description="Introduction to the topic")
    description: str = Field(description="Detailed description of the scenario")
    context: List[Persona] = Field(description="Topic context to trigger the discussion with the financial advisor")
    history: Optional[str] = Field(description="previous conversation history with the financial advisor if any")
    persona_mood: str = Field(description="current mood of the persona")

class ScenarioList(BaseModel):
    scenarios: List[Scenario] = Field(description="List of user research scenarios")