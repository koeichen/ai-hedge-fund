# src/utils/llm.py

import json
from typing import TypeVar, Type, Optional, Any
from pydantic import BaseModel
# from src.llm.models import get_model, get_model_info # 在仅收集 prompt 时注释掉
from src.utils.progress import progress
# import sys # 不再需要 sys 来退出程序
from datetime import datetime

T = TypeVar("T", bound=BaseModel)

PROMPT_LOG_FILE = "output_prompt.txt"

# class ManualInterventionRequired(Exception): # 不再需要这个异常
#     """自定义异常，用于暂停程序执行以进行手动干预。"""
#     pass

def call_llm(
    prompt: Any,
    model_name: str,
    model_provider: str,
    pydantic_model: Type[T],
    agent_name: Optional[str] = None,
    max_retries: int = 1,  # 确保不重试
    default_factory=None,
) -> T:
    """
    修改后的函数：打印 prompt，将其写入文件，并返回默认数据，不实际调用 LLM。
    程序将继续运行。
    """
    prompt_string = ""
    if hasattr(prompt, 'to_string'):
        prompt_string = prompt.to_string()
    elif hasattr(prompt, 'messages'):
        formatted_messages = []
        for msg in prompt.messages:
            formatted_messages.append(f"  Role: {msg.type}\n  Content: {msg.content}\n")
        prompt_string = "\n".join(formatted_messages)
    else:
        prompt_string = str(prompt)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_header = f"--- PROMPT for Agent: {agent_name} at {current_time} (Model: {model_name}, Provider: {model_provider}) ---"
    log_footer = f"--- END PROMPT for Agent: {agent_name} ---\n\n"
    
    print(log_header)
    print(prompt_string)
    print(f"--- Pydantic Model Expected: {pydantic_model.__name__} ---")
    print(log_footer.strip())

    try:
        with open(PROMPT_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_header + "\n")
            f.write(prompt_string + "\n")
            f.write(f"--- Pydantic Model Expected: {pydantic_model.__name__} ---\n")
            f.write(log_footer)
        print(f"--- Prompt successfully written to {PROMPT_LOG_FILE} ---")
    except Exception as e:
        print(f"--- Error writing prompt to file: {e} ---")
    
    if agent_name:
        # 更新状态，表明 prompt 已生成，但 LLM 调用被跳过
        progress.update_status(agent_name, None, f"Prompt generated and logged. LLM call bypassed.")

    # --- 核心修改：不再抛出异常，而是返回默认值 ---
    print(f"--- Bypassing LLM call for {agent_name}. Returning default response. ---")
    if default_factory:
        return default_factory()
    return create_default_response(pydantic_model) # 确保 create_default_response 定义正确


def create_default_response(model_class: Type[T]) -> T:
    """Creates a safe default response based on the model's fields."""
    default_values = {}
    # 确保为所有 Pydantic 模型字段提供合理的默认值，以允许程序流程继续
    # 特别注意那些嵌套的 Pydantic 模型或影响后续 Agent 逻辑的字段
    for field_name, field_info in model_class.model_fields.items():
        field_type = field_info.annotation
        
        if field_name == "signal": # 针对 AnalystSignal 和类似模型
            default_values[field_name] = "neutral"
        elif field_name == "confidence": # 针对 AnalystSignal 和类似模型
            default_values[field_name] = 0.0
        elif field_name == "reasoning": # 针对 AnalystSignal 和类似模型
            default_values[field_name] = "LLM call bypassed; using default data logged to file."
        elif field_name == "action": # 针对 PortfolioDecision
            default_values[field_name] = "hold"
        elif field_name == "quantity": # 针对 PortfolioDecision
            default_values[field_name] = 0
        elif field_name == "decisions" and hasattr(model_class, 'decisions') : # 针对 PortfolioManagerOutput
            # PortfolioManagerOutput 的 'decisions' 字段是一个字典，键是 ticker，值是 PortfolioDecision
            # 我们需要确保它是一个空字典，而不是 None
            default_values[field_name] = {}
        elif field_type == str:
            default_values[field_name] = "Default String Value"
        elif field_type == float:
            default_values[field_name] = 0.0
        elif field_type == int:
            default_values[field_name] = 0
        elif field_type == bool:
            default_values[field_name] = False
        elif hasattr(field_type, "__origin__") and field_type.__origin__ == list:
            default_values[field_name] = []
        elif hasattr(field_type, "__origin__") and field_type.__origin__ == dict:
            default_values[field_name] = {}
        else:
            try:
                # 尝试处理 Literal 类型或其他带有 __args__ 的类型
                if hasattr(field_type, "__args__") and field_type.__args__:
                    default_values[field_name] = field_type.__args__[0]
                else:
                    default_values[field_name] = None # 最后手段
            except:
                default_values[field_name] = None
    
    try:
        return model_class(**default_values)
    except Exception as e:
        print(f"Error creating default response for {model_class.__name__} with values {default_values}: {e}")
        # 如果创建失败，可能需要更通用的处理，或者让它失败以暴露问题
        # 为了收集 prompt，我们这里可以尝试返回一个空的模型实例，但这可能导致后续问题
        # 或者，如果有一个已知的简单模型（如只包含字符串的），可以返回它
        # 最安全的做法是确保 default_values 总是能成功实例化 model_class
        # 这里我们还是尝试实例化，如果失败，异常会被外层捕获（如果外层有捕获的话）
        raise e # 或者返回一个预先定义的、非常简单的 Pydantic 模型实例

def extract_json_from_response(content: str) -> Optional[dict]:
    """Extracts JSON from markdown-formatted response."""
    # 这个函数在当前模式下不会被调用，因为我们不处理 LLM 的真实响应
    try:
        json_start = content.find("```json")
        if json_start != -1:
            json_text = content[json_start + 7 :]
            json_end = json_text.find("```")
            if json_end != -1:
                json_text = json_text[:json_end].strip()
                return json.loads(json_text)
    except Exception as e:
        print(f"Error extracting JSON from response: {e}")
    return None