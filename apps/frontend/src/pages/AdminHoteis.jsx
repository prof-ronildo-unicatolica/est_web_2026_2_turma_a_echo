import { Link } from "react-router-dom"
import { useState } from "react"

export default function AdminHoteis() {
  const [hoteis, setHoteis] = useState([
    {
      id: 1,
      nome: "Hotel Central",
      cidade: "Fortaleza",
    },
    {
      id: 2,
      nome: "Hotel Juazeiro",
      cidade: "Juazeiro do Norte",
    },
    {
      id: 3,
      nome: "Hotel Quixadá",
      cidade: "Quixadá",
    },
  ])

  function excluirHotel(id) {
    const confirmar = window.confirm(
      "Deseja realmente excluir este hotel?"
    )

    if (!confirmar) {
      return
    }

    setHoteis(
      hoteis.filter((hotel) => hotel.id !== id)
    )
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1>Administração de Hotéis</h1>
          <p>
            Gerencie os hotéis cadastrados no sistema.
          </p>
        </div>

        <Link
          to="/admin/hoteis/novo"
          className="btn btn-primary"
        >
          Novo Hotel
        </Link>
      </div>

      <div className="card">
        <div className="card-body">

          <h5 className="card-title mb-3">
            Hotéis cadastrados
          </h5>

          {hoteis.length === 0 ? (
            <p className="text-muted">
              Nenhum hotel cadastrado.
            </p>
          ) : (
            <div className="table-responsive">

              <table className="table table-striped table-hover">

                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Cidade</th>
                    <th>Ações</th>
                  </tr>
                </thead>

                <tbody>

                  {hoteis.map((hotel) => (
                    <tr key={hotel.id}>

                      <td>{hotel.nome}</td>

                      <td>{hotel.cidade}</td>

                      <td>
                        <button
                          type="button"
                          className="btn btn-sm btn-warning me-2"
                          onClick={() =>
                            alert(
                              "A edição será integrada à API de Hotéis."
                            )
                          }
                        >
                          Editar
                        </button>

                        <button
                          type="button"
                          className="btn btn-sm btn-danger"
                          onClick={() =>
                            excluirHotel(hotel.id)
                          }
                        >
                          Excluir
                        </button>
                      </td>

                    </tr>
                  ))}

                </tbody>

              </table>

            </div>
          )}

        </div>
      </div>
    </div>
  )
}