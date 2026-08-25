import { useEffect, useState } from "react"
import { apiGet } from "../services/api"

export default function Home() {
  const [dados, setDados] = useState(null)
  const [erro, setErro] = useState("")

  useEffect(() => {
    apiGet("/sobre")
      .then(setDados)
      .catch(() => setErro("Não foi possível conectar com o backend."))
  }, [])

  return (
    <div>
      <h1 className="mb-4">Sistema de Reservas</h1>

      {erro && (
        <div className="alert alert-danger">
          {erro}
        </div>
      )}

      {dados && (
        <div className="card">
          <div className="card-body">
            <h5 className="card-title">{dados.equipe}</h5>

            <p className="card-text">
              <strong>Professor:</strong> {dados.professor.nome}
            </p>

            <p className="card-text">
              <strong>Ano:</strong> {dados.ano}
            </p>

            <p className="card-text">
              <strong>Semestre:</strong> {dados.semestre}
            </p>

            <div className="alert alert-success mt-3">
              Backend conectado com sucesso!
            </div>
          </div>
        </div>
      )}
    </div>
  )
}