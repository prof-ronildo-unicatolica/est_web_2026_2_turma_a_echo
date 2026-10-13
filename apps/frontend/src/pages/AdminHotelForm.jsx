import { useEffect, useState } from "react"
import { apiGet } from "../services/api"

export default function AdminHotelForm() {
  const [nome, setNome] = useState("")
  const [cidadeId, setCidadeId] = useState("")
  const [cidades, setCidades] = useState([])

  useEffect(() => {
    async function carregarCidades() {
      try {
        const dados = await apiGet("/cidades")
        setCidades(dados)
      } catch (error) {
        console.error("Erro ao carregar cidades:", error)
      }
    }

    carregarCidades()
  }, [])

  function handleSubmit(event) {
    event.preventDefault()

    console.log({
      nome,
      cidade_id: cidadeId,
    })
  }

  return (
    <div>
      <h1>Novo Hotel</h1>

      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">
            Nome do hotel
          </label>

          <input
            type="text"
            className="form-control"
            placeholder="Digite o nome do hotel"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">
            Cidade
          </label>

          <select
            className="form-select"
            value={cidadeId}
            onChange={(e) => setCidadeId(e.target.value)}
            required
          >
            <option value="">
              Selecione uma cidade
            </option>

            {cidades.map((cidade) => (
              <option
                key={cidade.id}
                value={cidade.id}
              >
                {cidade.nome}
              </option>
            ))}
          </select>
        </div>

        <button
          type="submit"
          className="btn btn-primary"
        >
          Salvar
        </button>
      </form>
    </div>
  )
}