from flask import Flask, redirect, render_template, request
import requests
from sqlrand import sqlrand_randomize

app = Flask(__name__)

PROXY_URL = "http://localhost:5001/execute"
REQUEST_TIMEOUT = 5  

def execute_via_proxy(sql, params=()):

    sql_rand = sqlrand_randomize(sql)
    print("App -> Sending randomized query to proxy:", sql_rand)

    payload = {"query": sql_rand, "params": list(params)}
    try:
        r = requests.post(PROXY_URL, json=payload, timeout=REQUEST_TIMEOUT)
    except Exception as e:
        print("Error contacting proxy:", e)
        return None

    if r.status_code != 200:

        try:
            err = r.json().get("error", r.text)
        except Exception:
            err = r.text
        print(f"Proxy returned error (status {r.status_code}):", err)
        return None

    try:
        data = r.json().get("result")
    except Exception as e:
        print("Invalid JSON from proxy:", e)
        return None

    return data

@app.route('/addTask', methods=['GET'])
def add_task():
    task = request.args.get('task')
    if not task:
        return redirect('/')
    res = execute_via_proxy("INSERT INTO tasks(task) VALUES(?)", (task,))

    return redirect('/')

@app.route('/getTasks', methods=['GET'])
def get_tasks():
    rows = execute_via_proxy("SELECT * FROM tasks")

    return render_template("index.html", tasks=rows or [])

@app.route('/move-to-done/<int:id>/<string:task_name>')
def move_to_done(id, task_name):
    execute_via_proxy("INSERT INTO done(task, task_id) VALUES(?,?)", (task_name, id))
    execute_via_proxy("DELETE FROM tasks WHERE tid = ?", (id,))
    return redirect('/')

@app.route('/deleteTask/<int:id>')
def deleteTask(id):
    execute_via_proxy("DELETE FROM tasks WHERE tid=?", (id,))
    return redirect('/')

@app.route('/delete-completed/<int:id>')
def deleteCompletedTask(id):
    execute_via_proxy("DELETE FROM done WHERE did=?", (id,))
    return redirect('/')

@app.route('/')
def home():
    tasks = execute_via_proxy("SELECT * FROM tasks") or []
    done = execute_via_proxy("SELECT * FROM done") or []
    return render_template('index.html', tasks=tasks, done=done)

if __name__ == "__main__":
    app.run(debug=True)
