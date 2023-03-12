from flask import Flask, render_template, request, send_file, session
from pytube import YouTube
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = "654c0fb3968af9d5e6a9b3edcbc7051b"

@app.route('/load')
def load():
    if request.method == "POST":
        session['link'] = request.form.get('url')
        try:
            url = YouTube(session['link'])
            url.check_availability()
        except:
            return render_template("error.html")
        return render_template("download.html", url = url)
    return render_template("getData.html")

@app.route("/", methods = ["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download_audio():
    if request.method == "POST":
        session['link'] = request.form.get('url')
        try:
            url = YouTube(session['link'])
            url.check_availability()
        except:
            return render_template("error.html")
        buffer = BytesIO()
        audio_streams = url.streams.filter(only_audio=True).order_by('abr').desc().all()
        if len(audio_streams) == 0:
            return render_template("error.html")
        
        audio_streams[0].stream_to_buffer(buffer)
        buffer.seek(0)
        title = url.title
        file_name = f"{title}.mp3"
        return send_file(buffer, as_attachment=True, download_name=file_name, mimetype="audio/mpeg")
    return redirect(url_for("index"))
