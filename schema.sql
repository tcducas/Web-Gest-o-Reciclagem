-- 1. Tabela de Usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL, 
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabela de Materiais Recicláveis
CREATE TABLE IF NOT EXISTS materiais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL, -- Ex: Plástico, Papel, Eletrônicos
    descricao TEXT,
    categoria TEXT
);

-- 3. Tabela de Pontos de Coleta  
CREATE TABLE IF NOT EXISTS pontos_coleta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_local TEXT NOT NULL,   
    endereco TEXT NOT NULL,
    -- Campos Cruciais:
    horario_funcionamento TEXT NOT NULL, -- Tag importante para o usuário
    telefone_contato TEXT,
    tipo_residuo_aceito TEXT,              
    usuario_id INTEGER,                    
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);