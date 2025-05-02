from pygments.lexers import guess_lexer
from ..lib.models import Language

class LanguageDetector:
    """Utility class for detecting programming languages from code snippets."""
    
    @staticmethod
    def detect_language(code: str) -> str:
        """
        Detect the programming language of the input code.
        
        Args:
            code (str): The code snippet to analyze
            
        Returns:
            str: The detected language name
        """
        try:
            # Try to guess the lexer based on the code
            lexer = guess_lexer(code)
            # Map common lexer names to our Language enum values
            language_map = {
                'python': 'python',
                'typescript': 'typescript',
                'javascript': 'javascript',
                'go': 'go',
                'kotlin': 'kotlin',
                'swift': 'swift',
                'java': 'java',
                'csharp': 'csharp'
            }
            # Get the base language name
            base_lang = lexer.name.lower()
            # Return the mapped language or default to python
            return language_map.get(base_lang, 'python')
        except:
            return 'python' 