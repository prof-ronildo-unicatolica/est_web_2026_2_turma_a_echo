import { useState } from "react"
import { apiGet, apiPost } from "../services/api"

function extrairTokenDeAcesso(resposta) {
  if (!resposta) {
    return ""
  }
  return resposta.access_token || resposta.token || ""
}

export default function Login() {
  const [email, setEmail] = useState("")
  const [senha, setSenha] = useState("")
  const [mensagemErro, setMensagemErro] = useState("")
  const [perfilAutenticado, setPerfilAutenticado] = useState(null)
  const [enviando, setEnviando] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setMensagemErro("")
    setPerfilAutenticado(null)
    setEnviando(true)

    try {
      const data = await apiPost("/auth/login", {
        email: email.trim(),
        senha,
      })

      const token = extrairTokenDeAcesso(data)
      localStorage.setItem("token", token)

      const usuario = await apiGet("/auth/me")
      setPerfilAutenticado(usuario)
    } catch (error) {
      setMensagemErro(error.message || "Falha ao autenticar usuário.")
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="row justify-content-center">
      <div className="col-md-5">
        <h1 className="mb-4">Login</h1>

        {mensagemErro && (
          <div className="alert alert-danger" role="alert">
            {mensagemErro}
          </div>
        )}

        {perfilAutenticado && (
          <div className="alert alert-success" role="status">
            Sessão iniciada como <strong>{perfilAutenticado.nome || perfilAutenticado.email}</strong>.
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="login-email" className="form-label">
              E-mail
            </label>

            <input
              id="login-email"
              type="email"
              className="form-control"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              required
            />
          </div>

          <div className="mb-3">
            <label htmlFor="login-senha" className="form-label">
              Senha
            </label>

            <input
              id="login-senha"
              type="password"
              className="form-control"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              autoComplete="current-password"
              required
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={enviando}
          >
            {enviando ? "Autenticando..." : "Entrar"}
          </button>
        </form>
      </div>
    </div>
  )
}
