// frontend/src/main.jsx
import React from "react";
import ReactDOM from "react-dom/client";
import { GoogleOAuthProvider } from "@react-oauth/google";
import App from "./app.jsx"; // Asegurate de la ruta correctai

ReactDOM.createRoot(document.getElementById("app")).render(
  <GoogleOAuthProvider clientId="277449645968-7q19lqbsb10cvoasbgp4pevqvnnnjttn.apps.googleusercontent.com">
    <App />
  </GoogleOAuthProvider>
);
