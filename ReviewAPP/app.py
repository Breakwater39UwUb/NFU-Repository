from flask import Flask, request, render_template, json, url_for
import os
from Packages.scraper import get_reviews
from Packages.predictor_1 import review_predict
from Packages.predictor_2 import predict_multiclass
flask_template_path = 'web/'	# web/templates/
home_page = 'web.html'	# main.html
predict_page = 'predict.html'
analysis_page = 'analysis.html'
platform = ''
user_rating = 1
bert_rating = 1

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
	'''
	user_rating = request.form['star'] + '星'
	txt = [request.form['txt']]
	bert_rating = review_predict(txt) + '星'

	return render_template(predict_page, users = user_rating, berts = bert_rating)

@app.route("/get_url", methods=['GET', 'POST'])
def get_url():
	'''
	Get url for web scraper
	then call web scraper
	calculate all label and show results on web
	'''
	scrape_url = request.get_json()
	if scrape_url is None :
		raise ValueError('Please input a url under "Overview tab".')
	
	if scrape_url == 'test':
		print(scrape_url)
		return request.get_json()
	
	if platform == 'Googlemaps':
		print('Select Googlemaps')
		get_reviews(url=scrape_url, webname=platform)

	if platform == 'Foodpanda':
		print('Select foodpanda')
		get_reviews(url=scrape_url, webname=platform)

	print('return analysis results')
	return render_template(analysis_page)

@app.route("/get_platform", methods=['GET','POST'])
def get_platform():
	'''Set platform to set scrape web
	Foodpanda | Googlemaps
	'''
	# output = request.get_json()
	# global platform
	# platform = output
	return ('', 204)

if __name__ == "__main__":
	app.run(port=8900)
