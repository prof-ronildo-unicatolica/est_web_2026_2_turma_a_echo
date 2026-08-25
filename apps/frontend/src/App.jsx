import { BrowserRouter, Link, Route, Routes } from "react-router-dom"

import Home from "./pages/Home"
import Hoteis from "./pages/Hoteis"
import Reservas from "./pages/Reservas"
import Login from "./pages/Login"

function App() {
  return (
    <BrowserRouter>
      <nav className="navbar navbar-expand-lg bg-dark navbar-dark">
        <div className="container">
          <Link className="navbar-brand" to="/">
            Hotelaria
          </Link>

          <div className="navbar-nav">
            <Link className="nav-link" to="/">Home</Link>
            <Link className="nav-link" to="/hoteis">Hotéis</Link>
            <Link className="nav-link" to="/reservas">Minhas Reservas</Link>
            <Link className="nav-link" to="/login">Login</Link>
          </div>
        </div>
      </nav>

      <main className="container mt-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/hoteis" element={<Hoteis />} />
          <Route path="/reservas" element={<Reservas />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App