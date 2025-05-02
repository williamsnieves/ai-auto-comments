import re
from typing import Tuple
from src.lib.models import CodeInput, Language
from src.services.ai_service import AIService
from src.utils.language_detector import LanguageDetector

class CodeProcessor:
    """Core class for processing code and generating comments."""
    
    def __init__(self, ai_service: AIService):
        """
        Initialize the CodeProcessor.
        
        Args:
            ai_service (AIService): The AI service to use for comment generation
        """
        self.ai_service = ai_service
        self.language_detector = LanguageDetector()
    
    def process_code(self, code: str, language: str, context: str = "") -> tuple[str, str]:
        """
        Process the code and generate comments.
        
        Args:
            code (str): The code to process
            language (str): The programming language
            context (str): Additional context about the code
            
        Returns:
            tuple[str, str]: The commented code and an explanation
        """
        if not code.strip():
            return "", "Please provide some code to process."
        
        try:
            # Convert string language to Language enum
            try:
                lang_enum = Language(language.lower())
            except ValueError:
                return code, f"Invalid language: {language}. Please select a valid language from the dropdown."
            
            return self.ai_service.generate_comments(code, lang_enum, context)
        except Exception as e:
            return code, f"Error processing code: {str(e)}"

class LanguageDetector:
    """Utility class for detecting programming languages."""
    
    def detect_language(self, code: str) -> str:
        """
        Detect the programming language of the given code.
        
        Args:
            code (str): The code to analyze
            
        Returns:
            str: The detected language
        """
        # Simple heuristic-based detection
        if "def " in code or "import " in code:
            return Language.PYTHON.value
        elif "function " in code or "const " in code or "let " in code:
            return Language.JAVASCRIPT.value
        elif "func " in code or "package " in code:
            return Language.GO.value
        elif "class " in code and "{" in code:
            return Language.JAVA.value
        elif "func " in code and "->" in code:
            return Language.SWIFT.value
        elif "fun " in code:
            return Language.KOTLIN.value
        elif "public class " in code:
            return Language.CSHARP.value
        else:
            return Language.PYTHON.value  # Default to Python

    def process_code(self, code: str, language: str, context: str = "") -> Tuple[str, str]:
        """
        Process the input code and return the commented version with explanation.
        
        Args:
            code (str): The code to process
            language (str): The programming language
            context (str, optional): Additional context about the code
            
        Returns:
            Tuple[str, str]: The processed code and explanation
        """
        try:
            # Detect language if not provided
            if not language:
                language = self.detect_language(code)
                
            input_data = CodeInput(
                code=code,
                language=Language(language.lower()),
                context=context if context else None
            )
            result = self.ai_service.generate_comments(input_data)
            
            # Clean up the response to remove any HTML formatting
            cleaned_code = self._clean_code(result.commented_code)
            
            return cleaned_code, result.explanation
        except Exception as e:
            return f"Error: {str(e)}", ""
    
    def _clean_code(self, code: str) -> str:
        """
        Clean the code by removing any HTML formatting.
        
        Args:
            code (str): The code to clean
            
        Returns:
            str: The cleaned code
        """
        # Remove HTML tags
        code = re.sub(r'<[^>]+>', '', code)
        # Remove HTML entities
        code = re.sub(r'&[^;]+;', '', code)
        return code 