from flask import Flask,request, render_template,send_file,after_this_request
from pytube import YouTube
import tempfile
from io import BytesIO
import shutil


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/link", methods=['GET'])
@app.route("/res", methods=['POST'])
def download_video():
    if request.method == 'POST':
        # URL of the YouTube video to download
        video_url = request.form['link']
        res=request.form['res']
        # Fetch the YouTube video using pytube
        yt = YouTube(video_url)
        try:
            stream = yt.streams.filter(mime_type="video/mp4", resolution=res).first()
        except:
            return "<h1>Some thing went wrong . go back and click download again</h1>"
         # Create a temporary directory within the Flask project root directory
        temp_dir= tempfile.TemporaryDirectory(dir=app.root_path+'/temp')
        video_path = stream.download(temp_dir.name) 
        # Return the video file as an HTTP response to the user
        with open(video_path, 'rb') as f:
            video_bytes = BytesIO(f.read())
        return send_file(video_bytes,as_attachment=True, download_name=yt._title+".mp4", mimetype="video/mp4")
        
            

    else:
        link = request.args.get('url')
        print(link)
        video=YouTube(link)
        thumbnail=video.thumbnail_url
        available_resolutions = list( {stream.resolution for stream in video.streams.filter(mime_type="video/mp4",type="video",file_extension='mp4').order_by('resolution')})
        return render_template('index.html',resolutions=available_resolutions,thumbnail=thumbnail,link=link)
        

if __name__ == '__main__':
    app.run(debug=True)
