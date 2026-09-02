import { useState, useRef, useEffect } from 'react'
import { Form, Button, Spinner, Alert } from 'react-bootstrap'
import { enviarPergunta } from '../services/api'

export default function Chat() {
  const [mensagens, setMensagens] = useState([
    { role: 'jarbas', content: 'Olá! Sou o Jarbas. Pergunte sobre seus gastos, resumos ou investimentos. 😊' },
  ])
  const [input, setInput] = useState('')
  const [carregando, setCarregando] = useState(false)
  const [erro, setErro] = useState('')
  const fimRef = useRef(null)

  useEffect(() => {
    fimRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [mensagens, carregando])

  const submit = async (e) => {
    e.preventDefault()
    const pergunta = input.trim()
    if (!pergunta || carregando) return

    setErro('')
    setMensagens((m) => [...m, { role: 'user', content: pergunta }])
    setInput('')
    setCarregando(true)

    try {
      const { resposta } = await enviarPergunta(pergunta)
      setMensagens((m) => [...m, { role: 'jarbas', content: resposta }])
    } catch (err) {
      setErro(err.message)
    } finally {
      setCarregando(false)
    }
  }

  return (
    <>
      <h1 className="mb-4">Conversar com o Jarbas</h1>

      {erro && <Alert variant="danger">{erro}</Alert>}

      <div className="chat-window mb-3">
        {mensagens.map((m, i) => (
          <div key={i} className={`chat-bubble ${m.role === 'user' ? 'user' : 'jarbas'}`}>
            {m.content}
          </div>
        ))}
        {carregando && (
          <div className="chat-bubble jarbas">
            <Spinner size="sm" animation="border" /> pensando...
          </div>
        )}
        <div ref={fimRef} />
      </div>

      <Form onSubmit={submit}>
        <div className="d-flex gap-2">
          <Form.Control
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ex: quanto gastei essa semana? O que é um FII?"
            disabled={carregando}
          />
          <Button variant="primary" type="submit" disabled={carregando || !input.trim()}>
            Enviar
          </Button>
        </div>
      </Form>
    </>
  )
}
