from src.lib.models import Language, CodeInput, CodeOutput

def test_language_enum():
    """Test that the Language enum contains all required languages."""
    expected_languages = {
        "python", "typescript", "javascript", "go",
        "kotlin", "swift", "java", "csharp"
    }
    assert set(lang.value for lang in Language) == expected_languages

def test_code_input_creation():
    """Test the creation of a CodeInput instance."""
    input_data = CodeInput(
        code="def example(): pass",
        language=Language.PYTHON
    )
    assert input_data.code == "def example(): pass"
    assert input_data.language == Language.PYTHON
    assert input_data.context is None

def test_code_input_with_context():
    """Test CodeInput creation with optional context."""
    input_data = CodeInput(
        code="def example(): pass",
        language=Language.PYTHON,
        context="This is a test function"
    )
    assert input_data.context == "This is a test function"

def test_code_output_creation():
    """Test the creation of a CodeOutput instance."""
    output = CodeOutput(
        original_code="def example(): pass",
        commented_code="\"\"\"Example function.\"\"\"\ndef example(): pass",
        explanation="Added docstring to the function"
    )
    assert output.original_code == "def example(): pass"
    assert output.commented_code == "\"\"\"Example function.\"\"\"\ndef example(): pass"
    assert output.explanation == "Added docstring to the function" 