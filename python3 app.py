from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn  

@app.route('/', methods=['GET'])
def home():
    return "Bem-vindo ao sistema de gerenciamento de materiais!"

# 1. CREATE - Cadastrar novo material
@app.route('/materiais', methods=['POST'])
def criar_material():
    dados = request.get_json()
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO materiais (nome, descricao, categoria)
        VALUES (?, ?, ?)
    ''', (dados['nome'], dados.get('descricao'), dados.get('categoria')))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Material cadastrado com sucesso!"}), 201

# 2. READ - Listar todos os materiais
@app.route('/materiais', methods=['GET'])
def listar_materiais():
    conn = get_db_connection()
    materiais = conn.execute('SELECT * FROM materiais').fetchall()
    conn.close()
    return jsonify([dict(m) for m in materiais])

# 3. UPDATE - Editar um material existente
@app.route('/materiais/<int:id>', methods=['PUT'])
def editar_material(id):
    dados = request.get_json()
    conn = get_db_connection()
    conn.execute('''
        UPDATE materiais 
        SET nome = ?, descricao = ?, categoria = ?
        WHERE id = ?
    ''', (dados['nome'], dados.get('descricao'), dados.get('categoria'), id))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Material atualizado!"})

# 4. DELETE - Remover material
@app.route('/materiais/<int:id>', methods=['DELETE'])
def deletar_material(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM materiais WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Material removido!"})

#colocando os pontos de coleta
@app.route('/pontos', methods=['GET'])
def listar_pontos():
    conn = get_db_connection()
    pontos = conn.execute('SELECT * FROM pontos_coleta').fetchall()
    conn.close()
    return jsonify([dict(p) for p in pontos])

@app.route('/pontos/<int:id>', methods=['GET'])
def buscar_ponto(id):
    conn = get_db_connection()
    ponto = conn.execute(
        'SELECT * FROM pontos_coleta WHERE id = ?', (id,)
    ).fetchone()
    conn.close()

    if ponto is None:
        return jsonify({"erro": "Ponto não encontrado"}), 404

    return jsonify(dict(ponto))


@app.route('/pontos/<int:id>', methods=['PUT'])
def atualizar_ponto(id):
    dados = request.get_json()
    conn = get_db_connection()

    conn.execute('''
        UPDATE pontos_coleta
        SET nome_local = ?, endereco = ?, horario_funcionamento = ?, telefone_contato = ?, tipo_residuo_aceito = ?
        WHERE id = ?
    ''', (
        dados['nome_local'],
        dados['endereco'],
        dados['horario_funcionamento'],
        dados.get('telefone_contato'),
        dados.get('tipo_residuo_aceito'),
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Ponto atualizado com sucesso!"})

@app.route('/pontos/<int:id>', methods=['DELETE'])
def deletar_ponto(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM pontos_coleta WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Ponto removido com sucesso!"})



@app.route('/pontos', methods=['POST'])
def criar_ponto():
    dados = request.get_json()
    conn = get_db_connection()

    conn.execute('''
        INSERT INTO pontos_coleta 
        (nome_local, endereco, horario_funcionamento, telefone_contato, tipo_residuo_aceito)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        dados['nome_local'],
        dados['endereco'],
        dados['horario_funcionamento'],
        dados.get('telefone_contato'),
        dados.get('tipo_residuo_aceito')
    ))

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Ponto criado com sucesso!"}), 201


# 1. Cadastrar usuário



@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json(force=True, silent=True)
    if not dados or 'nome' not in dados or 'email' not in dados:
        return jsonify({"erro": "Campos 'nome' e 'email' são obrigatórios"}), 400
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO usuarios (nome, email, senha)
            VALUES (?, ?, ?)
        ''', (dados['nome'], dados['email'], dados.get('senha')))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"erro": "Email já cadastrado"}), 409
    conn.close()
    return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201
 
# 2. READ - Listar todos os usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    conn = get_db_connection()
    usuarios = conn.execute(
        'SELECT id, nome, email, data_criacao FROM usuarios'
    ).fetchall()
    conn.close()
    return jsonify([dict(u) for u in usuarios])
 
# 3. READ - Buscar usuário por ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    conn = get_db_connection()
    usuario = conn.execute(
        'SELECT id, nome, email, data_criacao FROM usuarios WHERE id = ?', (id,)
    ).fetchone()
    conn.close()
    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    return jsonify(dict(usuario))
 
# 4. UPDATE - Editar usuário
@app.route('/usuarios/<int:id>', methods=['PUT'])
def editar_usuario(id):
    dados = request.get_json(force=True, silent=True)
    if not dados or 'nome' not in dados or 'email' not in dados:
        return jsonify({"erro": "Campos 'nome' e 'email' são obrigatórios"}), 400
    conn = get_db_connection()
    conn.execute('''
        UPDATE usuarios
        SET nome = ?, email = ?, senha = ?
        WHERE id = ?
    ''', (dados['nome'], dados['email'], dados.get('senha'), id))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Usuário atualizado com sucesso!"})
 
# 5. DELETE - Remover usuário
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Usuário removido com sucesso!"})



