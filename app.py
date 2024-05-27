from flask import Flask, request, render_template, make_response, request
import pymysql

app = Flask(__name__)

def login_chk():
    pass

@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    resp.set_cookie('PHPSESSID', '2en3inka7nng9jhvqilo9dkpg6')
    return resp

@app.route('/souce')
def index1():
    return render_template('souce.html')

@app.route('/login', methods=['GET'])
def login():
    pw = request.args.get('pw', '')
    
    # 필터링 로직
    if any(keyword in pw.lower() for keyword in ['prob', '_', '.', '()', 'or', 'and', 'substr(', '=']):
        return "필터링에 걸렸습니다~"
    
    # 데이터베이스 연결
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='1234',
                           database='datainjection',
                           cursorclass=pymysql.cursors.DictCursor)  
    cursor = conn.cursor()
    
    # 첫 번째 쿼리 (파라미터화된 쿼리 사용)
    query = "SELECT id FROM roro4 WHERE id='guest' AND pw=%s"
    cursor.execute(query, (pw,))
    result = cursor.fetchone()
    
    response = f"<hr>query : <strong>SELECT id FROM roro3 WHERE id='guest' AND pw='{pw}'</strong><hr><br>"
    
    if result:
        response += f"<h2>Hello!~ {result['id']}</h2>"
    
    # 두 번째 쿼리 (파라미터화된 쿼리 사용)
    query = "SELECT id, pw FROM roro4 WHERE id='admin' AND pw=%s"
    cursor.execute(query, (pw,))
    result = cursor.fetchone()

    if result and 'pw' in result and result['pw'] == pw:
        response += "<h2>성공 했습니다!!</h2>"
    
    conn.close()
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
