# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Para que serve no Jarbas? |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores, ou seja, dar continuidade ao atendimento de forma eficiente. |
| `perfil_investidor.json` | JSON | Personalizar as explicações sobre as dúvidas e necessidades de aprendizado do cliente. |
| `produtos_financeiros.json` | JSON | Conhecer os produtos disponíveis para que eles possam ser ensinados ao cliente. |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente e usar essas informações de forma didática. |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

O produto Fundo Imobiliário (FII) substitui o Fundo Multimercado, pois pessoalmente me sinto mais confiante em usar apenas produtos financeiros que eu conheço. Assim, poderei validar as respostas do Jarbas de forma mais assertiva.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os arquivos CSV/JSON da pasta `data` são carregados no início da sessão e convertidos em estruturas de dados internas — não em busca vetorial, já que são dados tabulares/transacionais, não documentos soltos.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Em vez de injetar a base inteira no prompt, o agente seleciona apenas o recorte relevante para a pergunta do usuário — perfil do investidor, últimas transações ou o produto perguntado — e inclui esse recorte no contexto enviado ao LLM. Isso mantém o prompt enxuto e reduz a superfície para alucinação, reforçando o checklist de Segurança e Anti-Alucinação já definido no README.

---

## Exemplo de Contexto Montado

> Ajuste os nomes de campo abaixo para bater exatamente com as chaves reais dos seus arquivos `perfil_investidor.json` e `transacoes.csv` — o exemplo abaixo é ilustrativo.

```
Perfil do Cliente:
- Nome: João Silva
- Perfil de investidor: Moderado
- Saldo disponível: R$ 5.000
- Produto de interesse: FII (Fundo Imobiliário)

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
- 05/11: Aporte em FII - R$ 300
```