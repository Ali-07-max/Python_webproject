from os.path import splitext
from re import split
from flask import Flask, config, render_template, request, send_file
from werkzeug.utils import secure_filename
from flask.helpers import redirect
import os
from werkzeug.exceptions import RequestEntityTooLarge
from PIL import Image , ImageEnhance

app = Flask(__name__, template_folder='templets', static_folder='statics')
app.config['upload_folder'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                                           'statics', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif']
app.config['PDF_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                                        'statics' , 'pdfs')
@app.route('/')
@app.route('/home')
def index():
  print(app.config['upload_folder'])
  return render_template('index.html')


@app.route('/uploads', methods=['POST'])
def upload():
  try:
  # Get the uploaded file
    file = request.files['file']
    if file:
      extension = os.path.splitext(file.filename)[1].lower()
      if extension not in app.config['ALLOWED_EXTENSIONS']:
        return 'File is not an image.'
      file.save(os.path.join(app.config['upload_folder'], secure_filename(file.filename)))
      image = Image.open(os.path.join(app.config['upload_folder'], secure_filename(file.filename)))
      nameoffile = os.path.splitext(file.filename)[0]               
      pdf_path = os.path.join(app.config['PDF_FOLDER'], f"{nameoffile}.pdf")
      image.save(pdf_path, "PDF")
    return redirect('/')
  except  RequestEntityTooLarge:
    return 'File is larger then 16MBs.'

if __name__ == '__main__':
  app.run(debug=True)
