// frontend/src/App.jsx
import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"; // Cambia Switch por Routes
import LoginComponent from "./LoginComponent";
import RegisterComponent from "./RegisterComponent";
import SuccessComponent from "./successComponent"; // Importa el nuevo componente
import HomePage from "./HomePage"; // Asegúrate de importar la página de inicio si la tienes

const App = () => {
  const [accessToken, setAccessToken] = useState(null);

  return (
    <Router>
      <div>
        <h1>Bienvenido a la Aplicación</h1>
        <Routes>
          {" "}
          {/* Usa Routes en lugar de Switch */}
          <Route
            path="/"
            element={
              accessToken ? (
                <HomePage />
              ) : (
                <LoginComponent onLoginSuccess={setAccessToken} />
              )
            }
          />
          <Route path="/register" element={<RegisterComponent />} />
          <Route path="/success" element={<SuccessComponent />} />
          {/* Otras rutas aquí */}
        </Routes>
      </div>
    </Router>
  );
};

export default App;
