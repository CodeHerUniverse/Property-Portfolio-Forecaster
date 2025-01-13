from flask import Flask, jsonify, request
from db_utils import get_property_list, get_feature_list, get_properties_by_bedroom_nr, add_property, add_renovations, amend_feature_price, get_renovations_tracker, get_property_list_after_renos

# Create the Flask App
app = Flask(__name__)

# Defining a route for the home page
@app.route('/')
def index():
    #Welcome Message
    return "Welcome to the Property Portfolio & Forecaster!"

# http://127.0.0.1:5001/



# Defining a route to collect a list of all the properties available
@app.route('/all_properties')
def get_properties():
    try:
        # get_property_list() is defined under db_utils and is called as a "module"
        res = get_property_list()
        return jsonify(res)
    
    # Error handling if the function cannot be called
    except Exception as e:
        return jsonify({"error": "Failed to get property list. " + str(e)}), 500

# http://127.0.0.1:5001/all_properties



# Defining a route to collect a list of all the properties available, which also includes their current values after any renovations are saved
@app.route('/all_properties_after_renovations')
def get_prop_list_after_renos():
    try:
        # get_property_list_after_renos() is defined under db_utils and is called as a "module"
        res = get_property_list_after_renos()
        return jsonify(res)
    
    #Error handling if the function cannot be called
    except Exception as e:
        return jsonify({"error": "Failed to get property list after renovations. " + str(e)}), 500

# http://127.0.0.1:5001/all_properties_after_renovations



# Defining a route to collect a list of all the properties available, if they meet a criteria - this criteria is the number of bedrooms
@app.route('/properties_by_bedroom_nr/<bd_number>')
def get_prop_by_bed(bd_number):
    try:
        # get_properties_by_bedroom_nr() is defined under db_utils and is called as a "module"
        res = get_properties_by_bedroom_nr(bd_number)
        # If there are no properties with the given number of bedrooms
        if not res:
            # return error message
            return jsonify({"error": "No properties found with that number of bedrooms"}), 404
        return jsonify(res)
    
    # If the input is not a valid input
    except ValueError:
        return jsonify({"error": "Invalid input for bedroom number"}), 400
    
    # For any other instance
    except Exception as e:
        return jsonify({"error": "Failed to get properties by bedroom number. " + str(e)}), 500
        
# http://127.0.0.1:5001/properties_by_bedroom_nr/2



# Defining a route to collect a list of all the renovation features available in the system.
@app.route('/renovation_features')
def get_features_available_for_calc():
    try:
        # get_feature_list() is defined under db_utils and is called as a "module"
        res = get_feature_list()
        return jsonify(res)
    
    # Error handling if the function cannot be called
    except Exception as e:
        return jsonify({"error": "Failed to get renovation features. " + str(e)}), 500

# http://127.0.0.1:5001/renovation_features



# Defining a route to collect a list of all the renovation features available in the system.
@app.route('/renovations_tracker/<int:property_id>')
def get_renovations(property_id):
    try:
        # get_renovations_tracker() is defined under db_utils and is called as a "module"
        res = get_renovations_tracker(property_id)
        # If there are no properties with the given number of bedrooms
        if not res:
            return jsonify({"error": f"No renovations found for property ID {property_id}"}), 404
        
        return jsonify(res)
    
    # Error handling if the function cannot be called
    except Exception as e:
        return jsonify({"error": f"Failed to get renovations for property ID {property_id}. " + str(e)}), 500

# http://127.0.0.1:5001/renovations_tracker/2   -- This will only work once some renovations are logged in the system. Please see snippets



# Defining a route to add (POST) new properties to the property_list table.
@app.route('/add_property', methods=['POST'])
def add_prop():  

    # property variable stores the JSON data received from incoming POST request       
    property = request.get_json()

    try:
        # transposes the values in the JSON file into variables to be used in the next function
        postcode = property['postcode']
        number_bedrooms = property['number_bedrooms']
        purchase_price = property['purchase_price']
        purchase_date = property['purchase_date']

        # add_property() is defined under db_utils and is called as a "module"
        add_property(postcode, number_bedrooms, purchase_price, purchase_date)

        # Success message
        return jsonify({"message": "Property added successfully"}), 201

    # Error handling if the function cannot be called
    except Exception as e:
        return jsonify({"error": "Failed to add property. " + str(e)}), 500
            


# Defining a route to add (POST) new renovatins to the renovations_tracker table.
@app.route('/add_renovations', methods=['POST'])
def add_reno():   

    # reno variable stores the JSON data received from incoming POST request             
    reno = request.get_json()

    try:
        # transposes the values in the JSON file into variables to be used in the next function
        property_id = reno['property_id']
        feature = reno['feature']
        price_paid_for_feature = reno['price_paid_for_feature']
        current_evaluation = reno['current_evaluation']
        feature_added_date = reno['feature_added_date']
        property_value_after_renovation = reno['property_value_after_renovation']

        # add_renovations() is defined under db_utils and is called as a "module"
        add_renovations(property_id, feature, price_paid_for_feature, current_evaluation, feature_added_date, property_value_after_renovation)

        # Success Message
        return jsonify({"message": "Renovation(s) added successfully"}), 201
    
    # Error handling if the function cannot be called
    except Exception as e:
        return jsonify({"error": "Failed to add property. "+str(e)}), 500
            
    

# Defining a route to amend (PUT) the price paid for certain features in the renovations_tracker table.
@app.route('/update_feature_price', methods=['PUT'])
def update_feature_price():

    # up_feature variable stores the JSON data received from incoming POST request 
    up_feature = request.get_json()
    try:

        # transposes the values in the JSON file into variables to be used in the next function
        property_id = up_feature['property_id']
        renovation_to_amend = up_feature['renovation_to_amend']
        new_price_paid_for_feature  = up_feature['new_price_paid_for_feature']

        # amend_feature_price() is defined under db_utils and is called as a "module"
        amend_feature_price(new_price_paid_for_feature, property_id, renovation_to_amend)

        #Success Message
        return jsonify({"message": "Renovation and dependent rows updated successfully"}), 200
    
    # Error handling if the function cannot be called
    except Exception as e:
        return jsonify({"error": "Failed to add property. "+str(e)}), 500



# Check to see if this script is being run directly or being imported as a module
if __name__ == '__main__':
    # app.run() starts the Flask developent server. 
    # debug = True enables Flask's debug mode which allows automatic reloading if there are changes in the code.
    app.run(debug=True, port=5001)