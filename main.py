from os.path import splitext
from re import split
from flask import Flask, config, render_template, request, send_file
from werkzeug.utils import secure_filename
from flask.helpers import redirect
import os
from werkzeug.exceptions import RequestEntityTooLarge
from PIL import Image, ImageEnhance
import docx2pdf
from aspose.words import Document, SaveFormat

app = Flask(__name__, template_folder='templets', static_folder='statics')
app.config['upload_folder'] = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'statics', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['ALLOWED_EXTENSIONS'] = [
    '.jpg', '.jpeg', '.png', '.gif', '.docx', '.doc', '.xlxs', '.xlsx',
    '.pptx', '.ppt', '.txt'
]
app.config['PDF_FOLDER'] = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'statics', 'pdfs')


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
      file.save(
          os.path.join(app.config['upload_folder'],
                       secure_filename(file.filename)))

    try:
      if extension == '.jpg' or extension == '.jpeg' or extension == '.png' or extension == '.gif':
        nameoffile = os.path.splitext(file.filename)[0]
        pdf_path = os.path.join(app.config['PDF_FOLDER'], f"{nameoffile}.pdf")
        image = Image.open(
            os.path.join(app.config['upload_folder'],
                         secure_filename(file.filename)))
        image.save(pdf_path, "PDF")
        return send_file(pdf_path,
                         as_attachment=True,
                         download_name=f"{nameoffile}.pdf")
      if extension == '.docx' or extension == '.doc':
        nameoffile = os.path.splitext(file.filename)[0]
        pdf_path = os.path.join(app.config['PDF_FOLDER'], f"{nameoffile}.pdf")
        doc = Document(
            os.path.join(app.config['upload_folder'],
                         secure_filename(file.filename)))
        doc.save(pdf_path, SaveFormat.PDF)
    except Exception as e:
      print(e)
      return 'Error converting file to PDF. Please Try Again'
    return redirect('/')
  except RequestEntityTooLarge:
    return 'File is larger then 16MBs.'


if __name__ == '__main__':
  app.run(debug=True)
