import os
from typing import Optional

from openai import OpenAI


class LLM_config:
    api_key = os.getenv("LLM_MODEL_API_KEY")
    model = "deepseek-chat"
    base_url = "https://api.deepseek.com"
    temperature = 0


def get_llm_answer(input_prompt: str, system_prompt: str) -> Optional[str]:
    """
    Function gets response from LLM
    :param input_prompt: custom input prompt
    :param system_prompt: instruction or context for LLM
    :return answer
    """
    try:
        client = OpenAI(api_key=LLM_config.api_key, base_url=LLM_config.base_url)
        response = client.chat.completions.create(
            model=LLM_config.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_prompt},
            ],
            stream=False,
            temperature=LLM_config.temperature,
            response_format={"type": "json_object"},
        )
        response = response.choices[0].message.content
        return response
    except Exception as e:
        return None
