-- Script de inicialización
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contraseña hash de 'admin123'
INSERT INTO users (username, password_hash)
VALUES ('admin', '$2b$12$.srKy8vjpe/byqSmhdr.6OKUlqWu18CLCFZzoKPTbmFMtTk4XG3bi');
