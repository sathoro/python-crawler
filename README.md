python-crawler
====

This is a small library intended for finding forms and submitting them with custom data. The primary use case would be for websites that don't have an API. `main.py` has example code for logging into `github.com` to get a list of your repositories. CSRF tokens are often required for forms and by using the `get_forms(url)` method it will automatically populate any anti-CSRF tokens to send with the request.

### Setup

    pip install beautifulsoup4
    pip install lxml

### Example Usage

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
	
### Custom Cookies and/or Headers

Optionally pass a dictionary of headers and/or cookies when instantiating the `Crawler` object to have them included with requests. Example usage: you are already authenticated on a website and would like to use your session cookie.

    headers = {
		'user-agent': 'not-a-bot'
	}

	cookies = {
		'session_id': 'Mp8a8ILEdasfsafau6crICX-1ceAFvVvaWlB'
	}

	crawler = Crawler(headers, cookies)
	
### Other Methods

    crawler.add_to_cookies({'foo': 'bar'})
	crawler.get_cookies()
	
	crawler.add_to_headers({'foo': 'bar'})
	crawler.get_headers()
