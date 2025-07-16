from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__) # __name__ == "__main__"

# CRUD or C.R.U.D.
# Create, Read, Update and Delete / Criar, Ler, Atualizar e Deletar

tasks = []
task_id_control = 1

# ROTA de CREAT
@app.route('/tasks', methods=['POST'])
def creat_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data['title'], description=data.get("description", ""))
    task_id_control += 1 # serve p/ acrescentar +1 no id, p/ ñ ter ids iguais
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Nova tarefa criada com sucesso", "id":new_task.id})

# ROTA de READ
@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    
    output = {
                "tasks": task_list,
                "total_tasks": len(task_list)
            }
    return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    
    return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

# ROTA de UPDATE
@app.route('/tasks/<int:id>', methods=["PUT"])
def update_tasl(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    print(task)
    if task == None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404
    
    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    print(task)
    return jsonify({"message":"Tarefa atualizada com sucesso"}), 200

# ROTA de DELETE
@app.route('/tasks/<int:id>', methods=["DELETE"])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    
    if not task:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404
    tasks.remove(task)
    return jsonify({"message":"Tarefa deletada com sucesso"}), 200

# @app.route('/user/<username>')
# def show_user(username):
#    print(username)
#    print(type(username))
#    return username

# @app.route('/userid/<int:user_id>')*/
# def show_user(user_id):
#    print(user_id)
#    print(type(user_id))
#    return "%s" % user_id

## Converter types: ##
# string -- (default) accepts any text without a slash
# int -- accepts positive integers
# float -- accepts positive floating point values
# path -- like string but also accepts slashes
# uuid -- accepts UUID strings
### flask.palletsprojects.com/en/3.0.x/quickstart/#routing ###

if __name__ == "__main__":
    app.run(debug=True)