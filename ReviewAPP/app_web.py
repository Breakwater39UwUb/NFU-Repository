from flask import Flask, request, render_template
from markupsafe import escape
app = Flask(__name__, template_folder='web')
@app.route('/', methods=['POST','GET'])
def Comment():
    if request.method == "POST":
       comment = request.form.get("Comment")
       return f'{comment}'
    return render_template('main.html')
    
def FoodpandaLink():
    if request.method == "POST":
       foodpandalink = request.form.get("FoodpandaLink")
       return f'{foodpandalink}'
    return render_template('main.html')

def GoogleLink():
    if request.method == "POST":
       googlelink = request.form.get("GoogleLink")
       return f'{googlelink}'
    return render_template('main.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
