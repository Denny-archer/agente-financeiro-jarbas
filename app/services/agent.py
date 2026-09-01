from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.prompts.system_prompt import JARBAS_SYSTEM_PROMPT


def perguntar_ao_agente(pergunta: str, contexto: str) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": JARBAS_SYSTEM_PROMPT},
            {"role": "system", "content": f"Dados disponíveis:\n{contexto}"},
            {"role": "user", "content": pergunta},
        ],
        temperature=0.3,
    )
    return resposta.choices[0].message.content
