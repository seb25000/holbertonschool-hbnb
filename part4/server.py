from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, 
    template_folder='templates',  # dossier contenant les fichiers HTML
    static_folder='static'        # dossier contenant les fichiers statiques (CSS, JS, images)
)

# Configuration
app.config['API_URL'] = 'http://localhost:5001/api/v1'  # URL de l'API backend

@app.route('/')
def index():
    """Route pour la page d'accueil"""
    return render_template('index.html')

@app.route('/login')
def login():
    """Route pour la page de connexion"""
    return render_template('login.html')

@app.route('/place/<place_id>')
def place_details(place_id):
    """Route pour la page de détails d'une place"""
    return render_template('place.html')

@app.route('/add-review/<place_id>')
def add_review(place_id):
    """Route pour la page d'ajout de review"""
    return render_template('add_review.html')

@app.route('/favicon.ico')
def favicon():
    """Route pour le favicon"""
    return send_from_directory(os.path.join(app.root_path, 'static/images'),
                             'icon.png', mimetype='image/png')

# Gestion des erreurs
@app.errorhandler(404)
def page_not_found(e):
    """Page 404 personnalisée"""
    return render_template('404.html'), 404

if __name__ == '__main__':
    # En mode développement, on active le mode debug
    app.run(
        host='0.0.0.0',      # Écoute sur toutes les interfaces
        port=8000,           # Port 8000 comme le serveur original
        debug=True           # Mode debug activé
    ) 