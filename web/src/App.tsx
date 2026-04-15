import { BrowserRouter, Routes, Route } from "react-router-dom"
import HomePage from "./pages/HomePage"
import PropertyDetail from "./components/layout/PropertyDetail"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/propiedad/:id" element={<PropertyDetail />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
