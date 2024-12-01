import React, { useState } from "react";

const RegisterComponent = ({ email, onRegisterSuccess }) => {
  const [name, setName] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(
        "https://d277-2803-9800-9024-7c0f-28f0-aaa9-4ae4-622a.ngrok-free.app/auth/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email, name, phone_number: phoneNumber }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Error: ${errorData.detail}`);
      }

      const data = await response.json();
      onRegisterSuccess(data.access_token); // Llama a la función pasada para manejar el éxito
    } catch (error) {
      console.error("Error al registrar:", error);
    }
  };

  return (
    <form onSubmit={handleRegister}>
      <h2>Completa tu registro</h2>
      <input
        type="text"
        placeholder="Nombre"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="tel"
        placeholder="Número de Teléfono"
        value={phoneNumber}
        onChange={(e) => setPhoneNumber(e.target.value)}
        required
      />
      <button type="submit">Registrarse</button>
    </form>
  );
};

export default RegisterComponent;
