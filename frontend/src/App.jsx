import { Routes, Route, NavLink } from 'react-router-dom'
import { Navbar, Nav, Container, Badge } from 'react-bootstrap'
import Dashboard from './pages/Dashboard.jsx'
import CadastroGastos from './pages/CadastroGastos.jsx'
import Chat from './pages/Chat.jsx'
import Importar from './pages/Importar.jsx'

export default function App() {
  return (
    <>
      <Navbar bg="dark" variant="dark" expand="lg">
        <Container>
          <Navbar.Brand href="/">
            Jarbas <Badge bg="success">Agente Financeiro</Badge>
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto">
              <Nav.Link as={NavLink} to="/" end>Dashboard</Nav.Link>
              <Nav.Link as={NavLink} to="/gastos">Gastos</Nav.Link>
              <Nav.Link as={NavLink} to="/chat">Chat</Nav.Link>
              <Nav.Link as={NavLink} to="/importar">Importar</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Container className="mt-4">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/gastos" element={<CadastroGastos />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/importar" element={<Importar />} />
        </Routes>
      </Container>
    </>
  )
}
