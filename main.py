import sqlite3
from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel, Field
app = FastAPI()

conexao = sqlite3.connect('tarefas.db', check_same_thread=False)
conexao.execute('''CREATE TABLE IF NOT EXISTS tarefas
                    (id INTEGER PRIMARY KEY, titulo TEXT, concluida BOOLEAN)''')
conexao.commit()

class Tarefa(BaseModel):
    titulo: str = Field(min_length=1)
    concluida: bool = False


@app.get("/tarefas")
def listar_tarefas():
    cursor = conexao.execute('SELECT id, titulo, concluida FROM tarefas')
    tarefas_banco = []
    for linha in cursor.fetchall():
        tarefas_banco.append({
            "id": linha[0],
            "titulo": linha[1],
            "concluida": bool(linha[2]),
        })
    return tarefas_banco

@app.get("/tarefas/{id}")
def buscar_tarefa(id: int):
    cursor = conexao.execute('SELECT id, titulo, concluida FROM tarefas WHERE id = ?', (id,))
    linha = cursor.fetchone()
    if linha:
        return {"id": linha[0], "titulo": linha[1], "concluida": bool(linha[2])}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.post("/tarefas")
def gravar_tarefa(tarefa: Tarefa):
    cursor =  conexao.execute('INSERT INTO tarefas (titulo, concluida) VALUES (?, ?)', (tarefa.titulo, tarefa.concluida))
    conexao.commit()
    novo_id = cursor.lastrowid
    return {"id": novo_id, "titulo": tarefa.titulo, "concluida": tarefa.concluida}



@app.put("/tarefas/{id}")
def atualizar_tarefa(id: int, tarefa_atualizada: Tarefa):
    cursor = conexao.execute(
        'UPDATE tarefas SET titulo = ?, concluida = ? WHERE id = ?',
        (tarefa_atualizada.titulo, tarefa_atualizada.concluida, id),
    )
    conexao.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"id": id, "titulo": tarefa_atualizada.titulo, "concluida": tarefa_atualizada.concluida}

@app.delete("/tarefas/{id}")
def deletar_tarefa(id: int):
    cursor = conexao.execute('DELETE FROM tarefas WHERE id = ?', (id,))
    conexao.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"message": "Tarefa deletada com sucesso"}