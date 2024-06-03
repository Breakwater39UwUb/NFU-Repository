from flask import Flask, request, render_template, url_for, send_from_directory
import json
from os.path import sep
from urllib.parse import quote
from my_Packages import utils
import my_Packages.review_plot as rplt
from my_Packages.scraper import get_reviews
from my_Packages.predictor_1 import review_predict
from my_Packages.predictor_2 import review_analyze
from my_Packages.db_update import insert_review, get_years

flask_template_path = 'web/'	# web/templates/
home_page = 'main.html'	# main.html
predict_page = 'predict.html'
new_predict_page = 'new_predict.html'
analysis_page = 'analysis.html'
chart_html= 'chart.html'
user_rating = 1
review_file = ''
passed = 0

app = Flask(__name__,
            template_folder=flask_template_path,
            static_folder=flask_template_path,
            static_url_path='')
app.debug = True

@app.route("/")
def Home():
    return render_template('main.html')

@app.route("/get_Star", methods=['GET','POST'])
def get_Star():
    '''Get user review rating for multi-class classification'''
    global user_rating
    user_rating  = int(request.get_json())
    return render_template(predict_page)

# TODO: Remove this API due to it is not accessed
# Ask 1234AWEOOOOOO before removing


# TODO: Ask 1234AWEOoooo for the feature of this API
@app.route("/get_Passed", methods=['GET','POST']) # Funtion to handle get Passed value
def get_Passed():
    global passed
    passed = request.get_json()
    print (passed)

    return render_template(predict_page)

# TODO: Rename this API for better readability
# TODO: Change main.html to handle renamed API
@app.route('/get_Change', methods=['POST','GET'])  
def get_Change():    
    '''Show BERT multiclass classification prediction

    Get rating and review from user by form.

    Returns
    user_rating: string
        original user rating
    bert_rating: string
        number in range 0 to 2(class number)
        
        - '0', Negative (1, 2 star)
        - '1', Neutral (3 star)
        - '2', Positive (4, 5 star)
    '''
    if request.method == "POST":
        data = request.form.get("txtbox1")
        
    answer = review_predict(q_input=data)
    
    if answer in utils.rating_dict:
        bert_rating, valid_ratings = utils.rating_dict[answer]
        if user_rating in valid_ratings:
            bert_rating += '且評分與評論相符。'
            insert_review(user_rating, data)
        else:
            bert_rating += '但評分與評論不符。'
    return render_template(new_predict_page, users = user_rating, berts = bert_rating, user_txt = data)




@app.route( "/get_Url" , methods=['POST','GET'])
def get_Url():
    if request.method == "POST":
        data_url = request.form.get("myTextarea")
        # TODO: Add boolean to check if data_url is entered before
        # If True, skip scraping.
        if data_url is None :
            raise ValueError('Please input a url under "Overview tab".')
        if 'google' in data_url:
            platform = 'Googlemaps'
        else:
            platform = 'Foodpanda'
        
        form_time_start = request.form.get('time_start') 
        form_time_end = request.form.get('time_end')
        # TODO: Get year from web
        YEAR = '2023'

        if form_time_start is not None:
            form_time_start, form_time_end = utils.sort_times(form_time_start, form_time_end)
            # month_range: '2003-05 2004-03'
            month_range = f'{form_time_start} {form_time_end}'
            YEAR = None
        
        if YEAR is not None:
            month_range = None


    
    global review_file
    try:
        # TODO: file format should select by user
        # may remove the check_cache until client web have proper function to handle
        review_file = get_reviews(url=data_url, webname=platform, format='json', check_cache=True)
    except:
        raise Exception('Failed at get_reviews()')
    
    # TODO: Change filename to dynamic to avoid redundant image creation
    # Check prediction cache for plot
    prediction_file = utils.check_predict_cache(review_file)
    if prediction_file is None:
        predictions = review_analyze(file_path=review_file)
    else:
        # TODO: Read predictions from file
        predictions = utils.read_predictions(prediction_file)
    
    analysis = calculate_labels(predictions)

    # TODO: Add statement to determine filtering month or year
    if month_range is not None:
        filtered_data = [d for d in predictions  if d[2].split('/')[1] != '']
        
        labels = [rplt.FOOD, rplt.PRICE, rplt.SERVICE, rplt.ENV]
        label_names = ['Food', 'Price', 'Service', 'Environment']
        chart_urls = {}

        for label, name in zip(labels, label_names):
            chart_urls[name] = process_chart_by_month(filtered_data, label, month_range, review_file)
    
        return render_template(chart_html,
                            str1=analysis[0], str2=analysis[1], str3=analysis[2], str4=analysis[3],
                            Food = chart_urls['Food'],
                            Price = chart_urls['Price'],
                            Service = chart_urls['Service'],
                            Environment = chart_urls['Environment'],
                            passed = passed
                            )
    # get review on given year
    if YEAR is not None:
        filtered_data = [d for d in predictions if YEAR in d[2].split('/')]

        chart_url = rplt.sort_by_year(filtered_data, YEAR, review_file)
        chart_url = chart_url.split(sep)[1:]
        chart_url = '/'.join(chart_url)
        chart_url = url_for('serve_image', filename=chart_url)
        # return render_template(chart_html,
        #                        str1=analysis[0], str2=analysis[1], str3=analysis[2], str4=analysis[3],
        #                        YEARLY = chart_url)
        return (chart_url, 200)

    

@app.route('/<path:filename>')
def serve_image(filename):
    print('--------------------------------------------------------')
    print(filename)
    return send_from_directory('', filename)

@app.route('/show_years', methods=['POST','GET'])
def show_years():
    '''Get all review from given year
    
    year format in YYYY/
    '''

    global review_file
    if request.method == "POST":
        YJ_path = review_file.split(sep)
        dir_ = utils.create_dir(YJ_path[1], ['web', 'charts'])
        YJ_path = 'YEARS' + YJ_path[1] + '.json'
        YJ_path = sep.join([dir_, YJ_path])

        years = get_years(review_file)
        with open(YJ_path, 'w') as year_file:
            json.dump(years, year_file, ensure_ascii=False, indent=4)

        year_file_url = YJ_path.split(sep)
        year_file_url = '/'.join(year_file_url)
        return (year_file_url, 200)

def process_chart_by_month(data: list,
                           label: int,
                           month_range: str,
                           file_path: str):
    chart_url = rplt.plot_by_label(data, label, month_range, file_path)
    chart_url = chart_url.split(sep)[1:]
    chart_url = '/'.join(chart_url)
    return url_for('serve_image', filename=chart_url)

@app.errorhandler(Exception)
def handle_exception(error):
    # now you're handling non-HTTP exceptions only
    return render_template('error.html', error_message=str(error)), 500
    

def calculate_labels(labels: list[tuple]):
    '''Calculate all labels and show results on web

    labels: list of tuples
        [(label, text, time), ]

    4 labels:
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

def debug_type(var):
    print('----------')
    print(f'Type: {type(var)}')
    if type(var) is list:
        print(f'type(var[0]): {type(var[0])}')
        print(f'var[0]: {var[0]}')
    else:
        print(f'value: {var}')

if __name__ == "__main__":
    app.run(host='10.1.1.22', port=8901)
