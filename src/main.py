from src.core.code_processor import CodeProcessor
from src.services.ai_service import AIService
from src.ui.app import App

def main():
    """Main entry point for the application."""
    # Initialize services
    ai_service = AIService()
    code_processor = CodeProcessor(ai_service)
    
    # Create and launch the app
    app = App(code_processor)
    app.launch()

if __name__ == "__main__":
    main() 