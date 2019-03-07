from urllib.request import urlopen
 
 
def index(url):
    def get():
        return urlopen(url).read()
 
    return get
 
 
baidu = index('http://www.baidu.com')
print(baidu().decode('utf-8'))
