from datetime import datetime, timedelta
import json
import heapq
from typing import Any

class OfferFilter:
    VALID_CATEGORIES = {
        'Restaurant': 1,
        'Retail': 2,
        'Activity': 4,
    }

    DAYS_TO_CHECKIN = 5

    def __init__(self, path: str):
        
        # Open the file and load the JSON data
        with open(path, 'r') as file:
            data = json.load(file)
        self.offer_data = data

        
    def load_checkin_date(self):
        while True:
            try:
                input_date = input("Please enter your check-in date (follow YYYY-MM-DD): ")
                self.checkin_date = datetime.strptime(input_date, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format. Please try again.")
        

    def filter_by_date(self):
        valid_offers = []

        #get date from offer
        for offer in self.offer_data.get('offers', []):
            valid_date = datetime.strptime(offer.get('valid_to', ''), '%Y-%m-%d')

            # Check if the offer is valid
            if self.is_valid_date(valid_date):
                valid_offers.append(offer)
        self.offer_data['offers'] = valid_offers

    def is_valid_date(self, valid_date):
        return valid_date >= self.checkin_date + timedelta(days=self.DAYS_TO_CHECKIN)


    def filter_by_categories(self):
        valid_offers= []

        for offer in self.offer_data.get('offers', []):
            #check if the category is valid
            if offer['category'] in self.VALID_CATEGORIES.values(): 
                valid_offers.append(offer)
            self.offer_data['offers'] = valid_offers

    
    def filter_by_shortest_distance(self):
        for offer in self.offer_data['offers']:
            #get min distance from each offer
            min_distance_offer = min(offer['merchants'], key=lambda x: x['distance'])
            offer['merchants'] = min_distance_offer


    def filter_by_shortest_distance_each_category(self):
        #group same category
        grouped_category = {}
        
        for offer in self.offer_data.get('offers', []):
            if offer['category'] not in grouped_category:
                grouped_category[offer['category']] = [offer]
            else:
                grouped_category[offer['category']].append(offer)

        #take shortest distance from each category
        shortest_distance_offers = []
        for sub_offer in grouped_category.values():
            min_distance_offer = min(sub_offer, key=lambda x: x['merchants']['distance'])
            shortest_distance_offers.append(min_distance_offer)

        self.offer_data['offers'] = shortest_distance_offers
        

    def filter_two_closest_offers(self):
        #get the 2 smallest distance offer
        smallest_two = heapq.nsmallest(2,  self.offer_data['offers'], key=lambda x: x['merchants']['distance'])
        self.offer_data['offers'] = smallest_two
 
        
    def return_offer(self):
        self.load_checkin_date()
        self.filter_by_date()
        self.filter_by_categories()
        self.filter_by_shortest_distance()
        self.filter_by_shortest_distance_each_category()
        self.filter_two_closest_offers()

        #output json file
        path = 'output.json'
        with open(path, 'w') as json_file:
            json.dump(self.offer_data, json_file, indent=2)
        json_response = json.dumps(self.offer_data,indent=2)
    
        return json_response


