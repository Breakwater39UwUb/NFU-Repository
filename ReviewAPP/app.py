from flask import Flask, request, render_template, url_for, send_from_directory
from os.path import sep
from urllib.parse import quote
from my_Packages import utils
import my_Packages.review_plot as rplt
from my_Packages.scraper import get_reviews
from my_Packages.predictor_1 import review_predict
from my_Packages.predictor_2 import review_analyze
from my_Packages.db_update import insert_review

flask_template_path = 'web/'	# web/templates/
home_page = 'main.html'	# main.html
predict_page = 'predict.html'
new_predict_page = 'new_predict.html'
analysis_page = 'analysis.html'
chart_html= 'chart.html'
user_rating = 1

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
@app.route("/get_Date", methods=['GET','POST'])
def get_Date():
    '''Set platform to set scrape web
    Foodpanda | Googlemaps
    '''
    global dateTEST
    dateTEST  = request.get_json()
    print (dateTEST)
    return render_template(predict_page)

# TODO: Ask 1234AWEOoooo for the feature of this API
@app.route("/get_Passed", methods=['GET','POST']) # Funtion to handle get Star value
def get_Passed():
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
    
    # TODO: Change return string for better presentation of results
    if answer == '0':
        bert_rating = '負向(1,2 星)' # Negative (1, 2 star) 
        #英文子太長超出去，所以改中文
    if answer == '1':
        bert_rating = '中立(3 星)' # Neutral (3 star)
        #英文子太長超出去，所以改中文
    if answer == '2':
        bert_rating = '正向(4,5 星)' # Positive (4, 5 star)
        #英文子太長超出去，所以改中文
    return render_template(new_predict_page, users = user_rating, berts = bert_rating, user_txt = data)




@app.route( "/get_Url" , methods=['POST','GET'])
def get_Url():
    if request.method == "POST":
        data_url = request.form.get("myTextarea")  
        if data_url is None :
            raise ValueError('Please input a url under "Overview tab".')
        if 'google' in data_url:
            platform = 'Googlemaps'
        else:
            platform = 'Foodpanda'
        
        form_time_start = request.form.get('time_start') 
        form_time_end = request.form.get('time_end')
        form_time_start, form_time_end = utils.sort_times(form_time_start, form_time_end)
        # month_range: '2003-05 2004-03'
        month_range = f'{form_time_start} {form_time_end}'

    
    try:
        # TODO: file format should select by user
        # may remove the check_cache until client web have proper function to handle
        review_file = get_reviews(url=data_url, webname=platform, format='json', check_cache=True)
    except:
        raise
        return ('', 500)
    
    # TODO: Change filename to dynamic to avoid redundant image creation
    # Check prediction cache for plot
    prediction_file = utils.check_predict_cache(review_file)
    if prediction_file is None:
        predictions = review_analyze(file_path=review_file)
    else:
        # TODO: Read predictions from file
        predictions = utils.read_predictions(prediction_file)
    filtered_data = [d for d in predictions  if d[2].split('/')[1] != '']

    # TODO: Read cached predictions file to plot charts
    food_label_chart = rplt.plot_by_label(filtered_data, rplt.FOOD, month_range, review_file)
    price_label_chart = rplt.plot_by_label(filtered_data, rplt.PRICE, month_range, review_file)
    serve_label_chart = rplt.plot_by_label(filtered_data, rplt.SERVICE, month_range, review_file)
    envir_label_chart = rplt.plot_by_label(filtered_data, rplt.ENV, month_range, review_file)
    
    food_label_chart = food_label_chart.split(sep)[1:]
    price_label_chart = price_label_chart.split(sep)[1:]
    serve_label_chart = serve_label_chart.split(sep)[1:]
    envir_label_chart = envir_label_chart.split(sep)[1:]

    food_label_chart = '/'.join(food_label_chart)
    price_label_chart = '/'.join(price_label_chart)
    serve_label_chart = '/'.join(serve_label_chart)
    envir_label_chart = '/'.join(envir_label_chart)

    food_label_url = url_for('serve_image', filename=food_label_chart)
    price_label_url = url_for('serve_image', filename=price_label_chart)
    serve_label_url = url_for('serve_image', filename=serve_label_chart)
    envir_label_url = url_for('serve_image', filename=envir_label_chart)
    print('-----------------', envir_label_chart)
    
    analysis = calculate_labels(predictions)
    return render_template(chart_html,
                        str1=analysis[0], str2=analysis[1], str3=analysis[2], str4=analysis[3],
                        Food = food_label_url,
                        Price = price_label_url,
                        Service = serve_label_url,
                        Environment = envir_label_url
                        )

@app.route('/<path:filename>')
def serve_image(filename):
    print('--------------------------------------------------------')
    print(filename)
    return send_from_directory('', filename)

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
    app.run(port=8900)
