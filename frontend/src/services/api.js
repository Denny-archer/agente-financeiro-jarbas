const API_BASE = ''

async function handleResponse(res) {
  if (!res.ok) {
    let detail = res.statusText
    try {
      const body = await res.json()
      detail = body.detail || body.mensagem || JSON.stringify(body)
    } catch (_) {
      // resposta sem JSON
    }
    throw new Error(detail)
  }
  return res.json()
}

export async function cadastrarGasto(gasto) {
  const res = await fetch(`${API_BASE}/gastos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(gasto),
  })
  return handleResponse(res)
}

export async function obterResumo(periodo = 'dia') {
  const res = await fetch(`${API_BASE}/resumo?periodo=${periodo}`)
  return handleResponse(res)
}

export async function obterAlertas() {
  const res = await fetch(`${API_BASE}/alertas`)
  return handleResponse(res)
}

export async function enviarPergunta(pergunta) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pergunta }),
  })
  return handleResponse(res)
}

export async function importarCSV(file) {
  const formData = new FormData()
  formData.append('file', file)
  const res = await fetch(`${API_BASE}/importar`, {
    method: 'POST',
    body: formData,
  })
  return handleResponse(res)
}
