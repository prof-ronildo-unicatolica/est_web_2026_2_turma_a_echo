import { BrowserRouter, Route, Routes } from "react-router-dom"

import Home from "./pages/Home"
import Hoteis from "./pages/Hoteis"
import Reservas from "./pages/Reservas"
import Login from "./pages/Login"
import Navbar from "./components/Navbar"

import Admin from "./pages/Admin"
import AdminRoute from "./components/AdminRoute"
import AdminHoteis from "./pages/AdminHoteis"
import AdminHotelForm from "./pages/AdminHotelForm"

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <main className="container mt-4">
        <Routes>
          <Route path="/" element={<Home />} />

          <Route path="/hoteis" element={<Hoteis />} />

          <Route path="/reservas" element={<Reservas />} />

          <Route path="/login" element={<Login />} />

          <Route
            path="/admin"
            element={
              <AdminRoute>
                <Admin />
              </AdminRoute>
            }
          />

          <Route
            path="/admin/hoteis"
            element={
              <AdminRoute>
                <AdminHoteis />
              </AdminRoute>
            }
          />

          <Route
            path="/admin/hoteis/novo"
            element={
              <AdminRoute>
                <AdminHotelForm />
              </AdminRoute>
            }
          />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App
