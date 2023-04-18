# Importing essential libraries and modules

from flask import Flask, render_template, request, Markup
import numpy as np
import pandas as pd
import requests
import pickle
import io

# ==============================================================================================

# -------------------------LOADING THE TRAINED MODELS -----------------------------------------------



# Loading crop recommendation model

crop_recommendation_model_path = 'D:\\IET_Groundwater\\models\\RandomForest.pkl'
crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))


# =========================================================================================

# Custom functions for calculations





# ===============================================================================================
# ------------------------------------ FLASK APP -------------------------------------------------


app = Flask(__name__)

# render home page


@ app.route('/')
def home():
    title = 'Hydro.AI - Home'
    return render_template('index.html', title=title)

# render crop recommendation form page


@ app.route('/crop-recommend')
def crop_recommend():
    title = 'Hydro.AI - Crop Recommendation'
    return render_template('crop.html', title=title)






# ===============================================================================================

# RENDER PREDICTION PAGES

# render crop recommendation result page


@ app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    title = 'Hydro.AI - Crop Recommendation'
    data_file = pd.read_excel('D:\\IET_Groundwater\\New Dataset.xlsx')
    category={'Critical': 0, 'Over-Exploited': 1, 'Safe': 2, 'Saline': 3, 'Semi-Critical': 4}
    soil={'Alluvial': 0, 'Alluvial ': 1, 'Alluvial Loam': 2, 'Alluvial Sandy Loam': 3, 'Black': 4, 'Black Clay': 5, 'Black Loamy': 6, 'Clay': 7, 'Laterite ': 8, 'Loam': 9, 'Red': 10, 'Red Clay': 11, 'Red, Black': 12, 'Saline,Laterite': 13, 'Sandy': 14, 'Sandy Loam': 15, 'Sandy Saline': 16, 'Volcanic': 17}

    if request.method == 'POST':       

        #state = request.form.get("state")
        city = request.form.get("city")
        block=request.form.get("block")
        test_cat=float(data_file.loc[data_file['Block']==block,'Categorization'].map(category)) 
        test_soil=float(data_file.loc[data_file['Block']==block, 'Soil'].map(soil) )   
            #temperature, humidity = weather_fetch(city)
        data = np.array([[test_cat,test_soil]])
        my_prediction = crop_recommendation_model.predict(data)
        final_prediction = my_prediction[0]
        categ=data_file.loc[data_file['Block']==block,'Categorization']
        str1=" "
        catgor=str1.join(categ.values)
        return render_template('crop-result.html', prediction=final_prediction, place=block, category=catgor,title=title)

    else:

            return render_template('try_again.html', title=title)






# ===============================================================================================
if __name__ == '__main__':
    app.run(debug=False)
