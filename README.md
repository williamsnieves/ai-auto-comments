# AI Code Comment Generator

An AI-powered tool that automatically generates docstrings and comments for code snippets across multiple programming languages.

## Supported Languages
- TypeScript/JavaScript
- Python
- Go
- Kotlin
- Swift
- Java
- C#

## Features
- Automatic docstring generation
- Code explanation through comments
- Support for multiple programming languages
- User-friendly Gradio interface
- Type-safe implementation

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Set up your OpenAI API key in a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

2. Run the application:
```bash
python src/main.py
```

## Development

The project follows a modular structure:
- `src/`: Main application code
- `tests/`: Unit tests
- `lib/`: External integrations and utilities

## Testing

Run tests with:
```bash
pytest tests/
```