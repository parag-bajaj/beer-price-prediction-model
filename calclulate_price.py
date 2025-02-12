import numpy as np
from datetime import datetime

def calculate_dynamic_beer_price(input_json, min_adjustment=-0.15, max_adjustment=0.40, noise_level=0.02):
    """
    Calculates dynamic beer price based on behavioral and situational factors.
    
    Args:
        input_json (dict): JSON containing pricing factors
        min_adjustment (float): Minimum price adjustment multiplier
        max_adjustment (float): Maximum price adjustment multiplier
        noise_level (float): Level of random noise to add to price
    
    Returns:
        float: Calculated dynamic price
    """
    # Default values for all possible inputs
    defaults = {
        'UserHistory': 'Occasional',
        'AgeGroup': '45-54',
        'DeviceType': 'Desktop',
        'OSType': 'Windows',
        'ScreenSize': 'Medium',
        'CompetitorPricing': 'Similar',
        'RegionalDemand': 'Medium',
        'CustomerRating': 'Medium',
        'PaydayProximity': 'Far',
        'TourismLevel': 'Medium',
        'ProductMarketingStatus': 'Medium',
        'DayOfWeek': 'Wednesday',
        'DemandIndex': 'Medium',
        'SpecialOccasion': 'None',
        'Temperature': 20,
        'WeatherCondition': 'Clear',
        'InventoryLevel': 'Medium',
        'CityType': 'Suburban',
        'WeekdayType': 'Weekday',
        'DayType': 'Regular'
    }
    
    # Merge input JSON with defaults
    data = {**defaults, **input_json}
    
    # Behavioral Markups
    user_history_markup = {
        'New': 0.98, 'Frequent': 1.02, 'Premium': 1.03, 'VIP': 1.04, 
        'Occasional': 1.00, 'Lapsed': 0.97
    }
    age_group_markup = {
        '18-24': 1.02, '25-34': 1.03, '35-44': 1.02, '45-54': 1.0, '55+': 0.99
    }
    device_type_markup = {
        'Mobile': 1.02, 'Desktop': 1.00, 'Tablet': 1.01, 'Smart TV': 1.00
    }
    os_type_markup = {
        'iOS': 1.03, 'Android': 1.02, 'Windows': 1.00, 'MacOS': 1.01
    }
    screen_size_markup = {
        'Small': 0.98, 'Medium': 1.00, 'Large': 1.02
    }
    competitor_pricing_markup = {
        'Lower': 0.98, 'Similar': 1.00, 'Higher': 1.02
    }
    regional_demand_markup = {
        'Low': 0.98, 'Medium': 1.00, 'High': 1.04
    }
    customer_rating_markup = {
        'Low': 0.97, 'Medium': 1.00, 'High': 1.03
    }
    payday_proximity_markup = {
        'Far': 1.0, 'Near': 1.02
    }
    tourism_level_markup = {
        'Low': 0.98, 'Medium': 1.0, 'High': 1.04
    }
    product_marketing_status_markup = {
        'Low': 0.98, 'Medium': 1.0, 'High': 1.03
    }
    
    def get_time_day_markup(hour, day):
        time_markup = 0.98 if hour < 12 else (1.00 if hour < 16 else 1.02)
        day_markup = {
            'Monday': 0.98, 'Tuesday': 0.99, 'Wednesday': 1.00, 
            'Thursday': 1.01, 'Friday': 1.04, 'Saturday': 1.05, 'Sunday': 1.02
        }
        happy_hour_factor = 0.98 if 16 <= hour < 19 else 1.00
        return time_markup * day_markup.get(day, 1.00) * happy_hour_factor

    demand_markup = {
        'Very Low': 0.95, 'Low': 0.97, 'Medium': 1.00, 
        'High': 1.02, 'Very High': 1.04
    }
    event_markup = {
        'None': 1.00, 'Sports Event': 1.05, 'Festival': 1.04, 
        'Holiday': 1.04, 'Concert': 1.06
    }
    
    def get_weather_markup(temp, condition):
        temp_factor = 1 + (temp - 20) * 0.005
        weather_factors = {
            'Sunny': 1.02, 'Rainy': 0.98, 'Cloudy': 0.99, 
            'Snow': 1.02, 'Clear': 1.0
        }
        return temp_factor * weather_factors.get(condition, 1.00)

    inventory_level_markup = {'Low': 1.04, 'Medium': 1.0, 'High': 0.98}
    city_type_markup = {'Urban': 1.03, 'Suburban': 1.0, 'Rural': 0.98}
    weekday_type_markup = {'Weekday': 1.00, 'Weekend': 1.03}
    day_type_markup = {'Regular': 1.00, 'Holiday': 1.03}

    # Calculate base price with all markups
    base_selling_price = data['BaseSellingPrice']
    max_price = base_selling_price * (1 + max_adjustment)
    min_price = base_selling_price * (1 + min_adjustment)
    
    # Apply all markups
    base_price = base_selling_price
    base_price *= user_history_markup.get(data['UserHistory'], 1.0)
    base_price *= age_group_markup.get(data['AgeGroup'], 1.0)
    base_price *= device_type_markup.get(data['DeviceType'], 1.0)
    base_price *= os_type_markup.get(data['OSType'], 1.0)
    base_price *= screen_size_markup.get(data['ScreenSize'], 1.0)
    base_price *= competitor_pricing_markup.get(data['CompetitorPricing'], 1.0)
    base_price *= regional_demand_markup.get(data['RegionalDemand'], 1.0)
    base_price *= customer_rating_markup.get(data['CustomerRating'], 1.0)
    base_price *= payday_proximity_markup.get(data['PaydayProximity'], 1.0)
    base_price *= tourism_level_markup.get(data['TourismLevel'], 1.0)
    base_price *= product_marketing_status_markup.get(data['ProductMarketingStatus'], 1.0)
    base_price *= get_time_day_markup(datetime.now().hour, data['DayOfWeek'])
    base_price *= demand_markup.get(data['DemandIndex'], 1.0)
    base_price *= event_markup.get(data['SpecialOccasion'], 1.0)
    base_price *= get_weather_markup(data['Temperature'], data['WeatherCondition'])
    base_price *= inventory_level_markup.get(data['InventoryLevel'], 1.0)
    base_price *= city_type_markup.get(data['CityType'], 1.0)
    base_price *= weekday_type_markup.get(data['WeekdayType'], 1.0)
    base_price *= day_type_markup.get(data['DayType'], 1.0)
    
    
    # Clip price to min/max range
    final_price = np.clip(base_price, min_price, max_price)
    
    return round(final_price, 2)