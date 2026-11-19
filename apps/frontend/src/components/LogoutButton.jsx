function handleLogout() {
  localStorage.removeItem("token")
  window.location.href = "/login"
}

export default function LogoutButton() {
  return (
    <button
      type="button"
      className="btn btn-outline-danger"
      onClick={handleLogout}
    >
      Sair
    </button>
  )
}
