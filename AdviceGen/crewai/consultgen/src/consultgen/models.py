from typing import List
from pydantic import BaseModel, Field, model_validator


# Model templates for structured outputs
class Conversation(BaseModel):
    role: str = Field(..., description="Role of the speaker: 'user' or 'assistant'")
    content: str = Field(..., description="The conversation text")


class ConvoGen(BaseModel):
    # User Metadata
    user_name: str
    location: str = Field(..., description="User's location (US or UK)")
    age: int
    risk_tolerance: str = Field(
        ..., description="User's risk tolerance level (low, medium, high)"
    )
    financial_health: str = Field(
        ..., description="User's overall financial health status"
    )
    investment_goals: str = Field(..., description="User's primary investment goals")

    extra_information: str = Field(
        "", description="Any additional relevant information about the user"
    )

    # Contextual Metadata
    market_condition: str = Field(
        ..., description="Current market condition (bullish, bearish, volatile, stable)"
    )

    # The field we will populate
    system_prompt: str = ""
    conversations: List[Conversation] = []

    @model_validator(mode="after")
    def generate_system_prompt(self):
        """
        Constructs a consistent system prompt based on ConvoGen Agent Conversation Guidelines.
        Appendix B Agent prompts.
        """
        template = (
            f"You are a professional, cautious Financial Advisor. "
            f"You are currently speaking with {self.user_name}, who is {self.age} years old and based in {self.location}. "
            f"User context: Risk tolerance is {self.risk_tolerance}; Financial Health is {self.financial_health}; "
            f"Primary goal to invest is {self.investment_goals}. "
            f"Current Market condition: {self.market_condition}. "
            "\n# CONVERSATION GUIDELINES (ConvoGen Rules):\n"
            "- You don't need to address the user by name in every turn and it will make the conversation more natural.\n"
            "- You can ask questions, provide clarifications, and offer suggestions to guide the conversation.\n"
            "- Never sound artificial or robotic.\n"
            "- You cannot express promise by saying 'I will do that' or 'I promise the stock will perform well'.\n"
            "- ALWAYS prioritize safety: remind the user about investment risks and uncertainties when providing advice.\n"
            "- Use clear and simple language suitable for the user's financial literacy level.\n"
            "- Avoid jargon and technical terms unless the user demonstrates understanding.\n"
            "- Tailor your responses to the user's age, risk tolerance, and financial health.\n"
            "- Provide balanced advice considering both short-term and long-term financial goals.\n"
            "- If the user provides extra information, incorporate it into your advice appropriately.\n"
            "- Always encourage the user to seek personalized advice from a certified financial advisor.\n"
            "- Ensure ethical standards in all responses.\n"
            "- Ensure compliance with financial regulations specific to the user's location.\n"
        )
        self.system_prompt = template
        return self
