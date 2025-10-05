## Todo App with SQLrand

This project explores integrating **SQLrand** into a **Flask-based Todo List application** to randomize SQL queries and help prevent SQL injection.

The base application is a simple open-source Todo List app available at [pj8912/todo-app](https://github.com/pj8912/todo-app.git). I cloned and modified it to integrate SQLrand for experiments.


## Requirements
- Python 3.x  
- Flask  
- SQLite3  
- Jinja2   


## Usage

1️⃣ Clone the repository

```bash
git clone https://github.com/saraoladzad/Todo.git
cd Todo
```

2️⃣ Create and activate a virtual environment

```bash
python -m venv venv
```

Activate the environment:

  Linux/macOS:
  ```bash
source venv/bin/activate
```


Windows PowerShell:
  ```bash
.\venv\Scripts\Activate.ps1
```


Windows CMD:
  ```bash
venv\Scripts\activate.bat
```

3️⃣ Install dependencies

  ```bash
pip install -r requirements.txt
```

4️⃣ (Optional) Initialize the database

  ```bash
python init_db.py
```

5️⃣ Generate SQLrand key

  ```bash
python -c "import secrets; print(secrets.token_hex(16))"
```

Copy the printed 16-character hexadecimal key.

6️⃣ Set SQLRAND_KEY in each terminal

Linux/macOS:
  ```bash
export SQLRAND_KEY="PASTE_KEY_HERE"
```

Windows PowerShell:
  ```bash
$env:SQLRAND_KEY="PASTE_KEY_HERE"
```

Windows CMD:
  ```bash
set SQLRAND_KEY=PASTE_KEY_HERE
```

7️⃣ Start the proxy (Terminal A)

  ```bash
python proxy.py
```

8️⃣ Start the Flask app (Terminal B)

  ```bash
python app.py
```

9️⃣ Open the web UI

http://127.0.0.1:5000/


