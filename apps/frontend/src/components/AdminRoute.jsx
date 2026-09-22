import { useEffect, useState } from "react"
import { Navigate } from "react-router-dom"
import { apiGet } from "../services/api"

export default function AdminRoute({ children }) {
  const [usuario, setUsuario] = useState(null)
  const [carregando, setCarregando] = useState(true)

  useEffect(() => {
    async function verificarUsuario() {
      try {
        const dados = await apiGet("/auth/me")
        setUsuario(dados)
      } catch {
        setUsuario(null)
      } finally {
        setCarregando(false)
      }
    }

    verificarUsuario()
  }, [])

  if (carregando) {
    return <p>Carregando...</p>
  }

  if (!usuario?.is_admin) {
    return <Navigate to="/" replace />
  }

  return children
}