// Em desenvolvimento o Vite repassa /api para o backend (vite.config.js) e, no
// Docker, o nginx faz o mesmo: o caminho relativo funciona nos dois e dispensa
// CORS. VITE_API_URL permite apontar para outro host quando for preciso.
const API_URL = import.meta.env.VITE_API_URL ?? "/api/v1"

const ERRO_PADRAO = "Erro ao acessar a API"

function getHeaders() {
  const token = localStorage.getItem("token")

  return {
    "Content-Type": "application/json",
    ...(token && {
      Authorization: `Bearer ${token}`,
    }),
  }
}

async function lerCorpo(response) {
  // 204 No Content (ex.: DELETE) nao tem corpo; response.json() lancaria.
  const texto = await response.text()

  if (!texto) {
    return null
  }

  try {
    return JSON.parse(texto)
  } catch {
    // Erro 500 do servidor costuma vir como texto puro.
    return { detail: texto }
  }
}

function mensagemDeErro(data) {
  const detail = data?.detail

  if (typeof detail === "string") {
    return detail
  }

  // 422 do FastAPI: lista de erros de validacao, um por campo.
  if (Array.isArray(detail)) {
    return detail.map((erro) => erro.msg).join("; ")
  }

  return ERRO_PADRAO
}

async function handleResponse(response, endpoint) {
  const data = await lerCorpo(response)

  if (response.status === 401 && endpoint !== "/auth/login") {
    localStorage.removeItem("token")
    window.location.href = "/login"
    throw new Error("Sessão expirada")
  }

  if (!response.ok) {
    throw new Error(mensagemDeErro(data))
  }

  return data
}

async function request(method, endpoint, data) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    method,
    headers: getHeaders(),
    ...(data !== undefined && { body: JSON.stringify(data) }),
  })

  return handleResponse(response, endpoint)
}

export function apiGet(endpoint) {
  return request("GET", endpoint)
}

export function apiPost(endpoint, data) {
  return request("POST", endpoint, data)
}

export function apiPut(endpoint, data) {
  return request("PUT", endpoint, data)
}

export function apiDelete(endpoint) {
  return request("DELETE", endpoint)
}

export default API_URL
