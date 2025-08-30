from flask import Flask, request, render_template
import yt_dlp

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template("index.html", error="No URL provided")

        ydl_opts = {"quiet": True, "skip_download": True}
        try:
            with yt_dlp.YoutubeDL({"quiet": True, "skip_download": True}) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get("formats", [])
                # Progressive formats have both audio+video
                progressive = [f for f in formats if f.get("acodec") != "none" and f.get("vcodec") != "none"]
                best = progressive[-1] if progressive else None
                if not best:
                    return render_template("index.html", error="No playable format found")
                video_url = best["url"]
                title = info.get("title", "video")
                return render_template("result.html", title=title, video_url=video_url)

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
