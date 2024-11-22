# app/views.py

from django.shortcuts import render
import pickle
import os
import numpy as np

def predict(request):
    if request.method == 'POST':
        # Extract user input from the form
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        bmi = request.POST.get('bmi')
        children = request.POST.get('children')
        smoker = request.POST.get('smoker')
        region = request.POST.get('region')
        
        # Convert input values to appropriate types
        try:
            age = int(age)
            sex = int(sex)  # Assuming sex is entered as '1' for male and '0' for female
            bmi = float(bmi)
            children = int(children)
            smoker = int(smoker)  # Assuming smoker is entered as '1' for yes and '0' for no
            region = int(region)  # Assuming region is entered as a numerical value
        except ValueError:
            return render(request, 'predict.html', {'error': 'Invalid input values. Please enter valid numeric data.'})
        
        # Ensure the input data matches the expected number of features (8 in this case)
        # Adjust this according to your model's requirements
        input_data = np.array([[age, sex, bmi, children, smoker, region, 0, 0]])  # Adjusted to match 8 features
        
        # Load the model
        model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        
        # Make prediction
        prediction = model.predict(input_data)
        
        # Render the result template with prediction value
        return render(request, 'result.html', {'prediction': prediction[0]})
    
    # If not a POST request, render the form template
    return render(request, 'predict.html')
