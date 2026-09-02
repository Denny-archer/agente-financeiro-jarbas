import { useState, useRef } from 'react'
import { Form, Button, Alert, Card, Table, Spinner } from 'react-bootstrap'
import { importarCSV } from '../services/api'

export default function Importar() {
  const [arquivo, setArquivo] = useState(null)
  const [nomeArquivo, setNomeArquivo] = useState('')
  const [importando, setImportando] = useState(false)
  const [resultado, setResultado] = useState(null)
  const [erro, setErro] = useState('')
  const fileRef = useRef(null)

  const onSelect = (e) => {
    setArquivo(e.target.files[0] || null)
    setNomeArquivo(e.target.files[0]?.name || '')
    setResultado(null)
    setErro('')
  }

  const submit = async (e) => {
    e.preventDefault()
    if (!arquivo) return
    setImportando(true)
    setErro('')
    setResultado(null)
    try {
      const res = await importarCSV(arquivo)
      setResultado(res)
      fileRef.current.value = ''
      setArquivo(null)
      setNomeArquivo('')
    } catch (err) {
      setErro(err.message)
    } finally {
      setImportando(false)
    }
  }

  return (
    <>
      <h1 className="mb-4">Importar transações (CSV)</h1>

      <p className="text-muted">
        Envie um arquivo <code>.csv</code> com as colunas{' '}
        <code>data</code>, <code>valor</code> (e opcionais <code>categoria</code>,{' '}
        <code>descricao</code>). A categoria é inferida automaticamente quando não informada.
      </p>

      {resultado && (
        <Alert variant={resultado.erros?.length ? 'warning' : 'success'}>
          <strong>{resultado.importados}</strong> de <strong>{resultado.total}</strong> registros
          importados.
          {resultado.erros?.length > 0 && (
            <>
              {' '}Houve <strong>{resultado.erros.length}</strong> erro(s).
            </>
          )}
        </Alert>
      )}
      {erro && <Alert variant="danger">{erro}</Alert>}

      {resultado?.erros?.length > 0 && (
        <Card className="mb-3">
          <Card.Header>Erros na importação</Card.Header>
          <Card.Body>
            <Table size="sm" striped responsive className="mb-0">
              <thead>
                <tr><th>Linha</th><th>Erro</th></tr>
              </thead>
              <tbody>
                {resultado.erros.map((e, i) => (
                  <tr key={i}>
                    <td>{e.linha}</td>
                    <td>{e.erro}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Card.Body>
        </Card>
      )}

      <Card>
        <Card.Body>
          <Form onSubmit={submit}>
            <Form.Group className="mb-3">
              <Form.Label>Arquivo CSV</Form.Label>
              <Form.Control
                type="file"
                accept=".csv"
                ref={fileRef}
                onChange={onSelect}
                required
              />
              {nomeArquivo && <Form.Text className="text-muted">Selecionado: {nomeArquivo}</Form.Text>}
            </Form.Group>
            <Button variant="primary" type="submit" disabled={!arquivo || importando}>
              {importando ? (
                <>
                  <Spinner size="sm" animation="border" className="me-1" /> Importando...
                </>
              ) : (
                'Importar'
              )}
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </>
  )
}
