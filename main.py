from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from flask.helpers import redirect
import os

app = Flask(__name__, template_folder='templets', static_folder='statics')
app.config['upload_folder'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'statics', 'uploads')


@app.route('/')
@app.route('/home')
def index():
  print(app.config['upload_folder'])
  return render_template('index.html')


@app.route('/uploads', methods=['POST'])
def upload():
  # Get the uploaded file
  file = request.files['file']
  if file:
    file.save(os.path.join(app.config['upload_folder'], secure_filename(file.filename)))
  return redirect('/')


if __name__ == '__main__':
  app.run(debug=True)
