"""Helper functions for LLM"""

import json
import os
import traceback
from datetime import datetime
from pydantic import BaseModel
from src.llm.models import get_model, get_model_info
from src.utils.progress import progress
from src.graph.state import AgentState


def _hack_llm_call(prompt: any, pydantic_model: type[BaseModel], agent_name: str | None = None, model_name: str = None, model_provider: str = None) -> BaseModel:
    """Hack function to intercept LLM calls and print prompts without making actual API calls."""
    
    # Create outputs directory if it doesn't exist
    outputs_dir = "./outputs"
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Extract ticker from prompt content
    ticker = "unknown"
    if hasattr(prompt, "messages"):
        for message in prompt.messages:
            if hasattr(message, 'content') and message.content:
                content = message.content
                # Look for ticker in the content
                if "Analyze this investment opportunity for" in content:
                    # Extract ticker after "for"
                    start_idx = content.find("Analyze this investment opportunity for")
                    if start_idx != -1:
                        ticker_start = content.find("for", start_idx) + 4
                        ticker_end = content.find(":", ticker_start)
                        if ticker_end != -1:
                            ticker = content[ticker_start:ticker_end].strip()
                elif "Ticker:" in content:
                    # Extract ticker after "Ticker:"
                    start_idx = content.find("Ticker:")
                    if start_idx != -1:
                        ticker_start = start_idx + 7
                        ticker_end = content.find("\n", ticker_start)
                        if ticker_end != -1:
                            ticker = content[ticker_start:ticker_end].strip()
                elif '"' in content and ':' in content:
                    # Look for JSON format tickers like "BRK.B": { ... }
                    try:
                        # Find the first quoted string that looks like a ticker
                        lines = content.split('\n')
                        tickers_found = []
                        for line in lines:
                            line = line.strip()
                            if line.startswith('"') and '":' in line:
                                # Extract ticker from "TICKER": format
                                ticker_start = line.find('"') + 1
                                ticker_end = line.find('":')
                                if ticker_end != -1:
                                    potential_ticker = line[ticker_start:ticker_end].strip()
                                    # Validate it looks like a ticker (alphanumeric + dots)
                                    if potential_ticker.replace('.', '').replace('-', '').isalnum():
                                        tickers_found.append(potential_ticker)
                        
                        # Use the first ticker found, or combine multiple tickers
                        if tickers_found:
                            if len(tickers_found) == 1:
                                ticker = tickers_found[0]
                            else:
                                # For multiple tickers, use the first one with a prefix
                                ticker = f"multi_{tickers_found[0]}"
                    except:
                        pass
    
    # Debug: Print ticker extraction info
    print(f"🔍 Ticker extraction: found '{ticker}' from prompt")
    
    # Generate timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    agent_safe_name = (agent_name or "unknown").replace("/", "_").replace("\\", "_")
    ticker_safe = ticker.replace("/", "_").replace("\\", "_")
    filename = f"llm_call_{ticker_safe}_{agent_safe_name}_{timestamp}.txt"
    filepath = os.path.join(outputs_dir, filename)
    
    # Get call stack to identify the calling agent
    stack_trace = traceback.extract_stack()
    calling_agent = "Unknown"
    
    # Look for the calling agent in the stack trace
    for frame in stack_trace:
        filename = frame.filename
        if "agents" in filename and filename.endswith(".py"):
            # Extract agent name from file path
            agent_file = os.path.basename(filename)
            calling_agent = agent_file.replace(".py", "")
            break
        elif "portfolio_manager" in filename:
            calling_agent = "portfolio_manager"
            break
        elif "risk_manager" in filename:
            calling_agent = "risk_manager"
            break
    
    # Prepare content for both console and file
    console_output = []
    file_content = []
    
    # Header
    header = "=" * 80
    console_output.append(header)
    file_content.append(header)
    
    # Call info
    call_info = f"LLM CALL INTERCEPTED - Agent: {agent_name or 'Unknown'}"
    console_output.append(call_info)
    file_content.append(call_info)
    
    calling_info = f"CALLING AGENT: {calling_agent}"
    console_output.append(calling_info)
    file_content.append(calling_info)
    
    ticker_info = f"TICKER: {ticker}"
    console_output.append(ticker_info)
    file_content.append(ticker_info)
    
    model_info = f"Model: {model_name} ({model_provider})"
    console_output.append(model_info)
    file_content.append(model_info)
    
    pydantic_info = f"Pydantic Model: {pydantic_model.__name__}"
    console_output.append(pydantic_info)
    file_content.append(pydantic_info)
    
    console_output.append(header)
    file_content.append(header)
    
    # Prompt content
    if hasattr(prompt, "messages"):
        prompt_title = "PROMPT MESSAGES:"
        console_output.append(prompt_title)
        file_content.append(prompt_title)
        
        # Combine all messages into one content
        combined_content = ""
        for i, message in enumerate(prompt.messages):
            if hasattr(message, 'content') and message.content:
                if combined_content:
                    combined_content += " "  # Add space between messages
                combined_content += message.content.strip()
        
        # Display combined content
        console_output.append("  Combined Content:")
        file_content.append("  Combined Content:")
        
        content_lines = combined_content.split('\n')
        for line in content_lines:
            formatted_line = f"    {line}"
            console_output.append(formatted_line)
            file_content.append(formatted_line)
        
        console_output.append("")
        file_content.append("")
            
    elif hasattr(prompt, "content"):
        prompt_title = "PROMPT CONTENT:"
        console_output.append(prompt_title)
        file_content.append(prompt_title)
        
        prompt_content = f"    {prompt.content}"
        console_output.append(prompt_content)
        file_content.append(prompt_content)
        console_output.append("")
        file_content.append("")
        
    else:
        prompt_title = "PROMPT (raw):"
        console_output.append(prompt_title)
        file_content.append(prompt_title)
        
        prompt_raw = f"    {prompt}"
        console_output.append(prompt_raw)
        file_content.append(prompt_raw)
        console_output.append("")
        file_content.append("")
    
    # Footer
    console_output.append(header)
    file_content.append(header)
    
    skip_info = "LLM CALL SKIPPED - Returning default response"
    console_output.append(skip_info)
    file_content.append(skip_info)
    
    console_output.append(header)
    file_content.append(header)
    console_output.append("")
    file_content.append("")
    
    # Print to console
    for line in console_output:
        print(line)
    
    # Save to file
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(file_content))
        print(f"📁 LLM call content saved to: {filepath}")
    except Exception as e:
        print(f"❌ Failed to save to file: {e}")

    return create_default_response(pydantic_model)


def call_llm(
    prompt: any,
    pydantic_model: type[BaseModel],
    agent_name: str | None = None,
    state: AgentState | None = None,
    max_retries: int = 3,
    default_factory=None,
) -> BaseModel:
    """
    Makes an LLM call with retry logic, handling both JSON supported and non-JSON supported models.

    Args:
        prompt: The prompt to send to the LLM
        pydantic_model: The Pydantic model class to structure the output
        agent_name: Optional name of the agent for progress updates and model config extraction
        state: Optional state object to extract agent-specific model configuration
        max_retries: Maximum number of retries (default: 3)
        default_factory: Optional factory function to create default response on failure

    Returns:
        An instance of the specified Pydantic model
    """

    # Extract model configuration if state is provided and agent_name is available
    if state and agent_name:
        model_name, model_provider = get_agent_model_config(state, agent_name)
    else:
        # Use system defaults when no state or agent_name is provided
        model_name = "gpt-4.1"
        model_provider = "OPENAI"

    # HACK: Uncomment the next line to enable prompt interception
    return _hack_llm_call(prompt, pydantic_model, agent_name, model_name, model_provider)

    model_info = get_model_info(model_name, model_provider)
    llm = get_model(model_name, model_provider, api_keys)

    # For non-JSON support models, we can use structured output
    if not (model_info and not model_info.has_json_mode()):
        llm = llm.with_structured_output(
            pydantic_model,
            method="json_mode",
        )

    # Call the LLM with retries
    for attempt in range(max_retries):
        try:
            # Call the LLM
            result = llm.invoke(prompt)

            # For non-JSON support models, we need to extract and parse the JSON manually
            if model_info and not model_info.has_json_mode():
                parsed_result = extract_json_from_response(result.content)
                if parsed_result:
                    return pydantic_model(**parsed_result)
            else:
                return result

        except Exception as e:
            if agent_name:
                progress.update_status(agent_name, None, f"Error - retry {attempt + 1}/{max_retries}")

            if attempt == max_retries - 1:
                print(f"Error in LLM call after {max_retries} attempts: {e}")
                # Use default_factory if provided, otherwise create a basic default
                if default_factory:
                    return default_factory()
                return create_default_response(pydantic_model)

    # This should never be reached due to the retry logic above
    return create_default_response(pydantic_model)


def create_default_response(model_class: type[BaseModel]) -> BaseModel:
    """Creates a safe default response based on the model's fields."""
    default_values = {}
    for field_name, field in model_class.model_fields.items():
        if field.annotation == str:
            default_values[field_name] = "Error in analysis, using default"
        elif field.annotation == float:
            default_values[field_name] = 0.0
        elif field.annotation == int:
            default_values[field_name] = 0
        elif hasattr(field.annotation, "__origin__") and field.annotation.__origin__ == dict:
            default_values[field_name] = {}
        else:
            # For other types (like Literal), try to use the first allowed value
            if hasattr(field.annotation, "__args__"):
                default_values[field_name] = field.annotation.__args__[0]
            else:
                default_values[field_name] = None

    return model_class(**default_values)


def extract_json_from_response(content: str) -> dict | None:
    """Extracts JSON from markdown-formatted response."""
    try:
        json_start = content.find("```json")
        if json_start != -1:
            json_text = content[json_start + 7 :]  # Skip past ```json
            json_end = json_text.find("```")
            if json_end != -1:
                json_text = json_text[:json_end].strip()
                return json.loads(json_text)
    except Exception as e:
        print(f"Error extracting JSON from response: {e}")
    return None


def get_agent_model_config(state, agent_name):
    """
    Get model configuration for a specific agent from the state.
    Falls back to global model configuration if agent-specific config is not available.
    Always returns valid model_name and model_provider values.
    """
    request = state.get("metadata", {}).get("request")
    
    if request and hasattr(request, 'get_agent_model_config'):
        # Get agent-specific model configuration
        model_name, model_provider = request.get_agent_model_config(agent_name)
        # Ensure we have valid values
        if model_name and model_provider:
            return model_name, model_provider.value if hasattr(model_provider, 'value') else str(model_provider)
    
    # Fall back to global configuration (system defaults)
    model_name = state.get("metadata", {}).get("model_name") or "gpt-4.1"
    model_provider = state.get("metadata", {}).get("model_provider") or "OPENAI"
    
    # Convert enum to string if necessary
    if hasattr(model_provider, 'value'):
        model_provider = model_provider.value

    return model_name, model_provider
