from crawler import Crawler
from bs4 import BeautifulSoup

crawler = Crawler()

# returns a list of the available forms
forms = crawler.get_forms('https://github.com/login')

# submits the login form
crawler.submit(forms[1], {'login': '---', 'password': '---'})

# just a simple GET request, returns a response object
response = crawler.visit('https://github.com')

# lets use BeautifulSoup to parse the response text
html = BeautifulSoup(response.text, 'lxml')

# get a list of our repositories by scraping the html
for repo in html.find(id='repo_listing').find_all('span', {'class': 'repo'}):
	print repo.text

print '\n', crawler.get_cookies()
print '\n', crawler.get_headers()