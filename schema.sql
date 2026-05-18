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
    nome TEXT NOT NULL,
    descricao TEXT,
    categoria TEXT
);

-- 3. Tabela de Pontos de Coleta  
CREATE TABLE IF NOT EXISTS pontos_coleta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_local TEXT NOT NULL,   
    endereco TEXT NOT NULL,
    horario_funcionamento TEXT NOT NULL, 
    telefone_contato TEXT,             
    usuario_id INTEGER,                    
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);

-- 4. Tabela Associativa (Relacionamento N:N entre Pontos e Materiais)
CREATE TABLE IF NOT EXISTS pontos_coleta_materiais (
    ponto_coleta_id INTEGER,
    material_id INTEGER,
    PRIMARY KEY (ponto_coleta_id, material_id),
    FOREIGN KEY (ponto_coleta_id) REFERENCES pontos_coleta(id),
    FOREIGN KEY (material_id) REFERENCES materiais(id)
);