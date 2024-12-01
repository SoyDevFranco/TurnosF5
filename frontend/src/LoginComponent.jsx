import React, { useState } from "react";
import { GoogleLogin } from "@react-oauth/google";
import RegisterComponent from "./RegisterComponent";
import SuccessComponent from "./successComponent";

const LoginComponent = () => {
  const [accessToken, setAccessToken] = useState(null);
  const [email, setEmail] = useState(null); // Almacenar el email del usuario
  const [error, setError] = useState(null); // Para manejar errores
  const [isRegistering, setIsRegistering] = useState(false); // Estado para el registro

  const handleLoginSuccess = async (credentialResponse) => {
    const { credential } = credentialResponse;

    console.log("Intentando iniciar sesión con Google...");

    if (!credential) {
      console.error("El token de credenciales está vacío o no se recibió.");
      return;
    }

    console.log("Token recibido:", credential);

    try {
      const response = await fetch("http://localhost:8001/auth/google", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ token: credential, "pepe": "pepe" }),
      });

      console.log("Respuesta del servidor recibida. Estado:", response.status);

      // Manejar respuesta del servidor
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error en la respuesta del servidor:", errorData);
        setError(errorData.detail); // Guarda el mensaje de error para depuración

        if (response.status === 401) {
          console.log(
            "Usuario no registrado. Redirigiendo al componente de registro..."
          );
          setEmail(credentialResponse.profileObj.email); // Guardar el email
          setIsRegistering(true); // Cambiar el estado a verdadero para mostrar el registro
          return;
        }
      } else if (response.status === 201) {
        console.log(
          "Usuario creado. Redirigiendo para completar el registro..."
        );
        setEmail(credentialResponse.profileObj.email); // Guardar el email
        setIsRegistering(true); // Cambiar el estado a verdadero para mostrar el registro
        return;
      } else {
        const responseData = await response.json();
        console.log(
          "Inicio de sesión exitoso. Datos de la respuesta:",
          responseData
        );
        setAccessToken(responseData.access_token); // Guarda el tokean de acceso
      }
    } catch (error) {
      console.error("Error al realizar la solicitud:", error);
    }
  };

  return (
    <div>
      <h1>Iniciar sesión</h1>
      {!accessToken && !isRegistering && (
        <GoogleLogin
          onSuccess={handleLoginSuccess}
          onError={(error) => {
            console.error("Error en Google Login:", error);
          }}
        />
      )}
      {error && <div className="error">{error}</div>}
      {accessToken && (
        <SuccessComponent message="¡Inicio de sesión exitoso! 🎉 Bienvenido!" />
      )}
      {isRegistering && (
        <RegisterComponent email={email} onRegisterSuccess={setAccessToken} />
      )}
    </div>
  );
};

export default LoginComponent;
