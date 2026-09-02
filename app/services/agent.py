from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.prompts.system_prompt import JARBAS_SYSTEM_PROMPT


class AgenteError(Exception):
    """Exceção base para erros do agente."""


class AgenteConfigError(AgenteError):
    """Chave de API ausente ou inválida."""


class AgenteOpenAIError(AgenteError):
    """Erro ao comunicar com a API da OpenAI."""


def perguntar_ao_agente(pergunta: str, contexto: str) -> str:
    if not OPENAI_API_KEY or OPENAI_API_KEY == "coloque_sua_chave_aqui":
        raise AgenteConfigError(
            "OPENAI_API_KEY não configurada. Defina a chave no arquivo .env."
        )

    import openai

    client = OpenAI(api_key=OPENAI_API_KEY)

    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"{JARBAS_SYSTEM_PROMPT}\n\nDados disponíveis:\n{contexto}",
                },
                {"role": "user", "content": pergunta},
            ],
            temperature=0.3,
        )
    except openai.AuthenticationError as exc:
        raise AgenteOpenAIError(
            "Chave de API da OpenAI inválida ou expirada."
        ) from exc
    except openai.RateLimitError as exc:
        raise AgenteOpenAIError(
            "Limite de requisições da OpenAI atingido. Tente novamente em instantes."
        ) from exc
    except openai.APIError as exc:
        raise AgenteOpenAIError(
            f"Falha ao contactar a OpenAI: {exc}"
        ) from exc

    return resposta.choices[0].message.content
