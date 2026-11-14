import { useEffect, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { apiGet, apiPost } from "../services/api"

const OPCOES_ESTRELAS = [1, 2, 3, 4, 5]

export default function AdminHotelForm() {
  const navigate = useNavigate()
  const [nome, setNome] = useState("")
  const [cidadeId, setCidadeId] = useState("")
  const [estrelas, setEstrelas] = useState("3")
  const [cidades, setCidades] = useState([])
  const [erro, setErro] = useState("")
  const [salvando, setSalvando] = useState(false)

  useEffect(() => {
    apiGet("/cidades")
      .then(setCidades)
      .catch(() => setErro("Não foi possível carregar as cidades."))
  }, [])

  async function handleSubmit(event) {
    event.preventDefault()
    setErro("")
    setSalvando(true)

    try {
      await apiPost("/hoteis", {
        nome: nome.trim(),
        cidade_id: cidadeId,
        estrelas: Number(estrelas),
      })
      navigate("/admin/hoteis")
    } catch (error) {
      setErro(error.message)
    } finally {
      setSalvando(false)
    }
  }

  return (
    <div className="row justify-content-center">
      <div className="col-md-8 col-lg-6">
        <h1 className="mb-4">Novo Hotel</h1>

        {erro && (
          <div className="alert alert-danger" role="alert">
            {erro}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="hotel-nome" className="form-label">
              Nome do hotel
            </label>

            <input
              id="hotel-nome"
              type="text"
              className="form-control"
              placeholder="Digite o nome do hotel"
              maxLength={100}
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              required
            />
          </div>

          <div className="mb-3">
            <label htmlFor="hotel-cidade" className="form-label">
              Cidade
            </label>

            <select
              id="hotel-cidade"
              className="form-select"
              value={cidadeId}
              onChange={(e) => setCidadeId(e.target.value)}
              required
            >
              <option value="">Selecione uma cidade</option>

              {cidades.map((cidade) => (
                <option key={cidade.id} value={cidade.id}>
                  {cidade.nome}
                </option>
              ))}
            </select>
          </div>

          <div className="mb-4">
            <label htmlFor="hotel-estrelas" className="form-label">
              Estrelas
            </label>

            <select
              id="hotel-estrelas"
              className="form-select"
              value={estrelas}
              onChange={(e) => setEstrelas(e.target.value)}
              required
            >
              {OPCOES_ESTRELAS.map((quantidade) => (
                <option key={quantidade} value={quantidade}>
                  {"★".repeat(quantidade)} ({quantidade})
                </option>
              ))}
            </select>
          </div>

          <div className="d-flex gap-2">
            <button type="submit" className="btn btn-primary" disabled={salvando}>
              {salvando ? "Salvando..." : "Salvar"}
            </button>

            <Link to="/admin/hoteis" className="btn btn-outline-secondary">
              Cancelar
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}
