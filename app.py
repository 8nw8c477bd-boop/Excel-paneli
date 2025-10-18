from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = "supersecretkey"
DATA_FILE = 'data/content.json'
ADMIN_PASSWORD = "özkan"

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        if name == ADMIN_PASSWORD:
            session['user'] = 'admin'
            return redirect('/admin')
        data = load_data()
        if name in data['titles']:
            session['user'] = name
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session or session['user'] == 'admin':
        return redirect('/')
    user = session['user']
    data = load_data()
    index = data['titles'].index(user)
    return render_template('dashboard.html', title=user, content=data['contents'][index])

@app.route('/update', methods=['POST'])
def update():
    if 'user' not in session:
        return 'Unauthorized', 403
    user = session['user']
    new_text = request.form['content']
    data = load_data()
    index = data['titles'].index(user)
    data['contents'][index] = new_text
    save_data(data)
    return 'Kaydedildi'

@app.route('/admin')
def admin():
    if 'user' not in session or session['user'] != 'admin':
        return redirect('/')
    data = load_data()
    return render_template('admin.html', titles=data['titles'], contents=data['contents'])

@app.route('/admin/update_titles', methods=['POST'])
def update_titles():
    new_titles = request.form.getlist('titles[]')
    data = load_data()
    data['titles'] = new_titles
    save_data(data)
    return 'Başlıklar güncellendi'

@app.route('/admin/clear_all', methods=['POST'])
def clear_all():
    data = load_data()
    data['contents'] = [""] * len(data['contents'])
    save_data(data)
    return 'Tüm metinler silindi'

if __name__ == '__main__':
    app.run()
