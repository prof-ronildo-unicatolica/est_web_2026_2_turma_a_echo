import { useState } from "react"

export default function AdminHotelForm() {
  const [nome, setNome] = useState("")
  const [cidade, setCidade] = useState("")

  function handleSubmit(event) {
    event.preventDefault()

    console.log({
      nome,
      cidade,
    })
  }

  return (
    <div>
      <h1>Novo Hotel</h1>

      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Nome do hotel</label>

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
          <label className="form-label">Cidade</label>

          <select
            className="form-select"
            value={cidade}
            onChange={(e) => setCidade(e.target.value)}
            required
          >
            <option value="">Selecione uma cidade</option>
            <option value="1">Cidade de teste</option>
          </select>
        </div>

        <button type="submit" className="btn btn-primary">
          Salvar
        </button>
      </form>
    </div>
  )
}