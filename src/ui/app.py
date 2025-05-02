import gradio as gr
from src.lib.models import Language
from src.core.code_processor import CodeProcessor
from src.services.ai_service import AIService
from src.config import ModelType, DEFAULT_MODEL

class App:
    """Main application class that handles the Gradio interface."""
    
    def __init__(self, code_processor: CodeProcessor):
        """
        Initialize the App.
        
        Args:
            code_processor (CodeProcessor): The code processor to use
        """
        self.code_processor = code_processor
        self.app = self._create_interface()
    
    def _create_interface(self) -> gr.Blocks:
        """Create the Gradio interface."""
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
                    model = gr.Dropdown(
                        choices=[model.value for model in ModelType],
                        label="AI Model",
                        value=DEFAULT_MODEL.value,
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
                    detected_lang = self.code_processor.language_detector.detect_language(code)
                    return gr.Dropdown(value=detected_lang)
                return gr.Dropdown()
            
            code_input.change(
                fn=on_code_change,
                inputs=[code_input],
                outputs=[language]
            )
            
            submit_btn.click(
                fn=self.code_processor.process_code,
                inputs=[code_input, language, context],
                outputs=[commented_code, explanation]
            )
        
        return app
    
    def launch(self):
        """Launch the Gradio interface."""
        self.app.launch() 