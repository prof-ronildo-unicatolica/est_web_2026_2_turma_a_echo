import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { apiDelete, apiGet } from "../services/api"

export default function AdminHoteis() {
  const [hoteis, setHoteis] = useState([])
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState("")

  useEffect(() => {
    apiGet("/hoteis")
      .then(setHoteis)
      .catch((error) => setErro(error.message))
      .finally(() => setCarregando(false))
  }, [])

  async function excluirHotel(hotel) {
    const confirmar = window.confirm(
      `Deseja realmente excluir o hotel "${hotel.nome}"?`
    )

    if (!confirmar) {
      return
    }

    try {
      await apiDelete(`/hoteis/${hotel.id}`)
      setHoteis((atuais) => atuais.filter((item) => item.id !== hotel.id))
    } catch (error) {
      setErro(error.message)
    }
  }

  function conteudo() {
    if (carregando) {
      return <p className="text-muted mb-0">Carregando hotéis...</p>
    }

    if (hoteis.length === 0) {
      return <p className="text-muted mb-0">Nenhum hotel cadastrado.</p>
    }

    return (
      <div className="table-responsive">
        <table className="table table-striped table-hover align-middle mb-0">
          <thead>
            <tr>
              <th scope="col">Nome</th>
              <th scope="col">Cidade</th>
              <th scope="col">Estrelas</th>
              <th scope="col" className="text-end">
                Ações
              </th>
            </tr>
          </thead>

          <tbody>
            {hoteis.map((hotel) => (
              <tr key={hotel.id}>
                <td>{hotel.nome}</td>
                <td>{hotel.cidade.nome}</td>
                <td aria-label={`${hotel.estrelas} estrelas`}>
                  {"★".repeat(hotel.estrelas)}
                </td>
                <td className="text-end">
                  <button
                    type="button"
                    className="btn btn-sm btn-danger"
                    onClick={() => excluirHotel(hotel)}
                  >
                    Excluir
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }

  return (
    <div>
      <div className="d-flex flex-wrap gap-2 justify-content-between align-items-center mb-4">
        <div>
          <h1>Administração de Hotéis</h1>
          <p className="mb-0">Gerencie os hotéis cadastrados no sistema.</p>
        </div>

        <Link to="/admin/hoteis/novo" className="btn btn-primary">
          Novo Hotel
        </Link>
      </div>

      {erro && (
        <div className="alert alert-danger" role="alert">
          {erro}
        </div>
      )}

      <div className="card">
        <div className="card-body">
          <h2 className="card-title h5 mb-3">Hotéis cadastrados</h2>
          {conteudo()}
        </div>
      </div>
    </div>
  )
}
