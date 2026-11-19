import { useEffect, useState } from "react"
import { apiGet } from "../services/api"

function formatarListaTecnologias(tecnologias) {
  if (!Array.isArray(tecnologias) || tecnologias.length === 0) {
    return "Sem tecnologias listadas"
  }
  return tecnologias.join(", ")
}

export default function Home() {
  const [dados, setDados] = useState(null)
  const [erro, setErro] = useState("")

  useEffect(() => {
    apiGet("/sobre")
      .then(setDados)
      .catch(() => setErro("Não foi possível conectar com o backend."))
  }, [])

  const nomeProfessor = dados?.professor?.nome || "Não cadastrado"
  const salaProfessor = dados?.professor?.sala || ""
  const disciplinas = Array.isArray(dados?.disciplinas) ? dados.disciplinas : []
  const stacks = Array.isArray(dados?.stacks) ? dados.stacks : []

  return (
    <div>
      <h1 className="mb-4">Sistema de Reservas</h1>

      {erro && (
        <div className="alert alert-danger" role="alert">
          {erro}
        </div>
      )}

      {dados && (
        <div className="card mb-4">
          <div className="card-body">
            <h5 className="card-title">Equipe {dados.equipe}</h5>

            <p className="card-text">
              <strong>Professor:</strong> {nomeProfessor}
              {salaProfessor ? ` (${salaProfessor})` : ""}
            </p>

            <p className="card-text">
              <strong>Período Letivo:</strong> {dados.ano}.{dados.semestre}
            </p>

            {disciplinas.length > 0 && (
              <div className="mt-3">
                <h6>Disciplinas Vinculadas</h6>
                <ul className="list-group list-group-flush">
                  {disciplinas.map((disc) => (
                    <li key={`${disc.nome}-${disc.ano}-${disc.semestre}`} className="list-group-item px-0">
                      <strong>{disc.nome}</strong> ({disc.ano}.{disc.semestre}) —{" "}
                      <span className="text-muted">
                        {formatarListaTecnologias(disc.tecnologias)}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {stacks.length > 0 && (
              <div className="mt-3">
                <h6>Stacks da Arquitetura</h6>
                <div className="d-flex flex-wrap gap-2">
                  {stacks.map((stack) => (
                    <span key={stack.nome} className="badge text-bg-secondary">
                      {stack.nome}: {Array.isArray(stack.tecnologias) ? stack.tecnologias.length : 0} tecnologia(s)
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div className="alert alert-success mt-3 mb-0">
              Backend conectado com sucesso!
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
