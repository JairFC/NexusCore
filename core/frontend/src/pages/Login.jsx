import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; // ✅ No olvides importar Axios aquí
import reactLogo from '../assets/react.svg'; // tu logo actual

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const apiBaseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

    try {
      const response = await axios.post(`${apiBaseUrl}/auth/login`, {
        username,
        password,
      });

      console.log('Respuesta del servidor:', response.data);

      if (response.status === 200) {
        alert('¡Inicio de sesión exitoso!');
        navigate('/dashboard'); //  Redirigir si todo sale bien
      }
    } catch (error) {
      console.error('Error al iniciar sesión:', error);
      alert('Error al iniciar sesión: ' + (error.response?.data?.detail || 'Network Error'));
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 px-4">
      <div className="bg-gray-800 p-8 rounded-xl shadow-2xl w-full max-w-md">
        <div className="flex justify-center mb-6">
          <img src={reactLogo} alt="Logo" className="h-16 animate-spin-slow" />
        </div>
        <h1 className="text-3xl font-bold text-center text-white mb-6">Iniciar Sesión</h1>
        <form onSubmit={handleSubmit} className="space-y-5">
          <input
            type="text"
            placeholder="Usuario"
            className="w-full p-3 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Contraseña"
            className="w-full p-3 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition duration-200"
          >
            Entrar
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
