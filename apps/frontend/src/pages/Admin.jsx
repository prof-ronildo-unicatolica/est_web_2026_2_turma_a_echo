import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { apiGet } from "../services/api"

function calcularMediaEstrelas(hoteis) {
  if (!Array.isArray(hoteis) || hoteis.length === 0) {
    return "0.0"
  }
  const soma = hoteis.reduce(
    (acc, item) => acc + (Number(item.estrelas) || 0),
    0
  )
  return (soma / hoteis.length).toFixed(1)
}

export default function Admin() {
  const [resumo, setResumo] = useState({
    totalCidades: 0,
    totalHoteis: 0,
    mediaEstrelas: "0.0",
    cidadesRecentes: [],
  })
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState("")

  async function carregarIndicadores() {
    setCarregando(true)
    setErro("")
    try {
      const [cidades, hoteis] = await Promise.all([
        apiGet("/cidades"),
        apiGet("/hoteis"),
      ])
      const listaCidades = Array.isArray(cidades) ? cidades : []
      const listaHoteis = Array.isArray(hoteis) ? hoteis : []

      setResumo({
        totalCidades: listaCidades.length,
        totalHoteis: listaHoteis.length,
        mediaEstrelas: calcularMediaEstrelas(listaHoteis),
        cidadesRecentes: listaCidades.slice(0, 5),
      })
    } catch {
      setErro("Não foi possível carregar os indicadores administrativos.")
    } finally {
      setCarregando(false)
    }
  }

  useEffect(() => {
    carregarIndicadores()
  }, [])

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1>Área Administrativa</h1>
          <p className="text-muted mb-0">
            Acesso permitido apenas para administradores. Acompanhe o inventário da rede hoteleira.
          </p>
        </div>

        <div className="d-flex gap-2">
          <button
            type="button"
            className="btn btn-outline-secondary"
            onClick={carregarIndicadores}
            disabled={carregando}
          >
            {carregando ? "Atualizando..." : "Atualizar Dados"}
          </button>
          <Link to="/admin/hoteis" className="btn btn-primary">
            Gerenciar Hotéis
          </Link>
        </div>
      </div>

      {erro && (
        <div className="alert alert-warning" role="alert">
          {erro}
        </div>
      )}

      <div className="row g-3 mb-4">
        <div className="col-md-4">
          <div className="card text-center">
            <div className="card-body">
              <h6 className="text-muted">Cidades Atendidas</h6>
              <p className="display-6 mb-0">{resumo.totalCidades}</p>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card text-center">
            <div className="card-body">
              <h6 className="text-muted">Hotéis Cadastrados</h6>
              <p className="display-6 mb-0">{resumo.totalHoteis}</p>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card text-center">
            <div className="card-body">
              <h6 className="text-muted">Média de Estrelas</h6>
              <p className="display-6 mb-0">{resumo.mediaEstrelas}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-body">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h5 className="card-title mb-0">Cidades no Catálogo</h5>
            <Link to="/admin/hoteis/novo" className="btn btn-sm btn-outline-primary">
              Cadastrar Novo Hotel
            </Link>
          </div>

          {resumo.cidadesRecentes.length === 0 ? (
            <p className="text-muted mb-0">
              Nenhuma cidade localizada no catálogo atual.
            </p>
          ) : (
            <ul className="list-group list-group-flush">
              {resumo.cidadesRecentes.map((cidade) => (
                <li
                  key={cidade.id}
                  className="list-group-item d-flex justify-content-between align-items-center px-0"
                >
                  <span>{cidade.nome}</span>
                  <span className="badge text-bg-light">{cidade.id}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  )
}
