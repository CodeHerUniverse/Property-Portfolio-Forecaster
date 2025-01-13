import requests
import json
from datetime import datetime


# Function to view properties - I am keeping this separate from get_properties so I can call it separately if I just need to view and not select.
def view_properties():

    try:

        # Get request
        result = requests.get('http://127.0.0.1:5001/all_properties',
        headers={'content-type': 'application/json'})
        api_result = result.json() 

    # Error Handling - let user know if Flask App is not running and advises to run it first.
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the Flask server. Please ensure the Flask app is running and try again.")
    
    #return API json object
    return api_result



# Function to return a list of the available properties and their updated current values as per whatever renovations they have stored in the Database
def get_property_list_after_renos(property_id):

    try:

        # Get request
        result = requests.get('http://127.0.0.1:5001/all_properties_after_renovations',
        headers={'content-type': 'application/json'})
        api_result = result.json() 

        #Determine the spacing to be used on the printing of headers.
        spacing = 5

        #printing the headers
        print('Property ID' + (" " * spacing) +
                    'Postcode' + (" " * spacing) +
                    'Bedroom #' + (" " * spacing) +
                    'Current Evaluation' + (" " * spacing) +
                    'Evaluation After Renovations' + (" " * spacing) +
                    'Purchase Date')
        for x in api_result:
            
            if property_id == 0:
                
                #for each result in the API json, print the results with specific spacing limits, in order to ensure it looks good visually.
                print(str(x['Property ID'])+(" "*(16-len(str(x['Property ID'])))+ 
                        x['Postcode'] + (" "*(13-len(str(x['Postcode'])))) +
                        str(x['Number of Bedrooms']) + (" "*(14-len(str(x['Number of Bedrooms'])))) +
                        str(x['Current Evaluation']) + (" " * (23-len(str(x['Current Evaluation'])))) +
                        str(x['Evaluation After Renovations']) + (" " * (33-len(str(x['Evaluation After Renovations'])))) +
                        str(datetime.strptime(x['Purchase Date'], '%a, %d %b %Y %H:%M:%S %Z').date())))

            #only display the results for the property ID the user has chosen
            if int(x['Property ID']) == int(property_id):
                
                #for each result in the API json, print the results with specific spacing limits, in order to ensuer it looks good visually.
                print(str(x['Property ID'])+(" "*(16-len(str(x['Property ID'])))+ 
                        x['Postcode'] + (" "*(13-len(str(x['Postcode'])))) +
                        str(x['Number of Bedrooms']) + (" "*(14-len(str(x['Number of Bedrooms'])))) +
                        str(x['Current Evaluation']) + (" " * (23-len(str(x['Current Evaluation'])))) +
                        str(x['Evaluation After Renovations']) + (" " * (33-len(str(x['Evaluation After Renovations'])))) +
                        str(datetime.strptime(x['Purchase Date'], '%a, %d %b %Y %H:%M:%S %Z').date())))
            else:
                pass
    #Error Handling in case Flask app is not running     
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the Flask server. Please ensure the Flask app is running and try again.")
    
    #return API json object
    return api_result



# Function to choose the property from the list of results
def choose_property(property_id):

    # results from the list of properties with Evaluations after Renovations
    api_result = get_property_list_after_renos(property_id)

    # While loop
    while True:
        try:

            # User to input chosen property via their ID
            print()
            chosen_property_id = input("Please enter the Property ID for the property you wish to use: ")
            print()

            # Number of properrties available
            number_properties = int(len(api_result))

            # Check if the user has entered nothing and trigger error
            if chosen_property_id =="":
                raise TypeError("Please enter a value. Input cannot be empty.")

            # Check if the user has entered a float and trigger error
            if "." in chosen_property_id:
                raise TypeError("Invalid input. Please enter a whole number between 0 and {}.".format(number_properties))
            
            # Convert user input to int
            chosen_property_id = int(chosen_property_id)

            # Check if the user has entered a number equal or smaller than zero (out of range) or a number larger than the number of available properties (out of range), trigger error
            if int(chosen_property_id) > number_properties or int(chosen_property_id) <= 0:
                raise ValueError("Invalid input. Please enter a number between 0 and {}.".format(number_properties))

            # Break while loop
            break

        # Catch the errors flagged in the previous block and add message to try again, as well as Escape commands.
        except ValueError as e:
            print(e)
            print("Please try again. (Press 'Ctrl + C' to close Program)")

        # Catch the errors flagged in the previous block and add message to try again, as well as Escape commands.
        except TypeError as e:
            print(e)
            print("Please try again. (Press 'Ctrl + C' to close Program)")

    # Select chosen property from API result (-1 as property ID's start at 1, whilst the list starts at 0)
    chosen_property = api_result[int(chosen_property_id)-1]

    # Store the chosen property's Purchase Price in a variable
    purchase_price = chosen_property['Purchase Price']

    # Store the chosen property's Evaluation After Renovations in a variable
    new_property_price = chosen_property['Evaluation After Renovations']

    # Store the chosen property's 'Purchase Date' as str in a variable
    purchase_date = str(datetime.strptime(chosen_property['Purchase Date'], '%a, %d %b %Y %H:%M:%S %Z').date())

    # Return the variables we need
    return purchase_price, new_property_price, purchase_date, chosen_property_id



# Function to add a new property via API post
def add_new_property(postcode, number_bedrooms, purchase_price, purchase_date):
    try:

        # Parameters to pass on as a Dictionary
        property = {
            "postcode": postcode,
            "number_bedrooms": number_bedrooms,
            "purchase_price": purchase_price,
            "purchase_date": purchase_date,
        }

        # Post request
        result = requests.post(
            'http://127.0.0.1:5001/add_property',
            headers={'content-type': 'application/json'},
            data=json.dumps(property))
    
    # Error Handling - let user know if Flask App is not running and advises to run it first.
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the Flask server. Please ensure the Flask app is running and try again.")
    
    # Return API result
    return result



# Function to add a new renovations via API post
def add_renovations(property_id, feature, price_paid_for_feature, current_evaluation, feature_added_date, property_value_after_renovation):
    try:

        # Parameters to pass on as a Dictionary
        reno = {
            "property_id": property_id,
            "feature": feature,
            "price_paid_for_feature": price_paid_for_feature,
            "current_evaluation": current_evaluation,
            "feature_added_date": feature_added_date,
            "property_value_after_renovation" : property_value_after_renovation
        }

        # Post request
        result = requests.post(
            'http://127.0.0.1:5001/add_renovations',
            headers={'content-type': 'application/json'},
            data=json.dumps(reno))
        
    # Error Handling - let user know if Flask App is not running and advises to run it first.
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the Flask server. Please ensure the Flask app is running and try again.")
    
    # Return API result
    return result



# Function to retrieve the available renovation features in the system via API post
def get_features():
    try:

        # GET request
        result = requests.get(
        'http://127.0.0.1:5001/renovation_features',
        headers={'content-type': 'application/json'})
        api_result = result.json() 

    # Error Handling - let user know if Flask App is not running and advises to run it first.
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the Flask server. Please ensure the Flask app is running and try again.")
    
    # Return API result
    return api_result



# Helper Function that helps print the get_features() results in a tidy way
def view_features():

    # Call get_features (API) and set results in variable
    api_result = get_features()

    # As the features don't have an ID in the system I am numbering them in this function, starting from 1
    feature_id = 1

    # Print Headers
    print('Feature Name                     Percentage')

    # For each API result, print results with specified spacing
    for i in api_result:
        distance = 40 - (len(i['Feature Name']) + len(str(feature_id)))
        feature = str(feature_id)+'.'+i['Feature Name'] + " " + i['Added Value Percentage'].rjust(distance)

        # Increase the Feature ID numbering by 1
        feature_id += 1

        # Print
        print(feature)
    
    # Return the API results
    return api_result



# Helper Function to select a feature from the get_feature() results
def select_feature(feature_to_calc):

    # Store the API results in a variable
    api_result = get_features()

    # Adjust list_number as Feature IDs start at 1
    list_number = int(feature_to_calc) - 1

    # Store chosen feature in a variable
    chosen_feature = api_result[list_number]

    # Store chosen feature name in a variable
    chosen_feature_name = chosen_feature['Feature Name']

    # Store chosen feature percentage in a variable
    chosen_percentage = float(chosen_feature['Added Value Percentage'][:-1])

    # Return our variables
    return chosen_percentage, chosen_feature_name



# Helper Function to calculate the Inflation price for a given property
# This is being calculated before adding to the SQL Database (rather than store the property details, let SQL calculate and then 
# retrieve the result from the database, because the user might not want to store the property details, so we have the calculation
# also taking place in client side for the Forecast with no storage of data.)
def calc_inflation(purchase_price, purchase_date):

    # Store variable with the purchase date as a date object
    date_obj = datetime.strptime(purchase_date, '%Y-%m-%d').date()

    # Store variable with the today's date as a date object
    today = datetime.today().date()

    # Calculate the year interval between the two dates (yearly inflation)
    date_interval_year = today.year - date_obj.year

    # Store purchase price in new variable
    new_property_price = purchase_price

    # For each year in the interval
    for x in range(date_interval_year):

        # Update the property price by 3.25% (property price + 3.25 of property price)
        new_property_price = new_property_price + (new_property_price * (3.25 / 100))

    # Print user message
    print("Without any features added, your property is currently estimated to be valued at: £{}".format(round(new_property_price, 2)))
    print("(Calculated using an average fixed inflation rate of 3.25% per year")

    # Return the new property price
    return new_property_price



# Helper Function to calculate the addded value of a feature
def calculate_added_value(feature_to_calc, new_property_price):

    # Store the selected feature result in a variable
    select_feature_res = select_feature(feature_to_calc)

    # Store the selected feature percentage in a variable
    chosen_percentage = select_feature_res[0]

    # Store the selected feature name in a variable
    chosen_feature = select_feature_res[1]

    # Calculate the added value using the above variables
    added_value = round(new_property_price * (chosen_percentage / 100), 2)

    # Return the added value and the feature name
    return added_value, chosen_feature



# Add new feature loop - I have made this loop so that it can be used in multiple parts of the code (Adding features for a new property, Adding features for an existing property)
def add_new_feature_loop(new_property_price,number_of_features,list_of_chosen_features):

    while True:
        try:
            # User to input the renovation feature numeric reference
            feature_to_calc = str(input("Please choose the desired renovation feature using their numeric reference: "))

            # Error handling in case the user inputs nothing
            if feature_to_calc == "":
                print()
                raise TypeError("Please enter a value. Input cannot be empty.")
            
            numeric_feature_to_calc = int(feature_to_calc)    

            # Error handling in case the user inputs a number higher than the number of available options
            if numeric_feature_to_calc > number_of_features:
                raise ValueError("Invalid input. Please enter a number between 0 and {}.".format(number_of_features))

            # Retrieve the feature name
            placeholder = 0
            feature_name = calculate_added_value(feature_to_calc, placeholder)[1]

            print()
            
            # Error handling in case the user inputs a number equal or lower than 0
            if numeric_feature_to_calc <= 0:
                raise ValueError("Invalid input. Please enter a number between 0 and {}.".format(number_of_features))
            
            # If the user has already selected the feature in a previous run
            if feature_name in list_of_chosen_features:
                print("You have already added this feature. Please choose another.")
                print()
                continue

            break
        
        # Catches the errors flagged in the previous block with an additional message to try again, and escape commands
        except TypeError as e:
            print(e)
            print("Please try again. (Press 'Ctrl + C' to close Program)")
            print()

        # Catches the errors flagged in the previous block, with a bespoke message that captures the error if the user 
        # enters a float, as well as an additional message to try again, and escape commands
        except ValueError as e:
            print("Invalid input. Please enter a whole number between 0 and {}.".format(number_of_features))
            print("Please try again. (Press 'Ctrl + C' to close Program)")
            print()
        
    while True:
        try:
            # User to input the amount of money they are planning to spend on this feature
            cost = input("Please confirm how much you are planning to spend on this feature: ")

            # Error handling in case the user inputs nothing
            if cost == "":
                print()
                raise TypeError("Please enter a value. Input cannot be empty.")

            cost = float(cost)

            # Error handling in case the user inputs a number lower than 0 (zero is still allowed in case the renovation is bein done for free)
            if cost < 0:
                print()
                raise ValueError("Invalid input. Please enter a number equal or larger than zero.")
            break

        # Error handling that catches the errors raised in the previous block as well as providing a message to Try again, and escape commands
        except ValueError as e:
            print(e)
            print("Please try again. (Press 'Ctrl + C' to close Program)")
            print()

        # Error handling that catches the errors raised in the previous block as well as providing a message to Try again, and escape commands
        except TypeError as e:
            print(e)
            print("Please try again. (Press 'Ctrl + C' to close Program)")
            print()

    # Store the added_value calculation result in a variable
    added_value_res = calculate_added_value(feature_to_calc, new_property_price)

    # Store the added value number in a variable
    added_value = added_value_res[0]

    # Store the feature name in a variable
    chosen_feature = added_value_res[1]

    # Return the added value number, the feature name and the cost
    return added_value, chosen_feature, cost



# Helper Function to perform some calculations on the Return on Investment for the features added to the property
def ROI_percentage(final_property_price,cost,purchase_price,new_property_price):

    # Calculate the difference between the current property evaluation (no renovations added) and the purchase price.
    inflation_difference = new_property_price - purchase_price

    # Calculate the percentage that the difference constitutes against the current property evaluation
    percentage_profit_inflation = round((inflation_difference / new_property_price) * 100, 2)

    # Calculate the difference between the current property evaluation (no renovations added) and the new property price estimate (with renovations).
    added_value_difference = final_property_price - new_property_price

    # Calculate the percentage that the difference constitutes against the new property evaluation (with renovations)
    percentage_profit_added_value = round((added_value_difference / final_property_price) * 100, 2)

    # Calculate the difference between the current property evaluation (no renovations added) and the new property price estimate (with renovations), minus the cost of the renovations.
    added_value_ROI_difference = final_property_price - new_property_price - cost

    # Calculate the percentage that the difference constitutes against the new property evaluation (with renovations)
    added_value_ROI = round((added_value_ROI_difference / final_property_price) * 100, 2)
    
    # Return the percentage values of each of the three calcs
    return percentage_profit_inflation, percentage_profit_added_value, added_value_ROI



# Helper Function that helps print the view_renovations_tracker() results in a tidy way - includes a print_command variable
# as sometimes I just want to retrieve the API results and not print anything. 
def view_renovations_tracker(property_id, print_command):
    
    # define the spacing gaps - kept separate for easy adjustment if needed
    bigspacing = 23
    mediumspacing = 12
    smallspacing = 3

    # Define headers with the spacing determined before - not printing immediately as sometimes I need the headers to not print
    headers = ('Renovation ID' + (" " * smallspacing) +
                'Property ID' + (" " * smallspacing) +
                'Feature' + (" " * bigspacing) +
                'Quote' + (" " * mediumspacing) +
                'Current Evaluation'+ (" " * smallspacing) +
                'Evaluation After Renovation'+ (" " * smallspacing) +
                'Date Feature Added')

    try:
        # Get request
        result = requests.get(
        'http://127.0.0.1:5001/renovations_tracker/{}'.format(property_id),
        headers={'content-type': 'application/json'})
        api_result = result.json() 

        # Empty list where I will store the renovation IDs
        list_of_renovation_ids = []

        # If an error is received from the API request, return just the headers (API result set to zero) I did this in case I just need the headers and not the API
        if "error" in api_result:
            api_result = 0
            return api_result, headers 

        # If the Print command is set to True
        if print_command == True:

            # For each result within the API
            for i in api_result:

                # Append the renovation IDs in the empty list defined earlier
                list_of_renovation_ids.append(i['Renovation ID'])

                # Print the API results in a tidy way - I defined the spacing by trial and error on what works
                print(str(i['Renovation ID'])+(" "*(16-len(str(i['Renovation ID'])))+
                        str(i['Property ID'])+(" "*(14-len(str(i['Property ID'])))+ 
                        i['Feature'] + (" "*(30-len(str(i['Feature'])))) +
                        str(i['Quote']) + (" "*(17-len(str(i['Quote'])))) +
                        str(i['Current Property Evaluation']) + (" " * (21-len(str(i['Current Property Evaluation'])))) +
                        str(i['Property Evaluation After Renovation']) + (" " * (30-len(str(i['Property Evaluation After Renovation'])))) +
                        str(datetime.strptime(i['Date Feature Added'], '%a, %d %b %Y %H:%M:%S %Z').date()))))

    # Error Handling - let user know if Flask App is not running and advises to run it first.
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the Flask server. Please ensure the Flask app is running and try again.")

    # Return the API results (or zero, if just needed the headers), headers and list of renovation ids
    return api_result, headers, list_of_renovation_ids



# Calcs Function - this is one of the main functions of this program.
def calcs(new_or_existing_property,purchase_price, purchase_date, new_property_price):

    # If the user has chosen to run a new Property through the Forecaster
    if new_or_existing_property == "New":

        # Go straight to the calc_inflation function as for Existing properties we alreday have the property price after inflation
        new_property_price = calc_inflation(purchase_price, purchase_date)

    # Otherwise continue
    else:
        pass

    # Message to the User, asking which renovation feature they would like to use
    print()
    print("Which renovation feature would you like to use in the calculation?")
    print("Please see the available list on our database, along with their corresponding potential Return on Investment as a Percentage")
    print()

    # Call the view_features() function to display the list of renovation features to the user
    feature_list = view_features()

    # Store the number of features available in a variable so we can use it as a max ID allowed in the user choice
    number_of_features = len(feature_list)
    print()

    # Set variable add_more to True for the upcoming loop
    add_more = True

    # Define a few empty lists to store values
    list_of_chosen_features = []
    list_of_costs = []

    # The below lsit has the starting point of the current property evaluation for a correct timeline of price increase
    list_of_price_increase =[new_property_price]

    # Define the variable cost to zero as a starting point (will increase incrementally)
    cost = 0

    # Define the variable final_property_price as the current property evaluation as a starting point (will increase incrementally)
    final_property_price = new_property_price

    # While loop #1
    while add_more:

        # Store the add_new_feature_loop() results in variable res
        res = add_new_feature_loop(new_property_price,number_of_features,list_of_chosen_features)

        # Increase final_property_price by the added_cost variable
        final_property_price += int(res[0])

        # Append results to the empty lists
        list_of_chosen_features.append(res[1])
        list_of_price_increase.append(final_property_price)

        # Increase cost variable by the cost variable (from add_new_feature_loop function)
        cost += int(res[2])

        # Append results to the empty lists
        list_of_costs.append(res[2])

        # While Loop #2
        while True:
            try:

                # User input to confirm if they want to add more features. This also breaks the while loop #2. Forces Upper case for consistency
                choice = input("Would you like to add more features? (Y/N): ").upper()
                print()

                # Error Handling if the user inputs anything but Y or N
                if choice not in ("Y","N"):
                    raise ValueError("Invalid input. Please enter either 'Y' or 'N'.")
                
                break

            # Catches the error raised in the previous block, along with a message to try again and escape commands
            except ValueError as e:
                print(e)
                print("Please try again. (Press 'Ctrl + C' to close Program)")
                print()

        # If User choses Y
        if choice == 'Y':

            # Continue the add_more loop (User confirmed that yes they want to add more features)
            add_more = True

        else:

            # Otherwise, (User chooses N) - set add_more to False to stop the loop
            add_more = False

            # Run the variables through the Return on Invesment function
            ROI_res = ROI_percentage(final_property_price,cost,purchase_price,new_property_price)

            # Store the relevant results in variables to then use in the User Messages
            percentage_profit_inflation = ROI_res[0]
            percentage_profit_added_value = ROI_res[1]
            added_value_ROI = ROI_res[2]
            final_property_price = round(final_property_price,2)

            # This flat list has the list of feature names added by the user
            flat_list = ', '.join(list_of_chosen_features)
            
            # ROI User Messages informing the User of the percentages relevant to the changes made to the property, as well as
            # how much of the profit is purely due to inflation
            print()
            print("#######################################################################")
            print()
            print("Your Final Property Evaluation Forecast is: {}".format(final_property_price))
            print("The above estimation is on the basis of adding the following features: {}".format(flat_list))
            print()
            print("The Return on investment is as follows :")
            print()
            print("""- Added Value Percentage solely due to Inflation: {}%\n- Added Value Percentage due to New Features (may not match feature catalogue due to roundings): {}%\n- True Added Value Percentage due to New Features but Accounting for Cost: {}%""".format(percentage_profit_inflation, percentage_profit_added_value, added_value_ROI))
            print()

    # Returns key variables for the rest of the run() function
    return list_of_chosen_features, list_of_costs, list_of_price_increase, new_property_price
    


# amend_renovations function to amend the price_paid_for_feature within the renovations_tracker table in the Database - via API  
def amend_renovations(new_price_paid_for_feature, property_id, renovation_to_amend):
    try:   

        # Parameters to pass on as a Dictionary
        renovations = {
            "new_price_paid_for_feature": new_price_paid_for_feature,
            "property_id": property_id,
            "renovation_to_amend": renovation_to_amend
        }

        # Put request
        result = requests.put(
            'http://127.0.0.1:5001/update_feature_price',
            headers={'content-type': 'application/json'},
            data=json.dumps(renovations))
    
    # Error Handling - let user know if Flask App is not running and advises to run it first.
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the Flask server. Please ensure the Flask app is running and try again.")
    
    # Return API's json response
    return result


# Main Function run()
def run():
    try:

        # WELCOME MESSAGE
        print()
        print("######  Welcome to the Property Portfolio & Forecaster!  ######")
        print()
        print("The Application where you can forecast the return on investment of renovations before you agree to them.")
        print()

        # While loop #1
        while True:
            try:

                ### First User choice ### - store answer in variable, force title() format
                forecast_or_amend = input("Would you like to run our Forecaster, or amend a feature cost of a stored property? (Forecast/Amend): ").title()
                print()

                # Error Handling in case user inputs anything but Forecast or Amend
                if forecast_or_amend not in ("Forecast","Amend"):
                    raise ValueError("Invalid input. Please enter either 'Forecast' or 'Amend'.")
                
                # Break while loop #1
                break

            # Catches the error raised in the previous block, along with a message to try again and escape commands
            except ValueError as e:
                print(e)
                print("Please try again. (Press 'Ctrl + C' to close Program)")
                print()
            
        # If user has chosen to Forecast
        if forecast_or_amend == "Forecast":
            
            # While loop #2
            while True:
                try:

                    ### Second User choice ### - store answer in variable - force title() format
                    print("Would you like to run a forecast on an existing property in our Portfolio or a new Property?")
                    new_or_existing_property = input("New/Existing: ").title()
                    print()

                    # Error Handling in case user inputs anything but New or Existing
                    if new_or_existing_property not in ("New","Existing"):
                        raise ValueError("Invalid input. Please enter either 'New' or 'Existing'.")
                    
                    # Break while loop #2
                    break

                # Catches the error raised in the previous block, along with a message to try again and escape commands
                except ValueError as e:
                    print(e)
                    print("Please try again. (Press 'Ctrl + C' to close Program)")
                    print()

            # If User has chosen to run Forecaster with a new property
            if new_or_existing_property == "New":

                # User Message
                print("Please provide us some details on the new property.")
                print()

                # Define variable choice as True as starting point for loop
                choice = True

                # While loop #3
                while choice:

                    # User Input - Postcode - force removal of spaces and force upper cas
                    postcode = input('Enter postcode: ').replace(" ", "").upper()

                    # If length of postcode is more than 7 characters (UK limits) (no spaces included), trigger message about incorrect input
                    if len(postcode) > 7:
                        print()
                        print("Postcode is too long - please enter a postcode with no more than 8 characters (including spaces) (Press 'Ctrl + C' to close Program)")      
                        print()

                        #choice remains true to continue the loop
                        choice = True

                    # If length of postcode is less than 5 characters (UK limits) (no spaces included), trigger message about incorrect input    
                    elif len(postcode) < 5:
                        print()
                        print("Postcode is too short - please enter a postcode with more than 5 characters (not including spaces) (Press 'Ctrl + C' to close Program)")      
                        print()

                        #choice remains true to continue the loop
                        choice = True
                    
                    # Otherwise Postcode meets criteria
                    else:

                        #choice remains set to False to break the loop
                        choice = False
                
                # While loop #4
                while True:
                    try:
                        # User to input number of bedrooms in the new property
                        number_bedrooms = input('How many bedrooms does the property have? ')

                        # Error Handling - if user doesn't input anything
                        if number_bedrooms == "":
                            print()
                            raise TypeError("Please enter a value. Input cannot be empty.")
                        
                        # Convert nr. bedrooms to int
                        number_bedrooms = int(number_bedrooms)

                        # Error Handling - if user inputs a number lower than 0 - allowing zero bedrooms to account for studios
                        if number_bedrooms < 0:
                            print()
                            raise ValueError("Invalid input. Please enter either a number higher than 0.")
                        
                        # Break while loop #4
                        break

                    # Catches the error raised in the previous block, along with a message to try again and escape commands
                    except ValueError as e:
                        print(e)
                        print("Please try again. (Press 'Ctrl + C' to close Program)")
                        print()

                    # Catches the error raised in the previous block, along with a message to try again and escape commands
                    except TypeError as e:
                        print(e)
                        print("Please try again. (Press 'Ctrl + C' to close Program)")
                        print()

                # While loop #5
                while True:
                    try:    

                        # User to input how much was paid for the new property
                        purchase_price = input('How much did you originally pay for the property? ')

                        # Error Handling - if user doesn't input anything
                        if purchase_price == "":
                            print()
                            raise TypeError("Please enter a value. Input cannot be empty.")
                        
                        # Convert price to float
                        purchase_price = float(purchase_price)

                        # Error Handling - if user inputs a value less than 0 - allowing zero for gifted properties
                        if purchase_price < 0:
                            print()
                            raise ValueError("Invalid input. Please enter either a value higher than or equal to 0.")
                        
                        # Break while loop #5
                        break

                    # Catches the error raised in the previous block, along with a message to try again and escape commands
                    except ValueError as e:
                        print(e)
                        print("Please try again. (Press 'Ctrl + C' to close Program)")
                        print()
                    
                    # Catches the error raised in the previous block, along with a message to try again and escape commands
                    except TypeError as e:
                        print(e)
                        print("Please try again. (Press 'Ctrl + C' to close Program)")
                        print()
                
                # While loop #6
                while True:

                    # User to input when did the new property was purchased
                    purchase_date = str(input('When did you by the property? (YYYY-MM-DD) '))
                    print()
                    try:

                        # Date format check
                        date_check = datetime.strptime(purchase_date, "%Y-%m-%d")

                        # Break while loop #6
                        break

                    # Catches the error raised in the previous block, along with a message to try again and escape commands
                    except ValueError:
                        print("Incorrect format, please enter the date in the format YYYY-MM-DD. Try again. (Press 'Ctrl + C' to close Program)")
                
                # Set new property price to 0 so it can be passed to the calcs function, this will be replaced with the inflated price within the calcs fucntion
                # The variable requires this, as it has been built to also work with existing properties, which already have a defined
                # new property price variable
                new_property_price = 0

                # Store calcs results in varible
                calcs_result = calcs(new_or_existing_property,purchase_price, purchase_date, new_property_price)

                #Store calcs result variables in local variables
                feature_list = calcs_result[0]
                list_of_costs = calcs_result[1]
                list_of_price_increase = calcs_result[2]

                # While loop #7
                while True:
                    try:

                        # User to input whether they want the app to store the property, and the renovation details
                        add_property_or_not = input("Would you like to store your property, renovations list and price increase forecast in our database for future use? (Y/N): ").upper()
                        print()

                        # Error Handling in case user inputs anything but Y or N
                        if add_property_or_not not in ("Y","N"):
                            raise ValueError("Invalid input. Please enter either 'Y' or 'N'.")
                        
                        # Break while loop #7
                        break

                    # Catches the error raised in the previous block, along with a message to try again and escape commands
                    except ValueError as e:
                        print(e)
                        print("Please try again. (Press 'Ctrl + C' to close Program)")
                        print()
                
                # If user has chosen to store the new property details, as well as the renovations
                if add_property_or_not =="Y":
                    
                    # Call the add_new_property function
                    add_new_property(postcode, number_bedrooms, purchase_price, purchase_date)

                    # Store the function results in local variable
                    property_list_res = view_properties()

                    # Define the property_id as the max amount of records (in the SQL table the property IDs as set to auto increment)
                    property_id = int(len(property_list_res))

                    # For each item in the list of features added:
                    for item in range(len(feature_list)): 

                        # Define the feature variable as the current iteration in the list of features
                        feature = feature_list[item]

                        # Define the price_paid_for_feature variable as the current iteration in the list of costs
                        price_paid_for_feature = str(list_of_costs[item])

                        # Define the current_evaluation variable as the current iteration in the list of price increases
                        current_evaluation = str(list_of_price_increase[item])

                        # Define the feature_added_date variable as the current iteration in the list of added dates
                        feature_added_date = str(datetime.today().strftime('%Y-%m-%d'))

                        # Define the property_value_after_renovation variable as the next iteration in the list of price increases
                        property_value_after_renovation = str(list_of_price_increase[item+1])

                        # Call the add_renovations function to add results to database
                        add_renovations(property_id, feature, price_paid_for_feature, current_evaluation, feature_added_date, property_value_after_renovation)
                    
                    print()

                    # Print headers only
                    print(view_renovations_tracker(0, False)[1])

                    # Print list of renovations in the renovations_tracker
                    view_renovations_tracker(property_id, True)
                    print()

                    # Get the property list summary for the property just added to the database (includes the evaluation price after renovations)
                    get_property_list_after_renos(property_id)
                    print()
                    print("Property & Renovation details stored. Have a good day, and see you soon!")
                    print()
                
                # Else if user has chosen not to store details
                elif add_property_or_not =="N":

                    # Print user message and don't store any information
                    print("Property details not stored. Have a good day, and see you soon!")
                    print()
            

            # If User has chosen to run Forecaster with an Existing property 
            elif new_or_existing_property == "Existing":
                
                # Set property_id to zero to show all the properties available (view_property) within the choose_property function
                # Function will return a valid property_id after the user has chosen
                property_id = 0

                # Store the function results in a variable
                property_list_res = choose_property(property_id)

                # Store the variable results in local variables
                purchase_price = float(property_list_res[0])
                purchase_date = property_list_res[2]
                new_property_price = float(property_list_res[1])
                chosen_property_id = int(property_list_res[3])

                # If the function API results are not zero (nothing)
                if view_renovations_tracker(chosen_property_id, False)[0] != 0:
                    
                    # Print User message
                    print()
                    print("Please see the below existing renovations on record - adding a renovation already in place might skew the Evaluation price.")
                    print("You may still add a renovation that is already in place, to account for extensions and room conversions.")
                    print()

                    # Print headers
                    print(view_renovations_tracker(0, False)[1])

                    # run view_renovations_tracker with print set to True
                    view_renovations_tracker(chosen_property_id, True)
                    print()

                # Store calcs results in varible
                calcs_result = calcs(new_or_existing_property,purchase_price, purchase_date, new_property_price)

                # Set calcs function results in local variables
                feature_list = calcs_result[0]
                list_of_costs = calcs_result[1]
                list_of_price_increase = calcs_result[2]
                
                # While loop #8
                while True:
                    try:

                        # User to input whether they want the app to store the renovation details
                        add_renovations_or_not = input("Would you like to store your renovations list and price increase forecast in our database for future use? (Y/N): ").title()
                        print()

                        # Error Handling in case user inputs anything but Y or N
                        if add_renovations_or_not not in ("Y","N"):
                            raise ValueError("Invalid input. Please enter either 'Y' or 'N'.")
                        
                        # Break while loop #8
                        break

                    # Catches the error raised in the previous block, along with a message to try again and escape commands
                    except ValueError as e:
                        print(e)
                        print("Please try again. (Press 'Ctrl + C' to close Program)")
                        print()

                # If user has chosen to store the new property details, as well as the renovations
                if add_renovations_or_not =="Y":

                    # For each item in the list of features added:
                    for item in range(len(feature_list)):

                        # Define the property_id variable as the chosen_property_id
                        property_id = chosen_property_id

                        # Define the feature variable as the current iteration in the list of features
                        feature = feature_list[item]

                        # Define the price_paid_for_feature variable as the current iteration in the list of costs
                        price_paid_for_feature = str(list_of_costs[item])

                        # Define the current_evaluation variable as the current iteration in the list of price increases
                        current_evaluation = str(list_of_price_increase[item])

                        # Define the feature_added_date variable as the current iteration in the list of dates
                        feature_added_date = str(datetime.today().strftime('%Y-%m-%d'))

                        # Define the property_value_after_renovation variable as the next iteration in the list of price increases
                        property_value_after_renovation = str(list_of_price_increase[item+1])
                        
                        # Call the add_renovations function to add results to database
                        add_renovations(property_id, feature, price_paid_for_feature, current_evaluation, feature_added_date, property_value_after_renovation)
                    
                    print()

                    # Print Headers only
                    print(view_renovations_tracker(0, False)[1])

                    # Print list of renovations in the renovations_tracker
                    view_renovations_tracker(property_id, True)
                    print()

                    # Get the property list summary for the property just added to the database (includes the evaluation price after renovations)
                    get_property_list_after_renos(property_id)
                    print()
                    print("Renovation details stored. Have a good day, and see you soon!")
                    print()

                # Else if user has chosen not to store details
                if add_renovations_or_not =="N":
                    
                    # Print user message and don't store any information
                    print("Property details not stored. Have a good day, and see you soon!")
                    print()

        # If the User has chosen to Amend instead of Forecast
        elif forecast_or_amend == "Amend":    
            
            # Call function view properties and store results in local variable
            api_result = view_properties()

            # Set reno_choice variable to True as a starting point for the loop
            reno_choice = True

            # While loop #9
            while reno_choice:

                # res is the length of results in teh API result as a number
                res = int(len(api_result))

                # Print Header
                print(view_renovations_tracker(0, False)[1])

                # For each iteration in a range from 0 to res
                for i in range(res):
                    try:

                        # View/Print the list of renovations stored in the renovations_tracker table (iteration is instance + 1 due to range starting at 0 and ids starting at 1)
                        renovations = view_renovations_tracker(i+1, True)

                        # If function result is True (exists)
                        if renovations:

                            # Set choice to False to break while loop #9
                            choice = False
                    
                    # Otherwise continuer
                    except:
                        continue

                print()

                # while loop #10
                while True:
                    try:

                        # User to input which property they want to amend the feature price for
                        property_id = str(input("Please select which Property to amend by Property ID: "))
                        print()

                        # Error Handling - if user doesn't input anything
                        if property_id == "":
                            raise ValueError("Please enter a value. Input cannot be empty.")
                        
                        # Convert property_id to integer
                        property_id_numeric = int(property_id)

                        # Error Handling - if user inputs a negative number
                        if property_id_numeric <= 0:
                            raise ValueError("Please enter a positive value.")
                        
                        # Error Handling - if the function view_renovations_tracker doesn't return any API results under the chosen property ID
                        if view_renovations_tracker(property_id, False)[0] == 0:
                            print(f"Error: Property ID {property_id} has no tracked renovations. Please try again.")
                            print()

                    # Catches the error raised in the previous block, along with a message to try again and escape commands
                    except TypeError as e:
                        print("Invalid Input. Please enter a whole number larger than 0.")
                        print("Please try again. (Press 'Ctrl + C' to close Program)")
                        print()

                    # Catches the error raised in the previous block, along with a message to try again and escape commands
                    except ValueError as e:
                        print(e)
                        print("Please try again. (Press 'Ctrl + C' to close Program)")
                        print()

                    # Break while loop #10
                    break

                print()

                # While loop #11
                while True:

                    # Print headers
                    print(view_renovations_tracker(0, False)[1])

                    # Store list of renovation_ids that is part of the view_renovations_tracker function return into a local variable
                    renovation_ids = view_renovations_tracker(property_id, True)[2]
                    print()

                    # While loop #12
                    while True:

                        # User to input which renovation they want to amend the feature price for, by renovation ID
                        renovation_to_amend = str(input("Please select which quote to amend by Renovation ID: "))
                        print()

                        try:

                            # Convert Renovation ID to integer
                            renovation_to_amend_int = int(renovation_to_amend)

                            # If renovation ID not present in the list of Renovation_IDs - Error
                            if renovation_to_amend_int not in renovation_ids:
                                print(f"Error: Renovation ID {renovation_to_amend} not available under selected Property. Please try again.")
                                print()

                            else:

                                # Break While loop #12
                                break

                        # Catches the error raised in the previous block, along with a message to try again and escape commands
                        except ValueError:
                            print(f"Error: '{renovation_to_amend}' is not a valid number. Please enter a valid Renovation ID.")
                            print()
                    
                    # While loop #13
                    while True:
                        try:
                            # User to input what is the correct feature cost/price 
                            new_price_paid_for_feature = input("Please input the correct price: ")

                            # Error Handling - if user doesn't input anything
                            if new_price_paid_for_feature.strip() == "":
                                print()
                                raise TypeError("Please enter a value. Input cannot be empty.")
                            
                            # Convert new_price_paid_for_feature_float to float
                            new_price_paid_for_feature_float = float(new_price_paid_for_feature)

                            # Error Handling - if user has input a value less than zero - zero cost is allowed as a friend might be doing the renovations for free
                            if float(new_price_paid_for_feature_float) < 0:
                                print()
                                raise ValueError("Invalid input. Please enter either a value higher than or equal to 0.")
                            
                            # Break while loop #13
                            break
                        
                        # Catches the error raised in the previous block, along with a message to try again and escape commands
                        except ValueError as e:
                            print(e)
                            print("Please try again. (Press 'Ctrl + C' to close Program)")
                            print()

                        # Catches the error raised in the previous block, along with a message to try again and escape commands
                        except TypeError as e:
                            print(e)
                            print("Please try again. (Press 'Ctrl + C' to close Program)")
                            print()

                    # Call the function to amend the existing renovations in the system
                    amend_renovations(new_price_paid_for_feature, property_id, renovation_to_amend)

                    # User Message
                    print()
                    print("Feature Price Amended Successfully!")
                    print()

                    # Print Headers
                    print(view_renovations_tracker(0, False)[1])

                    # Store renovaiton ID list from function result in local variable
                    renovation_ids = view_renovations_tracker(property_id, True)[2]

                    # Store the API result in local variable
                    renovations = view_renovations_tracker(property_id, False)[0]

                    # Set variable found to False as starting point
                    found = False

                    # for each renovation in the API results
                    for re in renovations:

                        # If the Renovation ID matches our choice
                        if re['Renovation ID'] == int(renovation_to_amend):

                            # Store the API results in local variables
                            new_property_price = float(re['Current Property Evaluation'])
                            final_property_price = float(re['Property Evaluation After Renovation'])
                            feature = re['Feature']
                            new_price_paid_for_feature = float(new_price_paid_for_feature) 

                            # Set found to True
                            found = True

                            # Break loop
                            break
                    
                    # If variable found is True (selected Renovation ID is found in the API results)
                    if found:

                        # Set purchase price to zero, as we are not interested in the inflation stats (they don't change as the feature price changes)
                        purchase_price = 0

                        # Call the function Return on Investment and store the results locally
                        ROI_res = ROI_percentage(final_property_price,new_price_paid_for_feature,purchase_price,new_property_price)

                        # Store the ROI returned variables in local variables
                        percentage_profit_added_value = ROI_res[1]
                        added_value_ROI = ROI_res[2]

                        # Print User Message with statistics information about the changes made and how it affects the ROI
                        print()
                        print("#######################################################################")
                        print()
                        print("The price was successfully amended for the following feature: {}".format(feature))
                        print()
                        print("The Return on investment is as follows :")
                        print()
                        print("""- Added Value Percentage due to New Features (may not match feature catalogue due to roundings): {}%\n- True Added Value Percentage due to New Features but Accounting for New Cost: {}%""".format(percentage_profit_added_value, added_value_ROI))
                        print()

                    # While Loop #14
                    while True:
                        try:

                            # User to choose whether they want to amend more features for the selected property 
                            continue_choice = input("Would you like to amend the price of more features for this property? (Y/N): ").upper()
                            print()

                            # Error Handling - If user inputs anything but Y or N
                            if continue_choice not in ("Y","N"):
                                raise ValueError("Invalid input. Please enter either 'Y' or 'N'.")
                            
                            # Break while loop #14
                            break

                        # Catches the error raised in the previous block, along with a message to try again and escape commands
                        except ValueError as e:
                            print(e)
                            print("Please try again. (Press 'Ctrl + C' to close Program)")
                            print()

                    # If user chooses Y, True - so continue with the loop
                    if continue_choice == "Y":
                        True

                    # If user chooses N, break while loop 11
                    if continue_choice == "N":
                        break
                        
                # while loop #15
                while True:
                    try:

                        # User to choose whether they want to amend more features for the selected property 
                        choice = input("Would you like to amend the feature cost of a different stored property? (Y/N): ").upper()
                        print()

                        # Error Handling - If user inputs anything but Y or N
                        if choice not in ("Y","N"):
                            raise ValueError("Invalid input. Please enter either 'Y' or 'N'.")
                        
                        # Break while loop #15
                        break

                    # Catches the error raised in the previous block, along with a message to try again and escape commands
                    except ValueError as e:
                        print(e)
                        print("Please try again. (Press 'Ctrl + C' to close Program)")
                        print()

                # If User chooses Y, continue the loop
                if choice == "Y":
                    reno_choice = True

                # If User chooses N, break while loop #9
                elif choice == "N":
                    reno_choice = False

                    # User Message
                    print("Thank you for updating our details. Have a good day, and see you soon!")
                    print()

    # If user does Keyboard Interrupt (Ctrl + C), close program and display goodbyie message
    except KeyboardInterrupt:
        print()
        print()
        print("Thank you for using our Forecaster Application. See you soon!")
        print()
    
    # Catches the error raised in the previous block, along with a message to try again and escape commands
    except Exception as e:
        print(f"An unexpected error occurred: {e}. Please try again.")
        print()


# Check to see if this script is being run directly or being imported as a module
if __name__ == '__main__':
    run()