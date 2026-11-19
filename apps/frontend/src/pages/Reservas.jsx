import { useEffect, useState } from "react"
import { apiGet } from "../services/api"

function filtrarHoteisDisponiveis(hoteis, cidadeSelecionada, estrelasMinimas) {
  return hoteis.filter((hotel) => {
    const atendeCidade =
      !cidadeSelecionada || String(hotel.cidade_id) === String(cidadeSelecionada)
    const atendeEstrelas =
      !estrelasMinimas || Number(hotel.estrelas || 0) >= Number(estrelasMinimas)
    return atendeCidade && atendeEstrelas
  })
}

function formatarEstrelas(quantidade) {
  const total = Math.max(1, Math.min(5, Number(quantidade) || 1))
  return `${total} estrela${total > 1 ? "s" : ""}`
}

export default function Reservas() {
  const [cidades, setCidades] = useState([])
  const [hoteis, setHoteis] = useState([])
  const [cidadeFiltro, setCidadeFiltro] = useState("")
  const [estrelasFiltro, setEstrelasFiltro] = useState("")
  const [hospedeNome, setHospedeNome] = useState("")
  const [noites, setNoites] = useState("2")
  const [reservas, setReservas] = useState([])
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState("")

  useEffect(() => {
    let ativo = true

    async function carregarCatalogo() {
      setCarregando(true)
      setErro("")
      try {
        const [listaCidades, listaHoteis] = await Promise.all([
          apiGet("/cidades"),
          apiGet("/hoteis"),
        ])
        if (ativo) {
          setCidades(Array.isArray(listaCidades) ? listaCidades : [])
          setHoteis(Array.isArray(listaHoteis) ? listaHoteis : [])
        }
      } catch {
        if (ativo) {
          setErro("Não foi possível carregar o catálogo de hotéis para reserva.")
        }
      } finally {
        if (ativo) {
          setCarregando(false)
        }
      }
    }

    carregarCatalogo()
    return () => {
      ativo = false
    }
  }, [])

  function adicionarReserva(hotel) {
    const nomeLimpo = hospedeNome.trim() || "Hóspede Padrão"
    const totalNoites = Math.max(1, Number(noites) || 1)
    const novaReserva = {
      codigo: `${hotel.id}-${totalNoites}-${nomeLimpo}`,
      hotelId: hotel.id,
      hotelNome: hotel.nome,
      cidadeNome: hotel.cidade?.nome || "Cidade não informada",
      estrelas: hotel.estrelas,
      hospede: nomeLimpo,
      noites: totalNoites,
    }

    setReservas((atuais) => {
      const semDuplicata = atuais.filter((item) => item.hotelId !== hotel.id)
      return [...semDuplicata, novaReserva]
    })
  }

  function cancelarReserva(hotelId) {
    setReservas((atuais) => atuais.filter((item) => item.hotelId !== hotelId))
  }

  function limparFiltros() {
    setCidadeFiltro("")
    setEstrelasFiltro("")
  }

  const hoteisFiltrados = filtrarHoteisDisponiveis(
    hoteis,
    cidadeFiltro,
    estrelasFiltro
  )

  return (
    <div>
      <h1 className="mb-3">Minhas Reservas</h1>
      <p className="text-muted">
        Consulte os hotéis disponíveis por cidade e categoria para planejar sua estadia.
      </p>

      {erro && (
        <div className="alert alert-warning" role="alert">
          {erro}
        </div>
      )}

      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title mb-3">Filtros e Dados da Estadia</h5>
          <div className="row g-3">
            <div className="col-md-3">
              <label htmlFor="reserva-hospede" className="form-label">
                Nome do hóspede
              </label>
              <input
                id="reserva-hospede"
                type="text"
                className="form-control"
                placeholder="Informe seu nome"
                value={hospedeNome}
                onChange={(e) => setHospedeNome(e.target.value)}
              />
            </div>

            <div className="col-md-2">
              <label htmlFor="reserva-noites" className="form-label">
                Diárias (noites)
              </label>
              <input
                id="reserva-noites"
                type="number"
                min="1"
                max="30"
                className="form-control"
                value={noites}
                onChange={(e) => setNoites(e.target.value)}
              />
            </div>

            <div className="col-md-4">
              <label htmlFor="reserva-cidade" className="form-label">
                Filtrar por cidade
              </label>
              <select
                id="reserva-cidade"
                className="form-select"
                value={cidadeFiltro}
                onChange={(e) => setCidadeFiltro(e.target.value)}
              >
                <option value="">Todas as cidades</option>
                {cidades.map((cidade) => (
                  <option key={cidade.id} value={cidade.id}>
                    {cidade.nome}
                  </option>
                ))}
              </select>
            </div>

            <div className="col-md-3">
              <label htmlFor="reserva-estrelas" className="form-label">
                Classificação mínima
              </label>
              <div className="d-flex gap-2">
                <select
                  id="reserva-estrelas"
                  className="form-select"
                  value={estrelasFiltro}
                  onChange={(e) => setEstrelasFiltro(e.target.value)}
                >
                  <option value="">Todas</option>
                  <option value="3">3+ estrelas</option>
                  <option value="4">4+ estrelas</option>
                  <option value="5">5 estrelas</option>
                </select>
                <button
                  type="button"
                  className="btn btn-outline-secondary"
                  onClick={limparFiltros}
                >
                  Limpar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="row g-4">
        <div className="col-lg-7">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title mb-3">
                Hotéis Disponíveis ({hoteisFiltrados.length})
              </h5>

              {carregando ? (
                <p className="text-muted">Carregando opções de hospedagem...</p>
              ) : hoteisFiltrados.length === 0 ? (
                <p className="text-muted">
                  Nenhum hotel encontrado para os critérios selecionados.
                </p>
              ) : (
                <ul className="list-group">
                  {hoteisFiltrados.map((hotel) => (
                    <li
                      key={hotel.id}
                      className="list-group-item d-flex justify-content-between align-items-center"
                    >
                      <div>
                        <strong>{hotel.nome}</strong>
                        <div className="small text-muted">
                          {hotel.cidade?.nome || "Cidade"} · {formatarEstrelas(hotel.estrelas)}
                        </div>
                      </div>
                      <button
                        type="button"
                        className="btn btn-sm btn-primary"
                        onClick={() => adicionarReserva(hotel)}
                      >
                        Selecionar
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>

        <div className="col-lg-5">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title mb-3">
                Resumo de Pré-Reservas ({reservas.length})
              </h5>

              {reservas.length === 0 ? (
                <p className="text-muted">
                  Selecione um hotel ao lado para simular sua reserva.
                </p>
              ) : (
                <ul className="list-group">
                  {reservas.map((item) => (
                    <li
                      key={item.codigo}
                      className="list-group-item d-flex justify-content-between align-items-center"
                    >
                      <div>
                        <strong>{item.hotelNome}</strong>
                        <div className="small text-muted">
                          {item.cidadeNome} · {item.noites} noite(s) · {item.hospede}
                        </div>
                      </div>
                      <button
                        type="button"
                        className="btn btn-sm btn-outline-danger"
                        onClick={() => cancelarReserva(item.hotelId)}
                      >
                        Remover
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
