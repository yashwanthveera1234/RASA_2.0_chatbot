# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from geopy.geocoders import Nominatim
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
import requests

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionPostal(Action):

    def name(self) -> Text:
        return "action_postal_code"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        print(entities)

        for e in entities:
            if e["entity"]=='pin':
                name = e['value']

                geolocator = Nominatim(user_agent="geoapiExercises")

                location = geolocator.geocode(name)

                stri = location[0][:-15]
                stri = str(stri)
                message = stri
                dispatcher.utter_message(message)

            dispatcher.utter_message("(choose services from the below categories)")
            response = requests.get("http://ec2-3-23-130-174.us-east-2.compute.amazonaws.com:8000/categories")
            res = response.text[9:-2].split(",")
            for data in res:
                dispatcher.utter_message(data)


        return []

class ActionHelp(Action):

    def name(self) -> Text:
        return "action_help"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pinc = tracker.get_slot("pin")
        cate = tracker.get_slot("cat")

        message = "Do you want to get the {} for - {}. Press yes to confirm and no to change another pincode".format(cate,pinc)
        dispatcher.utter_message(text=message)

        return []

class Actionone(Action):

    def name(self) -> Text:
        return "action_one"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get("http://ec2-3-23-130-174.us-east-2.compute.amazonaws.com:8000/categories")
        res = response.text[9:-2].split(",")
        for data in res:
            dispatcher.utter_message(data)



        return []

class Actioncategories(Action):

    def name(self) -> Text:
        return "action_categories"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pinc = tracker.get_slot("pin")
        cate = tracker.get_slot("cat")

        message = "thanks for providing the  pincode-{} and the service {} ,you want.-->(type Help)".format(pinc,cate)
        dispatcher.utter_message(text=message)


        return []

class Actionno(Action):

    def name(self) -> Text:
        return "action_no"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Please share pincode and service you want")

        return []

class Actionyes(Action):

    def name(self) -> Text:
        return "action_happy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pinc = tracker.get_slot("pin")
        cate = tracker.get_slot("cat")

        geolocator = Nominatim(user_agent="geoapiExercises")

        location = geolocator.geocode(pinc)

        stri = location[0][:-15]
        stri = str(stri)
        message = "we will send resources('{}') to this adress({}) ".format(cate,stri)
        dispatcher.utter_message(message)
        dispatcher.utter_message("thanks for contacting. If you have any emergency at any location please provide the pincode and the service you want Have a great day.")
        dispatcher.utter_message("STAY HOME STAY SAFE")




        return []


