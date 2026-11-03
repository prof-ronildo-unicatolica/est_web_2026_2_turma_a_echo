import { BrowserRouter, Link, Route, Routes } from "react-router-dom"

import Home from "./pages/Home"
import Hoteis from "./pages/Hoteis"
import Reservas from "./pages/Reservas"
import Login from "./pages/Login"
import LogoutButton from "./components/LogoutButton"

import Admin from "./pages/Admin"
import AdminRoute from "./components/AdminRoute"
import AdminHoteis from "./pages/AdminHoteis"
import AdminHotelForm from "./pages/AdminHotelForm"

function App() {
  return (
    <BrowserRouter>
      <nav className="navbar navbar-expand-lg bg-dark navbar-dark">
        <div className="container">
          <Link className="navbar-brand" to="/">
            Hotelaria
          </Link>

          <div className="navbar-nav">

            <Link className="nav-link" to="/admin/hoteis/novo">
              Novo Hotel
            </Link>
            
            <Link className="nav-link" to="/">
              Home
            </Link>

            <Link className="nav-link" to="/hoteis">
              Hotéis
            </Link>

            <Link className="nav-link" to="/reservas">
              Minhas Reservas
            </Link>

            <Link className="nav-link" to="/login">
              Login
            </Link>

            <LogoutButton />
          </div>
        </div>
      </nav>

      <main className="container mt-4">
        <Routes>
          <Route path="/" element={<Home />} />

          <Route path="/hoteis" element={<Hoteis />} />

          <Route path="/reservas" element={<Reservas />} />

          <Route path="/login" element={<Login />} />

          <Route
            path="/admin"
            element={
              <AdminRoute>
                <Admin />
              </AdminRoute>
            }
          />

          <Route
            path="/admin/hoteis"
            element={
              <AdminRoute>
                <AdminHoteis />
              </AdminRoute>
            }
          />

          <Route
            path="/admin/hoteis/novo"
            element={
              <AdminRoute>
                <AdminHotelForm />
              </AdminRoute>
            }
          />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App