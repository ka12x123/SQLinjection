from flask import Flask, request, render_template, jsonify
import pymysql

app = Flask(__name__)

@app.route('/soso', methods=['POST'])
def indexto():
    login = request.json.get('login')
    password = request.json.get('pw')
    
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='1234',
                           database='datainjection',
                           cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    print(login, password)
    queryId = "SELECT * FROM roro4 WHERE id = %s"
    cursor.execute(queryId, (login))
    user = cursor.fetchone()
    if user and user['id'] == login and user['pw'] == password:
        return jsonify({"success": True, "id" : user['id']})
    else:
        return jsonify({"success": False})

@app.route('/souce')
def souce():
    return render_template('souce.html')

@app.route('/login_suc_guest')
def login_suc_guest():
    return render_template('login_suc_guest.html')

@app.route('/login_suc_admin')
def login_suc_admin():
    return render_template('login_suc_admin.html')

@app.route('/')
def index():
    pw = request.args.get('pw', '')
    response = ""

    # 필터링 로직
    if any(keyword in pw.lower() for keyword in ['_', '.', '()', 'or', 'and', 'substr(', '=']):
        response = "필터링에 걸렸다,"
    
    # 데이터베이스 연결
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='1234',
                           database='datainjection',
                           cursorclass=pymysql.cursors.DictCursor)
    
    cursor = conn.cursor()
    
    # 파라미터화된 쿼리
    query = f"SELECT id FROM roro4 WHERE id='guest' AND pw='{pw}'"
    cursor.execute(query)
    result = cursor.fetchone()
    response += f"<hr>query : <strong>{query}</strong><hr><br>"
    
    if result:
        response += f"<h2>Hello {result['id']}</h2>"
    
    # 두 번째 쿼리
    query = f"SELECT pw FROM roro4 WHERE id='admin' AND pw='{pw}'"
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result and result['pw'] == pw:
        response += "<h2>성공 했어요</h2>"
    
    conn.close()
    
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
