from app import app
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
import os
from pathlib import Path
from time import perf_counter

app.config['UPLOAD_FOLDER'] = "./uploads/uploadFolder/"

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/format-conversion', methods=['GET','POST'])
def format_conversion():
    if(request.method=='POST'):
        file_names = request.files.getlist('filename[]')
        file_format = request.form.get('file-format')

        '''UPLOADING THE FILE TO A SPECIFIC LOCATION'''
        for file_name in file_names:
            file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_name.filename)))
            name_request = file_name.filename
 
        for file_name in file_names:
            myvideo = VideoFileClip("./uploads/uploadFolder/"+secure_filename(file_name.filename))
            name = secure_filename(file_name.filename)[:-4]+"-NewFormat"+file_format
            myvideo.write_videofile(f"./uploads/output_files/{name}", codec="libx264")
            
        file_area = "f'./uploads/output_files/{name_request}', codec='libx264'"
        '''RETURNING THE PAGE WITH URL LINK OF Converted FILES'''
        # return render_template('format-conversion.html', msg="Merged Successfully", file_path="f'./uploads/output_files/{name}', codec='libx264'")   
        return render_template('download.html')
    else:
        return render_template('format-conversion.html', msg="", file_path="")


@app.route('/download')
def download():
    p = "uploads\\output_files\\{file_name.filename}+file_format', codec='libx264'"
    return send_file(p, as_attachment=True)

# @app.route("/uploads/output_files/{name}, codec='libx264'", methods=['GET', 'POST'])
# def download(filen):
#     # Appending app path to upload folder path within app root folder
#     uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
#     # Returning file from appended path
#     return send_from_directory(directory=uploads, filen=filen)
