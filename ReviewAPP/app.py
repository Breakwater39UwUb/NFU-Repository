from flask import Flask, request, render_template, json
import os
from Packages.scraper import get_reviews
flask_template_path = 'web/'	# web/templates/
home_page = 'web.html'	# main.html
predict_page = 'predict.html'
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

@app.route("/comment", methods=['POST'])
def comment():
	comment = request.form['Comment']
	if comment:
		print(request.form['Comment'])
		return comment  
	

	link = request.form['Link']
	if link:
		print(request.form['Link'])
		try:
			get_reviews(url=link)
		except Exception:
			print(os.getcwd())
		finally:
			return link
		
@app.route("/get_user_review", methods=['POST'])
def get_user_review():
	
	print(request.form['star'])
	print(request.form['txt'])
	data = request.form['star']
	return render_template(predict_page, DATA = data)

@app.route("/get_url", methods=['GET', 'POST'])
def get_url():
	scrape_url = request.get_json()
	if scrape_url is None :
		raise ValueError('Please input a url under "Overview tab".')
	
	if platform == 'Googlemaps':
		print(scrape_url)
		get_reviews(url=scrape_url)

	if platform == 'Foodpanda':
		pass

	return render_template(home_page)

@app.route("/get_platform", methods=['GET','POST'])
def get_platform():
	output = request.get_json()
	global platform
	platform = output
	print(platform)
	return render_template(home_page)
        
if __name__ == "__main__":
	app.run(port=8900)
