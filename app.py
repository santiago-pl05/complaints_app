from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import database
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tajny-klucz'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

socketio = SocketIO(app, cors_allowed_origins="*")

# Utwórz folder uploads jeśli nie istnieje
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Strona główna - panel klienta
@app.route('/')
def index():
    return render_template('index.html')

# Panel administratora
@app.route('/admin')
def admin():
    return render_template('admin.html')

# API: Dodaj reklamację
@app.route('/api/complaints', methods=['POST'])
def api_add_complaint():
    try:
        title = request.form['title']
        description = request.form['description']
        importer = request.form['importer']
        product_code = request.form.get('code', '')  # POPRAWIONE: obsługa kodu produktu
        
        # Zapisz zdjęcie jeśli jest
        photo_path = None
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{secure_filename(photo.filename)}"
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                photo.save(photo_path)
        
        # Zapisz do bazy - POPRAWIONE: dodanie product_code
        complaint_id = database.add_complaint(
            title=title, 
            description=description, 
            importer=importer, 
            product_code=product_code, 
            photo_path=photo_path
        )
        
        # Wyślij powiadomienie przez WebSocket
        socketio.emit('new_complaint', {
            'id': complaint_id,
            'title': title,
            'status': 'new'
        })
        
        return jsonify({'success': True, 'id': complaint_id})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API: Pobierz reklamacje
@app.route('/api/complaints', methods=['GET'])
def api_get_complaints():
    complaints = database.get_complaints()
    return jsonify(complaints)

# WebSocket events
@socketio.on('connect')
def handle_connect():
    print('Klient podłączony')

if __name__ == '__main__':
    # Inicjalizuj bazę danych
    database.init_database()
    
    # Uruchom serwer
    print("Serwer uruchamia się na http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)