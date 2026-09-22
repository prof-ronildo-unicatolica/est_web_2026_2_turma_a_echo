export default function LogoutButton() {
  function handleLogout() {
    localStorage.removeItem("token")
    window.location.href = "/login"
  }

  return (
    <button className="btn btn-outline-danger" onClick={handleLogout}>
      Sair
    </button>
  )
}