import os
import openai
from dotenv import load_dotenv
from src.lib.models import Language
from src.config import ModelType, DEFAULT_MODEL, SYSTEM_PROMPTS

# Load environment variables from .env file
load_dotenv()

class AIService:
    """Service for interacting with AI models."""
    
    def __init__(self, model: ModelType = DEFAULT_MODEL):
        """
        Initialize the AI service.
        
        Args:
            model (ModelType): The AI model to use
        """
        self.model = model
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate_comments(self, code: str, language: Language, context: str = "") -> tuple[str, str]:
        """
        Generate comments and docstrings for the given code.
        
        Args:
            code (str): The code to comment
            language (Language): The programming language
            context (str): Additional context about the code
            
        Returns:
            tuple[str, str]: The commented code and an explanation
        """
        prompt = self._create_prompt(code, language, context)
        
        try:
            if self.model == ModelType.CLAUDE_3_5:
                # TODO: Implement Claude API integration
                raise NotImplementedError("Claude API integration not yet implemented")
            
            response = self.client.chat.completions.create(
                model=self.model.value,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPTS[self.model]},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            commented_code, explanation = self._parse_response(result)
            
            return commented_code, explanation
        except Exception as e:
            return code, f"Error generating comments: {str(e)}"
    
    def _create_prompt(self, code: str, language: Language, context: str) -> str:
        """Create the prompt for the AI model."""
        prompt = f"""
        Please add appropriate docstrings and comments to the following {language.value} code.
        
        Code:
        {code}
        
        Additional context:
        {context}
        
        Please provide:
        1. The code with added docstrings and comments
        2. A brief explanation of the changes made
        
        Format your response as:
        CODE:
        [commented code here]
        
        EXPLANATION:
        [explanation here]
        """
        return prompt
    
    def _parse_response(self, response: str) -> tuple[str, str]:
        """Parse the AI model's response into code and explanation."""
        parts = response.split("EXPLANATION:")
        if len(parts) != 2:
            return response, "No explanation provided."
        
        code_part = parts[0].replace("CODE:", "").strip()
        explanation = parts[1].strip()
        
        return code_part, explanation 