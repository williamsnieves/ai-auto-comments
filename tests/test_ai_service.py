import pytest
from unittest.mock import MagicMock, patch
from src.lib.models import Language, CodeInput, CodeOutput
from src.lib.ai_service import AIService

@pytest.fixture
def mock_openai():
    with patch("openai.OpenAI") as mock:
        yield mock

@pytest.fixture
def ai_service(mock_openai):
    return AIService()

def test_get_language_specific_prompt(ai_service):
    """Test that language-specific prompts are correctly returned."""
    assert "PEP 257" in ai_service._get_language_specific_prompt(Language.PYTHON)
    assert "JSDoc" in ai_service._get_language_specific_prompt(Language.TYPESCRIPT)
    assert "GoDoc" in ai_service._get_language_specific_prompt(Language.GO)

def test_generate_comments(ai_service, mock_openai):
    """Test the comment generation process with a mocked response."""
    # Mock the OpenAI response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content="\"\"\"Example function.\"\"\"\ndef example(): pass\n\nExplanation: Added docstring"
            )
        )
    ]
    ai_service.client.chat.completions.create.return_value = mock_response

    # Create test input
    input_data = CodeInput(
        code="def example(): pass",
        language=Language.PYTHON
    )

    # Call the method
    result = ai_service.generate_comments(input_data)

    # Verify the result
    assert isinstance(result, CodeOutput)
    assert result.original_code == "def example(): pass"
    assert result.commented_code == "\"\"\"Example function.\"\"\"\ndef example(): pass"
    assert result.explanation == "Added docstring"

    # Verify OpenAI was called correctly
    ai_service.client.chat.completions.create.assert_called_once()
    call_args = ai_service.client.chat.completions.create.call_args[1]
    assert "gpt-4-turbo-preview" in call_args["model"]
    assert "system" in call_args["messages"][0]["role"]
    assert "user" in call_args["messages"][1]["role"]
    assert input_data.code in call_args["messages"][1]["content"]

def test_generate_comments_with_context(ai_service, mock_openai):
    """Test comment generation with additional context."""
    # Mock the OpenAI response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content="\"\"\"Example function.\"\"\"\ndef example(): pass\n\nExplanation: Added docstring"
            )
        )
    ]
    ai_service.client.chat.completions.create.return_value = mock_response

    # Create test input with context
    input_data = CodeInput(
        code="def example(): pass",
        language=Language.PYTHON,
        context="This is a test function"
    )

    # Call the method
    result = ai_service.generate_comments(input_data)

    # Verify OpenAI was called with context
    call_args = ai_service.client.chat.completions.create.call_args[1]
    assert "Additional Context" in call_args["messages"][0]["content"]
    assert input_data.context in call_args["messages"][0]["content"] 