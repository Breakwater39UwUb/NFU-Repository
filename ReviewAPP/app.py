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

bert_meals_rating = 0
bert_serve_rating = 1
bert_surroundings_rating = 2
bert_price_rating = 3



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
	bert_rating =  "5" + '星'

	return render_template(predict_page, users = user_rating, berts = bert_rating)



@app.route("/get_predict")
def get_predict():
	if platform == 'Googlemaps':
		print('Select Googlemaps')
		try:
			get_reviews(url=scrape_url, webname=platform)
		except Exception:
			print(os.getcwd())
		finally:
			return render_template('analysis.html',
			str1=bert_meals_rating,str2=bert_serve_rating,str3=bert_surroundings_rating,str4=bert_price_rating)
		
	if platform == 'Foodpanda':
		print('Select foodpanda')
		try:
			get_reviews(url=scrape_url, webname=platform)
		except Exception:
			print(os.getcwd())
		finally:
			return render_template('analysis.html',
			str1=bert_meals_rating,str2=bert_serve_rating,str3=bert_surroundings_rating,str4=bert_price_rating)		
	

@app.route("/get_platform", methods=['GET','POST'])
def get_platform():
	'''Set platform to set scrape web
	Foodpanda | Googlemaps
	'''
	output = request.get_json()
	global platform
	platform = output
	return ('', 204)

@app.route("/get_url", methods=['GET', 'POST'])
def get_url():
	'''
	Get url for web scraper
	then call web scraper
	calculate all label and show results on web
	'''
	output = request.get_json()
	global scrape_url
	scrape_url = output
	
	if scrape_url is None :
		raise ValueError('Please input a url under "Overview tab".')

	print('return analysis results')
	return render_template(analysis_page)

if __name__ == "__main__":
	app.run(port=8900)
