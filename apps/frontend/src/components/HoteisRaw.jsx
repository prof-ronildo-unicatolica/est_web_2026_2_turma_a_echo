import { useEffect, useState } from "react"
import API_URL, { apiGet } from "../services/api"

// Mostra o JSON exatamente como a API devolveu: o objetivo e provar que o dado
// atravessou todas as camadas, do PostgreSQL ao navegador. Um card estilizado
// esconderia um campo faltando; o JSON cru nao esconde nada.
export default function HoteisRaw() {
  const [cidades, setCidades] = useState(null)
  const [hoteis, setHoteis] = useState(null)
  const [erro, setErro] = useState("")
  const [carregando, setCarregando] = useState(true)

  useEffect(() => {
    // As duas requisicoes nao dependem uma da outra: disparam em paralelo.
    Promise.all([apiGet("/cidades"), apiGet("/hoteis")])
      .then(([jsonCidades, jsonHoteis]) => {
        setCidades(jsonCidades)
        setHoteis(jsonHoteis)
      })
      .catch((error) => setErro(error.message))
      .finally(() => setCarregando(false))
  }, [])

  if (carregando) {
    return <p>Carregando hotéis...</p>
  }

  if (erro) {
    return (
      <div className="alert alert-danger" role="alert">
        <strong>Erro ao falar com a API:</strong> {erro}
        <br />
        O backend está no ar? Teste: <code>{API_URL}/hoteis</code>
      </div>
    )
  }

  return (
    <div className="row g-4">
      <section className="col-lg-4">
        <h2 className="h5">GET /cidades</h2>
        <pre className="bg-light border rounded p-3 small">
          {JSON.stringify(cidades, null, 2)}
        </pre>
      </section>

      <section className="col-lg-8">
        <h2 className="h5">GET /hoteis</h2>
        <pre className="bg-light border rounded p-3 small">
          {JSON.stringify(hoteis, null, 2)}
        </pre>
      </section>
    </div>
  )
}
