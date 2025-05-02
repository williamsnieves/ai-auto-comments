import gradio as gr
from lib.models import Language, CodeInput
from lib.ai_service import AIService
import pygments
from pygments.lexers import get_lexer_by_name, guess_lexer
import re

ai_service = AIService()

def detect_language(code: str) -> str:
    """Detect the programming language of the input code."""
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

def process_code(code: str, language: str, context: str = "") -> tuple[str, str]:
    """Process the input code and return the commented version with explanation."""
    try:
        # Detect language if not provided
        if not language:
            language = detect_language(code)
            
        input_data = CodeInput(
            code=code,
            language=Language(language.lower()),
            context=context if context else None
        )
        result = ai_service.generate_comments(input_data)
        
        # Clean up the response to remove any HTML formatting
        cleaned_code = re.sub(r'<[^>]+>', '', result.commented_code)
        cleaned_code = re.sub(r'&[^;]+;', '', cleaned_code)
        
        return cleaned_code, result.explanation
    except Exception as e:
        return f"Error: {str(e)}", ""

# Create the Gradio interface
with gr.Blocks(title="AI Code Comment Generator", theme=gr.themes.Soft()) as app:
    gr.Markdown("# AI Code Comment Generator")
    gr.Markdown("Automatically generate docstrings and comments for your code in multiple programming languages.")
    
    with gr.Row():
        with gr.Column():
            code_input = gr.Code(
                label="Code",
                language="python",
                lines=10,
                max_lines=20,
                interactive=True
            )
            language = gr.Dropdown(
                choices=[lang.value for lang in Language],
                label="Programming Language",
                value=Language.PYTHON.value,
                interactive=True
            )
            context = gr.Textbox(
                label="Additional Context (Optional)",
                placeholder="Add any additional context about the code...",
                lines=2
            )
            submit_btn = gr.Button("Generate Comments")
        
        with gr.Column():
            commented_code = gr.Code(
                label="Commented Code",
                language="python",
                lines=10,
                max_lines=20,
                interactive=False
            )
            explanation = gr.Textbox(
                label="Explanation",
                lines=3,
                max_lines=5,
                interactive=False
            )
    
    # Add event handler for code input to detect language
    def on_code_change(code):
        if code:
            detected_lang = detect_language(code)
            return gr.Dropdown(value=detected_lang)
        return gr.Dropdown()
    
    code_input.change(
        fn=on_code_change,
        inputs=[code_input],
        outputs=[language]
    )
    
    submit_btn.click(
        fn=process_code,
        inputs=[code_input, language, context],
        outputs=[commented_code, explanation]
    )

if __name__ == "__main__":
    app.launch() 