import urllib.request
import feedback
import time

source = """<html>
<head>
  <title>Seekers website coming soon</title>
</head>
<body>
  <h1>Hello Metaverse.....</h1>
</body>
</html>"""

url = "http://cet-bm.neea.edu.cn/"

if __name__ == '__main__':
    while 1:
        try:
            fp = urllib.request.urlopen(url)
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            time.sleep(60 * 30)
            if mystr != source:
                feedback.feedback("网站内容发生变动" + url, "M", 532013188)
                break
        except Exception as e:
            feedback.feedback("监控程序异常" + e + url, "M", 532013188)
            break
        finally:
            fp.close()
