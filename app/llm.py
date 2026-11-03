import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

# Загружаем .env
load_dotenv(Path(__file__).parent.parent / ".env")

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-dummy"))
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"

SYSTEM_PROMPT = """Ты — профессиональный контент-менеджер B2B-интернет-магазина измерительных приборов.
Твоя задача — на основе предоставленных данных сгенерировать черновик карточки товара.

ЖЁСТКИЕ ПРАВИЛА:
1. НЕ ВЫДУМЫВАЙ характеристики. Если данных нет — пиши "данных нет".
2. Используй только те технические значения, которые есть во входных данных.
3. Ответ должен быть строго в формате JSON.

ФОРМАТ ОТВЕТА:
{
  "seo_title": "SEO-заголовок до 70 символов",
  "seo_description": "SEO-описание 800-1200 символов",
  "key_features": ["характеристика 1", "характеристика 2", ...],
  "search_queries": ["запрос 1", "запрос 2", "запрос 3", "запрос 4", "запрос 5"],
  "commercial_block": "Краткий блок для менеджера: кому подходит, какие задачи решает",
  "missing_data": ["поле 1", "поле 2"]
}
"""


async def generate_product_card(product_data: dict) -> dict:
    if USE_MOCK:
        return {
            "seo_title": f"{product_data['name']} — купить в B2B-магазине",
            "seo_description": f"Купите {product_data['name']} от {product_data['manufacturer']}. Характеристики: {', '.join(product_data.get('specs', {}).keys())}.",
            "key_features": [f"{k}: {v}" for k, v in product_data.get("specs", {}).items()],
            "search_queries": [product_data["name"], f"{product_data['name']} купить", f"{product_data['manufacturer']} {product_data['name']}"],
            "commercial_block": f"Подходит для задач, связанных с {product_data['name']}.",
            "missing_data": ["данных нет"]
        }

    user_prompt = f"""Данные о товаре:
{json.dumps(product_data, ensure_ascii=False, indent=2)}

Сгенерируй черновик карточки товара строго в формате JSON."""

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )

    raw = response.choices[0].message.content

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"LLM вернул невалидный JSON: {raw}")