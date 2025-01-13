import mysql.connector
from config import USER, PASSWORD, HOST

# Specifying a specific error class, so I can use it when error handling database connection issues specifically, rather than relying
# on the generic Exception error
class DbConnectionError(Exception):
    pass



# Connect to the database
def _connect_to_db(db_name):
    try:
        # connection details
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            auth_plugin='mysql_native_password',
            database=db_name)

        # Success message
        print(f"Successfully connected to the database: {db_name}")
        return connection
    
    # Exception message if it fails to connect to the database
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        raise DbConnectionError(f"Failed to connect to the database: {e}")



# Mapping function so the data displayed in the API results is tidy - this one is specific to when the API calls data from the property_list table.
def _map_property_values(result):
    mapped = []
    # There are two different ways to map depending on the number of fields being passed through.
    # This is because sometimes the data is called either directly from the database via the browser (6 fields) or
    # sometimes it is called with the join SQL function that includes the "Evaluation After Renovations" field (7 fields)
    for item in result:

        # If number of fields is 6
        if len(item) == 6:
            mapped.append({
                'Property ID': item[0],
                'Postcode': item[1],
                'Number of Bedrooms': item[2],
                'Purchase Price': item[3],
                'Purchase Date': item[4],
                'Current Evaluation': item[5]
            })

        # If number of fields is 7
        if len(item) == 7:
            mapped.append({
                'Property ID': item[0],
                'Postcode': item[1],
                'Number of Bedrooms': item[2],
                'Purchase Price': item[3],
                'Purchase Date': item[4],
                'Current Evaluation': item[5],
                'Evaluation After Renovations': item[6]
            })

    return mapped



# Mapping function so the data displayed in the API results is tidy - this one is specific to when the API calls data from the renovation_features table.
def _map_feature_values(result):
    mapped = []
    for item in result:
        # Map with the "%" symbol
        percentage = str(item[1]) + "%"
        mapped.append({
            'Feature Name': item[0],
            'Added Value Percentage': percentage
        })

    return mapped



# Mapping function so the data displayed in the API results is tidy - this one is specific to when the API calls data from the renovations_tracker table.
def _map_renovations_tracker(result):
    mapped = []
    for item in result:
        mapped.append({
            'Renovation ID': item[0],
            'Property ID': item[1],
            'Feature': item[2],
            'Quote': item[3],
            'Current Property Evaluation': item[4],
            'Date Feature Added': item[5],
            'Property Evaluation After Renovation': item[6]
        })

    return mapped



# Helper function so I can pull data from the database whilst passing different SELECT queries through it.
def get_data(table, query):

    result_list =[]
    db_connection = None

    try:
        database_name = 'property_portfolio'

        # Connect to the database
        db_connection = _connect_to_db(database_name)

        # Initiate cursor
        cur = db_connection.cursor()

        # Success message
        print("Connected to DB: %s" % database_name)

        # Execute the query
        cur.execute(query)

        # this is a list with db records where each record is a tuple
        result = cur.fetchall()  

        # Checks to see which mapping function to use
        if table == 'property_list':
            result_list = _map_property_values(result)
        elif table == 'renovation_features':
            result_list = _map_feature_values(result)
        elif table == 'renovations_tracker':
            result_list = _map_renovations_tracker(result)

        # Close cursor
        cur.close()

    # Error handling to cover connection issues with the database
    except mysql.connector.Error as e:
        print(f"Database query error: {e}")
        raise DbConnectionError(f"Failed to read data from DB: {e}")
    
    # Error handling to cover rest of Exceptions
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

    finally:
        
        # If connection is successful
        if db_connection:
            # Close database connection
            db_connection.close()
            print("DB connection is closed")

    return result_list



# Function that passes through a SELECT query to retrieve all the features in the renovation_features table.
def get_feature_list():
    table = 'renovation_features'
    query = """

            SELECT 
                feature,
                added_value_percentage
            FROM 
                {};
            """.format(table)
    
    # Pull data using the helper function that retrieves data.
    return get_data(table, query)



# Function that passes through a SELECT query to retrieve all the features in the property_list table.
def get_property_list():
    table = 'property_list'
    query = """

            SELECT  
                ID,
                postcode,
                number_bedrooms,
                purchase_price,
                purchase_date,
                current_evaluation
            FROM 
                {}
            ORDER BY
                ID ASC;

            """.format(table)
    
    # Pull data using the helper function that retrieves data.
    return get_data(table, query)



# Function that passes through a SELECT query to retrieve all the features in the property_list table, but also joins 
# with the renovations_tracker table, to extract the Maximum property value of each property and Coalesce it in the property_list table
# This is just a data retrieval and it's not amending the original tables.

def get_property_list_after_renos():
    table = 'property_list'
    query = """

            SELECT 
                ps.ID, 
                ps.postcode, 
                ps.number_bedrooms, 
                ps.purchase_price, 
                ps.purchase_date, 
                ps.current_evaluation,
                COALESCE(q.maximum_value, ps.current_evaluation) AS evaluation_value_after_renos
            FROM
	            property_list AS ps
            LEFT JOIN
                (SELECT 
                    property_id, 
                    MAX(property_value_after_renovation) AS maximum_value 
                FROM 
                    renovations_tracker 
                GROUP BY 
                    property_id) AS q
            ON 
                ps.ID = q.property_id
            GROUP BY 
                ps.ID
            ORDER BY
                ps.ID ASC;

            """.format(table)
    
    # Pull data using the helper function that retrieves data.
    return get_data(table, query)



# Function that passes through a SELECT query to retrieve all the properties in the property_list table that have x number of bedrooms. 
def get_properties_by_bedroom_nr(_bd_number):
    table = 'property_list'
    query = """

            SELECT  
                ID,
                postcode,
                number_bedrooms,
                purchase_price,
                purchase_date,
                current_evaluation
            FROM 
                {}
            WHERE 
                number_bedrooms = {}
            ORDER BY
                ID ASC;

            """.format(table, _bd_number)
    
    # Pull data using the helper function that retrieves data.
    return get_data(table, query)
 


# Helper function so I can add data to the database whilst passing different INSERT or UPDATE queries through it.
def add_data(query, data):
    db_connection = None
    try:
        db_name = 'property_portfolio'

        # Connect to the database
        db_connection = _connect_to_db(db_name)

        # Initiate cursor
        cur = db_connection.cursor()

        # Success message
        print("Connected to DB: %s" % db_name)

        try:

            # Execute the query
            cur.execute(query, data)

            # Commit the changes
            db_connection.commit()
        
        # If any MySQL errors occur, query syntax, connection, etc, raise error and rollback transaction
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            db_connection.rollback()
            raise DbConnectionError(f"Failed to insert data into DB: {e}")
    
    # Catches the exception raised in the previous block
    except DbConnectionError as e:
        print(e)

    # Catch any other unexpected errors.
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    finally:
        # Close cursor
        cur.close()

        # Close database connection
        db_connection.close()



# Function that passes through an INSERT query to add new properties to the property_list table. 
def add_property(postcode, number_bedrooms, purchase_price, purchase_date):
    table = 'property_list'
    query = """

        INSERT INTO {} (
            postcode, 
            number_bedrooms, 
            purchase_price, 
            purchase_date
        )
        VALUES 
            (%s, %s, %s, %s);

    """.format(table)

    # Parameters to pass into the add_data function
    data = postcode, number_bedrooms, purchase_price, purchase_date

    # Calling the add_data function
    add_data(query, data)



# Function that passes through an INSERT query to add new properties to the property_list table. 
def add_renovations(property_id, feature, price_paid_for_feature, current_evaluation, feature_added_date, property_value_after_renovation):
    table = 'renovations_tracker'
    query = """

        INSERT INTO {} (
            property_id, 
            feature, 
            price_paid_for_feature, 
            current_evaluation, 
            feature_added_date, 
            property_value_after_renovation
        )
        VALUES 
            (%s, %s, %s, %s, %s, %s);

    """.format(table)

    # Parameters to pass into the add_data function
    data = property_id, feature, price_paid_for_feature, current_evaluation, feature_added_date, property_value_after_renovation
    
    # Calling the add_data function
    add_data(query, data)



# Function that passes through a SELECT query to retrieve the values in the renovations_tracker table, where a property is specified. 
def get_renovations_tracker(property_id):
    table = 'renovations_tracker'
    query = """

            SELECT 
                renovation_id,
                property_id,
                feature,
                price_paid_for_feature,
                current_evaluation,
                feature_added_date,
                property_value_after_renovation
            FROM 
                {}
            WHERE 
                property_id = {}
            ORDER BY
                renovation_id ASC;

            """.format(table, property_id)
    
    # Pull data using the helper function that retrieves data.
    return get_data(table, query)



# Function that passes through an UPDATE query to update the price_paid_for_feature amount in the renovations_tracker table. 
def amend_feature_price(new_price_paid_for_feature, property_id, renovation_to_amend):
    table = 'renovations_tracker'
    query = """

        UPDATE {} 
            SET price_paid_for_feature = %s
        WHERE 
            property_id = %s
            AND
            renovation_id = %s;

    """.format(table)

    # Parameters to pass into the add_data function
    data = (float(new_price_paid_for_feature), int(property_id), int(renovation_to_amend))

    # Calling the add_data function
    add_data(query, data)


# Check to see if this script is being run directly or being imported as a module
if __name__ == '__main__':
    get_property_list()
    get_feature_list()
    add_property()
    add_renovations()
    amend_feature_price()
    get_property_list_after_renos()