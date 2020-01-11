import web
import base64
import pycld2 as cld2
import json

"""
Define tupel for webserver path
"""
urls = (
    '/detectLang', 'detectLang'
)
app = web.application(urls, globals())

class detectLang:
    """
    Class handling get requests directed to the detectLang class.
    """
    def GET(self):
        get_input = web.input()
        decoded_text = str(base64.urlsafe_b64decode(get_input["text"].encode("utf-8")), "utf-8")
        isReliable, textBytesFound, details = cld2.detect(decoded_text)
        language, short, confidence, idk = details[0]
        return json.JSONEncoder().encode({"reliable": isReliable, "language": language, "short": short, "prob": confidence})

if __name__ == "__main__":
    app.run()
