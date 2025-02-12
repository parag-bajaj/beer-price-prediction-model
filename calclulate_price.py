import numpy as np
import pandas as pd
from datetime import datetime
import json

def calculate_dynamic_beer_price(df, min_adjustment=-0.15, max_adjustment=0.40, noise_level=0.02):
    """
    Calculates dynamic beer price based on behavioral and situational factors.
    """
    # Behavioral Markups
    user_history_markup = {
        'New': 0.98, 'Frequent': 1.02, 'Premium': 1.03, 'VIP': 1.04, 'Occasional': 1.00, 'Lapsed': 0.97
    }
    age_group_markup = {
        '18-24': 1.02, '25-34': 1.03, '35-44': 1.02, '45-54': 1.01, '55+': 0.99
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
        'Low': 0.98, 'Medium': 1.01, 'High': 1.04
    }
    customer_rating_markup = {
        'Low': 0.97, 'Medium': 1.00, 'High': 1.03
    }
    payday_proximity_markup = {
        'Far': 0.99, 'Near': 1.02
    }
    tourism_level_markup = {
        'Low': 0.98, 'Medium': 1.01, 'High': 1.04
    }
    product_marketing_status_markup = {
        'Low': 0.98, 'Medium': 1.01, 'High': 1.03
    }
    def get_time_day_markup(hour, day):
        time_markup = 0.98 if hour < 12 else (1.00 if hour < 16 else 1.02)
        day_markup = {'Monday': 0.98, 'Tuesday': 0.99, 'Wednesday': 1.00, 'Thursday': 1.01, 'Friday': 1.04, 'Saturday': 1.05, 'Sunday': 1.02}
        happy_hour_factor = 0.98 if 16 <= hour < 19 else 1.00
        return time_markup * day_markup.get(day, 1.00) * happy_hour_factor

    demand_markup = {'Very Low': 0.95, 'Low': 0.97, 'Medium': 1.00, 'High': 1.02, 'Very High': 1.04}
    event_markup = {'None': 1.00, 'Sports Event': 1.05, 'Festival': 1.04, 'Holiday': 1.04, 'Concert': 1.06}

    def get_weather_markup(row):
        temp_factor = 1 + (row.get('Temperature', 20) - 20) * 0.005
        weather_factors = {'Sunny': 1.02, 'Rainy': 0.98, 'Cloudy': 0.99, 'Snow': 1.02, 'Clear': 1.01}
        return temp_factor * weather_factors.get(row.get('WeatherCondition', 'Clear'), 1.00)

    inventory_level_markup = {'Low': 1.04, 'Medium': 1.02, 'High': 0.98}
    city_type_markup = {'Urban': 1.03, 'Suburban': 1.02, 'Rural': 0.98}
    weekday_type_markup = {'Weekday': 1.00, 'Weekend': 1.03}
    day_type_markup = {'Regular': 1.00, 'Holiday': 1.03}

    base_selling_price=df['BaseSellingPrice']
    max_price = base_selling_price * (1 + max_adjustment)
    min_price = base_selling_price * (1 + min_adjustment)
    
    base_price = df['BaseSellingPrice']
    base_price *= df['UserHistory'].map(user_history_markup)
    base_price *= df['AgeGroup'].map(age_group_markup)
    base_price *= df['DeviceType'].map(device_type_markup)
    base_price *= df['OSType'].map(os_type_markup)
    base_price *= df['ScreenSize'].map(screen_size_markup)
    base_price *= df['CompetitorPricing'].map(competitor_pricing_markup)
    base_price *= df['RegionalDemand'].map(regional_demand_markup)
    base_price *= df['CustomerRating'].map(customer_rating_markup)
    base_price *= df['PaydayProximity'].map(payday_proximity_markup)
    base_price *= df['TourismLevel'].map(tourism_level_markup)
    base_price *= df['ProductMarketingStatus'].map(product_marketing_status_markup)
    base_price *= df.apply(lambda x: get_time_day_markup(datetime.now().hour, x['DayOfWeek']), axis=1)
    base_price *= df['DemandIndex'].map(demand_markup)
    base_price *= df['SpecialOccasion'].map(event_markup)
    base_price *= df.apply(get_weather_markup, axis=1)
    base_price *= df['InventoryLevel'].map(inventory_level_markup)
    base_price *= df['CityType'].map(city_type_markup)
    base_price *= df['WeekdayType'].map(weekday_type_markup)
    base_price *= df['DayType'].map(day_type_markup)
    # noise = np.random.normal(0, noise_level, len(df))
    # base_price *= (1 + noise)
    price = np.clip(float(base_price.iloc[0]), float(min_price.iloc[0]), float(max_price.iloc[0]))    
    return price