import os
import re


SQLRAND_KEY = os.environ.get('SQLRAND_KEY', 'defaultkey123')

KEYWORDS = [
    "SELECT","FROM","WHERE","INSERT","INTO","VALUES",
    "UPDATE","SET","DELETE","JOIN","ON","AND","OR",
    "LIMIT","ORDER BY","GROUP BY"
]

def sqlrand_randomize(query: str) -> str:
    s = query
    kws = sorted(KEYWORDS, key=lambda k: -len(k))
    for kw in kws:
        s = re.sub(r'\b' + re.escape(kw) + r'\b', kw.lower() + SQLRAND_KEY, s, flags=re.IGNORECASE)
    return s

def derandomize(rand_query: str) -> str:
    s = rand_query
    kws = sorted(KEYWORDS, key=lambda k: -len(k))
    for kw in kws:
        pattern = r'\b' + re.escape(kw.lower() + SQLRAND_KEY) + r'\b'
        s = re.sub(pattern, kw, s, flags=re.IGNORECASE)
    return s

def validate_derandomized_query(sql: str):

    forbidden = ['DROP', 'ALTER', 'TRUNCATE', 'ATTACH', 'DETACH', 'PRAGMA']
    for f in forbidden:
        if re.search(r'\b' + f + r'\b', sql, flags=re.IGNORECASE):
            return False, f"Forbidden keyword: {f}"


    tables = set()
    tables |= set(re.findall(r'\bfrom\s+([A-Za-z_][A-Za-z0-9_]*)\b', sql, flags=re.IGNORECASE))
    tables |= set(re.findall(r'\binto\s+([A-Za-z_][A-Za-z0-9_]*)\b', sql, flags=re.IGNORECASE))
    tables |= set(re.findall(r'\bupdate\s+([A-Za-z_][A-Za-z0-9_]*)\b', sql, flags=re.IGNORECASE))

    allowed_tables = {'tasks', 'done'}
    for t in tables:
        if t.lower() not in allowed_tables:
            return False, f"Table not allowed: {t}"

    if not re.search(r'^\s*(SELECT|INSERT|UPDATE|DELETE)\b', sql, flags=re.IGNORECASE):
        return False, "Only SELECT/INSERT/UPDATE/DELETE allowed"

    return True, ""
