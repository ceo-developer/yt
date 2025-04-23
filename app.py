from flask import Flask, request, jsonify
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "YouTube Downloader API is running!"})

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL is missing'}), 400

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        download_link = stream.url

        return jsonify({
            'title': yt.title,
            'author': yt.author,
            'download_url': download_link,
            'filesize': stream.filesize,
            'resolution': stream.resolution
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
