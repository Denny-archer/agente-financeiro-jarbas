import { useEffect, useState } from 'react'
import { Row, Col, Card, Table, Alert, Spinner, Badge } from 'react-bootstrap'
import { obterResumo, obterAlertas } from '../services/api'

function Money({ value }) {
  return <strong>R$ {Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</strong>
}

export default function Dashboard() {
  const [resumoDia, setResumoDia] = useState(null)
  const [resumoSemana, setResumoSemana] = useState(null)
  const [alertas, setAlertas] = useState([])
  const [erro, setErro] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    Promise.all([obterResumo('dia'), obterResumo('semana'), obterAlertas()])
      .then(([dia, semana, alertas]) => {
        setResumoDia(dia)
        setResumoSemana(semana)
        setAlertas(alertas)
      })
      .catch((e) => setErro(e.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" />
      </div>
    )
  }

  return (
    <>
      <h1 className="mb-4">Dashboard</h1>

      {erro && <Alert variant="danger">{erro}</Alert>}

      <Row className="mb-4">
        <Col md={6}>
          <Card className="mb-3">
            <Card.Header>Hoje</Card.Header>
            <Card.Body>
              <h2><Money value={resumoDia?.total ?? 0} /></h2>
              <Table size="sm" striped className="mt-3 mb-0">
                <thead>
                  <tr><th>Categoria</th><th className="text-end">Valor</th></tr>
                </thead>
                <tbody>
                  {Object.entries(resumoDia?.por_categoria ?? {}).map(([cat, valor]) => (
                    <tr key={cat}>
                      <td>{cat}</td>
                      <td className="text-end"><Money value={valor} /></td>
                    </tr>
                  ))}
                  {Object.keys(resumoDia?.por_categoria ?? {}).length === 0 && (
                    <tr><td colSpan="2" className="text-muted">Nenhum gasto hoje.</td></tr>
                  )}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card className="mb-3">
            <Card.Header>Últimos 7 dias</Card.Header>
            <Card.Body>
              <h2><Money value={resumoSemana?.total ?? 0} /></h2>
              <Table size="sm" striped className="mt-3 mb-0">
                <thead>
                  <tr><th>Categoria</th><th className="text-end">Valor</th></tr>
                </thead>
                <tbody>
                  {Object.entries(resumoSemana?.por_categoria ?? {}).map(([cat, valor]) => (
                    <tr key={cat}>
                      <td>{cat}</td>
                      <td className="text-end"><Money value={valor} /></td>
                    </tr>
                  ))}
                  {Object.keys(resumoSemana?.por_categoria ?? {}).length === 0 && (
                    <tr><td colSpan="2" className="text-muted">Nenhum gasto na semana.</td></tr>
                  )}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Card>
        <Card.Header>Alertas de limite</Card.Header>
        <Card.Body>
          {alertas.length === 0 ? (
            <p className="text-muted mb-0">Nenhum limite excedido. 🎉</p>
          ) : (
            <Table responsive striped className="mb-0">
              <thead>
                <tr>
                  <th>Categoria</th>
                  <th className="text-end">Gasto atual</th>
                  <th className="text-end">Limite</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {alertas.map((a) => (
                  <tr key={a.categoria}>
                    <td>{a.categoria}</td>
                    <td className="text-end"><Money value={a.gasto_atual} /></td>
                    <td className="text-end"><Money value={a.limite} /></td>
                    <td><Badge bg="danger">Excedido</Badge></td>
                  </tr>
                ))}
              </tbody>
            </Table>
          )}
        </Card.Body>
      </Card>
    </>
  )
}
