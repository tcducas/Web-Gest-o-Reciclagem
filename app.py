from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

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

if __name__ == '__main__':
    app.run(debug=True)