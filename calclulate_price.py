import numpy as np
from datetime import datetime

def calculate_dynamic_beer_price(input_json, min_adjustment=-0.15, max_adjustment=0.40, noise_level=0.02):
    """
    Calculates dynamic beer price based on behavioral and situational factors.
    Case-insensitive matching for all string inputs.
    
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
        'UserHistory': 'occasional',
        'AgeGroup': '45-54',
        'DeviceType': 'desktop',
        'OSType': 'windows',
        'ScreenSize': 'medium',
        'CompetitorPricing': 'similar',
        'RegionalDemand': 'medium',
        'CustomerRating': 'medium',
        'PaydayProximity': 'far',
        'TourismLevel': 'medium',
        'ProductMarketingStatus': 'medium',
        'DayOfWeek': 'wednesday',
        'DemandIndex': 'medium',
        'SpecialOccasion': 'none',
        'Temperature': 20,
        'WeatherCondition': 'clear',
        'InventoryLevel': 'medium',
        'CityType': 'suburban',
        'WeekdayType': 'weekday',
        'DayType': 'regular'
    }
    
    # Convert input values to lowercase
    input_json_lower = {k: v.lower() if isinstance(v, str) else v for k, v in input_json.items()}
    
    # Merge input JSON with defaults
    data = {**defaults, **input_json_lower}
    
    # Behavioral Markups (all keys in lowercase)
    user_history_markup = {
        'new': 0.98, 'frequent': 1.02, 'premium': 1.03, 'vip': 1.04, 
        'occasional': 1.00, 'lapsed': 0.97
    }
    age_group_markup = {
        '18-24': 1.02, '25-34': 1.03, '35-44': 1.02, '45-54': 1.0, '55+': 0.99
    }
    device_type_markup = {
        'mobile': 1.02, 'desktop': 1.00, 'tablet': 1.01, 'smart tv': 1.00
    }
    os_type_markup = {
        'ios': 1.03, 'android': 1.02, 'windows': 1.00, 'macos': 1.01
    }
    screen_size_markup = {
        'small': 0.98, 'medium': 1.00, 'large': 1.02
    }
    competitor_pricing_markup = {
        'lower': 0.98, 'similar': 1.00, 'higher': 1.02
    }
    regional_demand_markup = {
        'low': 0.98, 'medium': 1.00, 'high': 1.04
    }
    customer_rating_markup = {
        'low': 0.97, 'medium': 1.00, 'high': 1.03
    }
    payday_proximity_markup = {
        'far': 1.0, 'near': 1.02
    }
    tourism_level_markup = {
        'low': 0.98, 'medium': 1.0, 'high': 1.04
    }
    product_marketing_status_markup = {
        'low': 0.98, 'medium': 1.0, 'high': 1.03
    }
    
    def get_time_day_markup(hour, day):
        time_markup = 0.98 if hour < 12 else (1.00 if hour < 16 else 1.02)
        day_markup = {
            'monday': 0.98, 'tuesday': 0.99, 'wednesday': 1.00, 
            'thursday': 1.01, 'friday': 1.04, 'saturday': 1.05, 'sunday': 1.02
        }
        happy_hour_factor = 0.98 if 16 <= hour < 19 else 1.00
        return time_markup * day_markup.get(day, 1.00) * happy_hour_factor

    demand_markup = {
        'very low': 0.95, 'low': 0.97, 'medium': 1.00, 
        'high': 1.02, 'very high': 1.04
    }
    event_markup = {
        'none': 1.00, 'sports event': 1.05, 'festival': 1.04, 
        'holiday': 1.04, 'concert': 1.06
    }
    
    def get_weather_markup(temp, condition):
        temp_factor = 1 + (temp - 20) * 0.005
        weather_factors = {
            'sunny': 1.02, 'rainy': 0.98, 'cloudy': 0.99, 
            'snow': 1.02, 'clear': 1.0
        }
        return temp_factor * weather_factors.get(condition, 1.00)

    inventory_level_markup = {'low': 1.04, 'medium': 1.0, 'high': 0.98}
    city_type_markup = {'urban': 1.03, 'suburban': 1.0, 'rural': 0.98}
    weekday_type_markup = {'weekday': 1.00, 'weekend': 1.03}
    day_type_markup = {'regular': 1.00, 'holiday': 1.03}

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