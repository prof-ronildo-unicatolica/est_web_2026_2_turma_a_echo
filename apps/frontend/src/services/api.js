const API_URL = "http://localhost:8000/api/v1"

function getHeaders() {
  const token = localStorage.getItem("token")

  return {
    "Content-Type": "application/json",
    ...(token && {
      Authorization: `Bearer ${token}`,
    }),
  }
}

async function handleResponse(response, endpoint) {
  const data = await response.json()

  if (response.status === 401 && endpoint !== "/auth/login") {
    localStorage.removeItem("token")
    window.location.href = "/login"
    throw new Error("Sessão expirada")
  }

  if (!response.ok) {
    throw new Error(data.detail || "Erro ao acessar a API")
  }

  return data
}

export async function apiGet(endpoint) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    headers: getHeaders(),
  })

  return handleResponse(response, endpoint)
}

export async function apiPost(endpoint, data) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify(data),
  })

  return handleResponse(response, endpoint)
}

export default API_URL