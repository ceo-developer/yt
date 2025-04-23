from flask import Flask, request, jsonify, send_file
import youtube_dl
import os
from pytube import YouTube
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return "YouTube Downloader API is Active!"

@app.route('/info', methods=['GET'])
def info():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL missing'}), 400
    try:
        yt = YouTube(url)
        data = {
            'title': yt.title,
            'thumbnail': yt.thumbnail_url,
            'length': yt.length,
            'author': yt.author
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    fmt = request.args.get('format', 'mp4')
    if not url:
        return jsonify({'error': 'URL missing'}), 400
    try:
        yt = YouTube(url)
        file_id = str(uuid.uuid4())
        filename = f"{file_id}.{fmt}"
        if fmt == 'mp3':
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(filename=filename)
        else:
            video_stream = yt.streams.get_highest_resolution()
            video_stream.download(filename=filename)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == '__main__':
    app.run(debug=True)
