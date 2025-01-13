import unittest
from Property_Portfolio_Forecaster_main import ROI_percentage

# Define TestROI class
class TestROI(unittest.TestCase):

    # Test to check the behavior of ROI calculation when feature cost is zero - let's say a friend is doing the work for free
    def test_roi_zero_cost(self):
        # Setup for zero cost
        final_property_price = 150000
        cost = 0  # Zero cost for renovations
        purchase_price = 100000
        new_property_price = 120000

        # Call the ROI function, store each result in new variables

        percentage_profit_inflation = ROI_percentage(
            final_property_price, 
            cost, purchase_price, 
            new_property_price)[0]
        
        percentage_profit_added_value = ROI_percentage(
            final_property_price, 
            cost, purchase_price, 
            new_property_price)[1]
        
        added_value_ROI = ROI_percentage(
            final_property_price, 
            cost, purchase_price, 
            new_property_price)[2]

        # Expected values based on the logic
        inflation_difference = new_property_price - purchase_price
        expected_percentage_profit_inflation = round((inflation_difference / new_property_price) * 100, 2)

        added_value_difference = final_property_price - new_property_price
        expected_percentage_profit_added_value = round((added_value_difference / final_property_price) * 100, 2)

        expected_added_value_ROI = expected_percentage_profit_added_value  # When cost is zero, ROI should match the added value
        
        # Assert expected values match the returned values
        self.assertEqual(percentage_profit_inflation, expected_percentage_profit_inflation)
        self.assertEqual(percentage_profit_added_value, expected_percentage_profit_added_value)
        self.assertEqual(added_value_ROI, expected_added_value_ROI)

        
    # Test to check the behavior of ROI calculation as normal
    # ROI should reflect the added value minus the renovation cost.
    def test_roi_with_cost(self):
        
        final_property_price = 150000
        cost = 10000  # cost for renovations
        purchase_price = 100000
        new_property_price = 120000

        # Call the ROI function, store each result in new variables
        percentage_profit_inflation = ROI_percentage(
            final_property_price, 
            cost, purchase_price, 
            new_property_price)[0]
        
        percentage_profit_added_value = ROI_percentage(
            final_property_price, 
            cost, purchase_price, 
            new_property_price)[1]
        
        added_value_ROI = ROI_percentage(
            final_property_price, 
            cost, purchase_price, 
            new_property_price)[2]
        
        # Expected values based on the logic
        inflation_difference = new_property_price - purchase_price
        expected_percentage_profit_inflation = round((inflation_difference / new_property_price) * 100, 2)

        added_value_difference = final_property_price - new_property_price
        expected_percentage_profit_added_value = round((added_value_difference / final_property_price) * 100, 2)

        added_value_ROI_difference = final_property_price - new_property_price - cost
        expected_added_value_ROI = round((added_value_ROI_difference / final_property_price) * 100, 2)

        # Assert expected values match the returned values
        self.assertEqual(percentage_profit_inflation, expected_percentage_profit_inflation)
        self.assertEqual(percentage_profit_added_value, expected_percentage_profit_added_value)
        self.assertEqual(added_value_ROI, expected_added_value_ROI)


# Check to see if this script is being run directly or being imported as a module
if __name__ == '__main__':
    # Run all the test cases
    unittest.main()