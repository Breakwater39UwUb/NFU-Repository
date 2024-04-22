from flask import Flask, request, render_template, json, url_for
import os
from my_Packages.scraper import get_reviews
from my_Packages.predictor_1 import review_predict
from my_Packages.predictor_2 import review_analyze
flask_template_path = 'web/'	# web/templates/
home_page = 'web.html'	# main.html
predict_page = 'predict.html'
analysis_page = 'analysis.html'
platform = ''
user_rating = 1	# may delete this
bert_rating = 1	# may delete this

app = Flask(__name__,
			template_folder=flask_template_path,
			
			static_folder=flask_template_path,
			static_url_path='')
app.debug = True

@app.route("/")
def Home():
	return render_template(home_page)

@app.route("/get_user_review", methods=['POST'])
def get_user_review():
	'''
	Show BERT prediction

	Predict one review for 30 times and return the mode result
	'''

	user_rating = request.form['star'] + '星'
	txt = [request.form['txt']]
	answers = []
	for t in range(30):
		answers.append(review_predict(q_inputs=txt))
	bert_rating =  max(set(answers), key=answers.count) + '星'

	return render_template(predict_page, users = user_rating, berts = bert_rating)

@app.route("/get_predict")
def get_predict():
	'''Get reviews on the given url,
	predict all labels of reviews and
	calculate all label and show results on web
	'''

	try:
		# may remove the check_cache until client web have proper function to handle
		review_file = get_reviews(url=scrape_url, webname=platform, format= 'json', check_cache=True)
		predictions = review_analyze(file_path=review_file)
		debug_type(predictions)
		analysis = calculate_labels(predictions)
		return render_template(analysis_page,
						 str1=analysis[0], str2=analysis[1], str3=analysis[2], str4=analysis[3])
	except:
		raise Exception(f'Failed to get review on\n{scrape_url}\n')

def calculate_labels(labels: list):
	'''Calculate all labels and show results on web

	sum of labels

		[food, price, service, environment]
	'''

	analysis = [0, 0, 0, 0]

	for label in labels:
		index = 0
		for value in label[0]:
			if value:
				analysis[index] += 1
			index += 1

	return analysis

@app.route("/get_platform", methods=['GET','POST'])
def get_platform():
	'''Set platform to set scrape web
	Foodpanda | Googlemaps
	'''

	global platform
	platform = request.get_json()
	return ('', 204)

@app.route("/get_url", methods=['GET', 'POST'])
def get_url():
	'''Get url for web scraper
	'''
	
	global scrape_url
	scrape_url = request.get_json()
	
	if scrape_url is None :
		raise ValueError('Please input a url under "Overview tab".')
	return ('', 204)

def read_review_file(FILE: str):
	'''Read lines from file for the BERT
	'''

	TEXT = []

	if FILE.split('.')[-1] == 'json':
		with open(FILE, 'r', encoding='utf-8') as file:
			data = json.load(file)
			for line in data:
				TEXT.append(line['comment'])
		return TEXT

def debug_type(var):
	print('----------')
	print(f'Type: {type(var)}')
	if type(var) is list:
		print(f'type(var[0]): {type(var[0])}')
		print(f'var[0]: {var[0]}')
	else:
		print(f'value: {var}')

if __name__ == "__main__":
	app.run(port=8900)
