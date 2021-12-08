from urllib.request import urlopen

url = "https://indianexpress.com/article/cities/bangalore/karnataka-former-iaf-officer-killing-wife-kids-11-years-7659589/"

page = urlopen(url)
print(page)

html_bytes = page.read()
html = html_bytes.decode("utf-8")

print(html)