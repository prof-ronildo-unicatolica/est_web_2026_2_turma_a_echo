import { useEffect, useState } from "react"
import { Link, NavLink, useLocation } from "react-router-dom"
import LogoutButton from "./LogoutButton"
import { apiGet } from "../services/api"

const LINKS_PUBLICOS = [
  { to: "/", rotulo: "Home", end: true },
  { to: "/hoteis", rotulo: "Hotéis" },
  { to: "/reservas", rotulo: "Minhas Reservas" },
]

const LINKS_ADMIN = [
  { to: "/admin/hoteis", rotulo: "Gerenciar hotéis", end: true },
  { to: "/admin/hoteis/novo", rotulo: "Novo hotel" },
]

function classeDoLink({ isActive }) {
  return isActive ? "nav-link active" : "nav-link"
}

export default function Navbar() {
  // useLocation faz a barra re-renderizar a cada troca de rota, e assim ela
  // percebe o token gravado pelo login ou apagado pelo logout.
  useLocation()
  const token = localStorage.getItem("token")
  const [isAdmin, setIsAdmin] = useState(false)

  useEffect(() => {
    if (!token) {
      setIsAdmin(false)
      return
    }

    apiGet("/auth/me")
      .then((usuario) => setIsAdmin(Boolean(usuario?.is_admin)))
      .catch(() => setIsAdmin(false))
  }, [token])

  return (
    <nav className="navbar navbar-expand-lg bg-dark navbar-dark">
      <div className="container">
        <Link className="navbar-brand" to="/">
          Hotelaria
        </Link>

        <button
          type="button"
          className="navbar-toggler"
          data-bs-toggle="collapse"
          data-bs-target="#menu-principal"
          aria-controls="menu-principal"
          aria-expanded="false"
          aria-label="Abrir menu"
        >
          <span className="navbar-toggler-icon" />
        </button>

        <div className="collapse navbar-collapse" id="menu-principal">
          <ul className="navbar-nav me-auto">
            {LINKS_PUBLICOS.map((link) => (
              <li className="nav-item" key={link.to}>
                <NavLink className={classeDoLink} to={link.to} end={link.end}>
                  {link.rotulo}
                </NavLink>
              </li>
            ))}

            {isAdmin &&
              LINKS_ADMIN.map((link) => (
                <li className="nav-item" key={link.to}>
                  <NavLink className={classeDoLink} to={link.to} end={link.end}>
                    {link.rotulo}
                  </NavLink>
                </li>
              ))}
          </ul>

          <div className="d-flex">
            {token ? (
              <LogoutButton />
            ) : (
              <Link className="btn btn-outline-light" to="/login">
                Login
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
