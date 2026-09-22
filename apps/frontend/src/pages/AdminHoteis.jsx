import { Link } from "react-router-dom"

export default function AdminHoteis() {
  const hoteis = []

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1>Administração de Hotéis</h1>
          <p>Gerencie os hotéis cadastrados no sistema.</p>
        </div>

      <Link to="/admin/hoteis/novo" className="btn btn-primary">
        Novo Hotel
        </Link>
      </div>

      <div className="card">
        <div className="card-body">
          <h5 className="card-title">Hotéis cadastrados</h5>

          {hoteis.length === 0 ? (
            <p className="text-muted mb-0">
              Nenhum hotel cadastrado.
            </p>
          ) : (
            <table className="table">
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
                      <button className="btn btn-sm btn-warning me-2">
                        Editar
                      </button>

                      <button className="btn btn-sm btn-danger">
                        Excluir
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  )
}