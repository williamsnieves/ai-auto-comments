# AI Code Comment Generator

An AI-powered tool that automatically generates docstrings and comments for code snippets in various programming languages.

## Features

- Automatic language detection
- Support for multiple programming languages:
  - Python
  - JavaScript/TypeScript
  - Go
  - Java
  - Kotlin
  - Swift
  - C#
- Multiple AI model support:
  - GPT-4
  - GPT-4 Mini
  - Claude 3.5 Sonnet (coming soon)
- Interactive Gradio interface
- Syntax highlighting
- Customizable context input
- Language-specific documentation conventions

## Demo

[![Demo Video](https://vimeo.com/YOUR_VIDEO_ID)](https://vimeo.com/1080902293)

*Click the image above to watch the demo video*

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-auto-comments.git
cd ai-auto-comments
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Run the application:
```bash
python -m src.main
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://127.0.0.1:7860)

3. In the interface:
   - Select your preferred AI model
   - Paste your code into the input field
   - Select the programming language (or let it auto-detect)
   - Optionally add context about your code
   - Click "Generate Comments" to get the commented version

4. The application will:
   - Analyze your code
   - Add appropriate docstrings and comments
   - Follow language-specific documentation conventions
   - Provide an explanation of the changes made

## Project Structure

```
ai-auto-comments/
├── src/
│   ├── core/
│   │   └── code_processor.py
│   ├── lib/
│   │   └── models.py
│   ├── services/
│   │   └── ai_service.py
│   ├── ui/
│   │   └── app.py
│   ├── config.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.