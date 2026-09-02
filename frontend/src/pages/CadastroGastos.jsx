import { useState } from 'react'
import { Form, Button, Alert, Card, Row, Col, Badge } from 'react-bootstrap'
import { cadastrarGasto } from '../services/api'

const CATEGORIAS_SUGERIDAS = [
  'Alimentacao', 'Streaming', 'Transporte', 'Saude',
  'Investimento', 'Moradia', 'Entretenimento', 'Educacao', 'Outros',
]

export default function CadastroGastos() {
  const [data, setData] = useState(new Date().toISOString().slice(0, 10))
  const [categoria, setCategoria] = useState('')
  const [valor, setValor] = useState('')
  const [descricao, setDescricao] = useState('')
  const [resultado, setResultado] = useState(null)
  const [erro, setErro] = useState('')
  const [enviando, setEnviando] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setErro('')
    setResultado(null)
    setEnviando(true)

    const payload = {
      data,
      valor: parseFloat(valor.replace(',', '.')),
      descricao,
    }
    if (categoria) payload.categoria = categoria

    try {
      const res = await cadastrarGasto(payload)
      setResultado(res)
      setValor('')
      setDescricao('')
      setCategoria('')
    } catch (err) {
      setErro(err.message)
    } finally {
      setEnviando(false)
    }
  }

  return (
    <>
      <h1 className="mb-4">Cadastrar gasto</h1>

      {resultado && (
        <Alert variant="success">
          {resultado.mensagem}{' '}
          {resultado.categoria && <Badge bg="secondary">{resultado.categoria}</Badge>}
        </Alert>
      )}
      {erro && <Alert variant="danger">{erro}</Alert>}

      <Card>
        <Card.Body>
          <Form onSubmit={submit}>
            <Row>
              <Col md={3}>
                <Form.Group className="mb-3">
                  <Form.Label>Data</Form.Label>
                  <Form.Control
                    type="date"
                    value={data}
                    onChange={(e) => setData(e.target.value)}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group className="mb-3">
                  <Form.Label>Categoria <span className="text-muted">(opcional)</span></Form.Label>
                  <Form.Select value={categoria} onChange={(e) => setCategoria(e.target.value)}>
                    <option value="">— Automática —</option>
                    {CATEGORIAS_SUGERIDAS.map((c) => (
                      <option key={c} value={c}>{c}</option>
                    ))}
                  </Form.Select>
                  <Form.Text className="text-muted">
                    Se não informada, o Jarbas infere pela descrição.
                  </Form.Text>
                </Form.Group>
              </Col>
              <Col md={5}>
                <Form.Group className="mb-3">
                  <Form.Label>Valor (R$)</Form.Label>
                  <Form.Control
                    type="text"
                    inputMode="decimal"
                    placeholder="ex: 49,90"
                    value={valor}
                    onChange={(e) => setValor(e.target.value)}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>
            <Form.Group className="mb-3">
              <Form.Label>Descrição</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
                placeholder="ex: Pedido iFood, assinatura Netflix, corrida Uber..."
                value={descricao}
                onChange={(e) => setDescricao(e.target.value)}
                required
              />
            </Form.Group>
            <Button variant="primary" type="submit" disabled={enviando}>
              {enviando ? 'Salvando...' : 'Cadastrar gasto'}
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </>
  )
}
