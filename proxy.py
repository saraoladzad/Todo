from flask import Flask, request, jsonify
import sqlite3
import traceback

from sqlrand import SQLRAND_KEY, KEYWORDS, derandomize, validate_derandomized_query

app = Flask(__name__)

def is_randomized_format(s: str) -> bool:

    if not s:
        return False
    low = s.lower()
    k = SQLRAND_KEY.lower()
    for kw in KEYWORDS:
        if (kw.lower() + k) in low:
            return True
    return False

@app.route("/execute", methods=["POST"])
def execute_query():

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "invalid json body"}), 400

    randomized_query = data.get("query")
    params = data.get("params", [])


    print("=== Proxy: incoming request ===")
    print("Received randomized query:", repr(randomized_query))
    print("Params:", params)


    ok_format = is_randomized_format(randomized_query)
    print("Is randomized format?:", ok_format)
    if not ok_format:
        return jsonify({"error": "Query not in randomized format (missing key)"}), 400


    try:
        derand_query = derandomize(randomized_query)
    except Exception as e:
        print("Derandomize failed:", e)
        traceback.print_exc()
        return jsonify({"error": "derandomize failed"}), 400

    print("Derandomized query:", derand_query)


    ok, reason = validate_derandomized_query(derand_query)
    print("Validation result:", ok, reason)
    if not ok:
        return jsonify({"error": f"Query validation failed: {reason}"}), 400


    try:
        conn = sqlite3.connect("todo.db")
        cursor = conn.cursor()

        if params is None:
            params = []
        cursor.execute(derand_query, params)
        if derand_query.strip().lower().startswith("select"):
            rows = cursor.fetchall()

            result = [list(r) for r in rows]
        else:
            conn.commit()
            result = {"status": "ok", "rowcount": cursor.rowcount}
        cursor.close()
        conn.close()
        print("Execution successful.")
        return jsonify({"result": result}), 200
    except Exception as e:
        print("Execution error:", e)
        traceback.print_exc()
        return jsonify({"error": f"execution error: {str(e)}"}), 500

if __name__ == "__main__":

    app.run(host="127.0.0.1", port=5001, debug=True)
