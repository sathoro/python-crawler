import requests, urlparse, json, lxml
from bs4 import BeautifulSoup

class Crawler(object):
	def __init__(self, headers={}, cookies={}):
		self.session = requests.session()

		headers.update({
			'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
		})

		self.session.headers.update(headers)
		self.add_to_cookies(cookies)

	def visit(self, url):
		return self._get(url)

	def submit(self, form, data={}, headers={}, method=None):
		data = self._merge(form.data, data)

		if method == 'get' or form.type == 'get':
			return self._get(form.url, data, headers)
		else:
			return self._post(form.url, data, headers)

	def get_forms(self, url):
		response = self._get(url)

		# update the url in case we were redirected
		# example: http://github.com/login redirects to https://github.com/login
		url = response.url

		html = BeautifulSoup(response.text, 'lxml')
		forms = []
		for form in html.find_all('form'):
			inputs = []
			for _input in form.find_all('input'):
				inputs.append({
					'name': _input['name'] if 'name' in _input.attrs else '',
					'value': _input['value'] if 'value' in _input.attrs else '',
					'type': _input['type'] if 'type' in _input.attrs else ''
				})

			method = form['method'].lower() if 'method' in form.attrs else 'get'
			forms.append(CrawlerForm(url, form['action'], inputs, method))

		return forms

	# return dictionary of cookies
	def get_cookies(self):
		return requests.utils.dict_from_cookiejar(self.session.cookies)

	# dictionary to add/overwrite cookies
	def add_to_cookies(self, cookie):
		self.session.cookies = requests.utils.cookiejar_from_dict(self._merge(self.get_cookies(), cookie))

	# return dictionary of headers
	def get_headers(self):
		return dict(self.session.headers)

	# dictionary to add/overwrite headers
	def add_to_headers(self, header):
		self.session.headers = self._merge(self.session.headers, header)

	def _request(self, method, url, params={}, headers={}, cookies={}):
		headers = self._merge(self.session.headers, headers)

		cookies = self._merge(self.get_cookies(), cookies)
		if method == 'get':
			return self.session.request(method.upper(), url, params=params, headers=headers, cookies=cookies)
		else:
			return self.session.request(method.upper(), url, data=params, headers=headers, cookies=cookies)

	def _get(self, url, *arg):
		return self._request('get', url, *arg)

	def _post(self, url, *arg):
		return self._request('post', url, *arg)

	def _merge(self, dict1, dict2):
		return dict(dict1.items() + dict2.items())

class CrawlerForm(object):
	def __init__(self, url, action, inputs, type):
		self.url = urlparse.urljoin(url, action)
		self.data = {}

		for _input in inputs:
			if _input['name'] is not '':
				self.data[_input['name']] = _input['value']

		if type != 'get' and type != 'post':
			raise Exception('Form type invalid: \'%s\'')

		self.type = type

	def __str__(self):
		return json.dumps({
			'url': self.url,
			'data': self.data,
			'type': self.type
		})