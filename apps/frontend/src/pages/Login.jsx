import { useState } from "react"
import { apiGet, apiPost } from "../services/api"

export default function Login() {
  const [email, setEmail] = useState("")
  const [senha, setSenha] = useState("")

async function handleSubmit(event) {
  event.preventDefault()

  try {
    const data = await apiPost("/auth/login", {
      email,
      senha,
    })

    const token = data.access_token || data.token

    localStorage.setItem("token", token)
    const usuario = await apiGet("/auth/me")
    console.log(usuario)

    alert("Login realizado com sucesso!")
  } catch (error) {
    alert(error.message)
  }
}

  return (
    <div className="row justify-content-center">
      <div className="col-md-5">
        <h1 className="mb-4">Login</h1>

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">E-mail</label>

            <input
              type="email"
              className="form-control"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="mb-3">
            <label className="form-label">Senha</label>

            <input
              type="password"
              className="form-control"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="btn btn-primary">
            Entrar
          </button>
        </form>
      </div>
    </div>
  )
}