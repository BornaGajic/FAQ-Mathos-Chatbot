# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from logging import info
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase

import json

class ActionMoreInfoProgramme(Action):

    def name(self) -> Text:
        return "action_more_info_programme"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        programme = ""
        degree = ""

        for e in tracker.latest_message['entities']:
            if e['entity'] == 'programme':
                programme = e['value']
            elif e['entity'] == 'degree':
                degree = e['value']
        print("more info action")
        print(f"program {programme}, degree {degree}")

        with open('./knowledge_base_data/study_programme_info.json') as json_file:
            data = json.load(json_file)

            try:
                for (key, info) in data[degree][programme].items():        
                    dispatcher.utter_message(text=f"{info}\n")
            except:
                if len(programme) > 0 or len(degree) > 0:
                    dispatcher.utter_message(text="Sorry, I don't understand your request. Please specify degree and programme that you are interested in.")
                else:
                    dispatcher.utter_message(text="Sorry, I don't understand your request.")

        return []

class ActionCourseList(Action):

    def name(self) -> Text:
        return "action_course_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        programme = ""
        degree = ""

        for e in tracker.latest_message['entities']:
            if e['entity'] == 'programme':
                programme = e['value']
            elif e['entity'] == 'degree':
                degree = e['value']
        print("course action")
        print(f"program {programme}, degree {degree}")

        with open('./knowledge_base_data/course_list.json') as json_file:
            data = json.load(json_file)

            try:
                if programme == "":
                    dispatcher.utter_message(text="Please specify a programme that you are interested in.")
                elif degree == "":
                    for (degrees, content) in data.items():
                        
                        if programme in content:
                            for (key, courses) in content.items():
                                k = key.replace('#', ' ')
                                dispatcher.utter_message(text=f"{k}\n")

                                for (id, name) in courses.items():
                                    dispatcher.utter_message(text=f"{id}, {name}\n")
                            break
                else:
                    for (key, courses) in data[degree][programme].items():
                        k = key.replace('#', ' ')
                        dispatcher.utter_message(text=f"{k}\n")

                        for (id, name) in courses.items():
                            dispatcher.utter_message(text=f"{id}, {name}\n")
            except:
                dispatcher.utter_message(text="Sorry, I don't understand your request.")

        return []

class ActionCourseInfo(Action):

    def name(self) -> Text:
        return "action_course_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course_id = ""
        course_name = ""

        for e in tracker.latest_message['entities']:
            if e['entity'] == 'course_id':
                course_id = e['value']
            elif e['entity'] == 'course_name':
                course_name = e['value']
        
        print("course info")
        print(f"id {course_id}, name {course_name}")

        with open('./knowledge_base_data/course_info.json') as json_file:
            data = json.load(json_file)

            try:
                for (key, course_info) in data.items():
                    if course_id.lower() in str(key).lower() and course_name.lower() in str(key).lower():
                        dispatcher.utter_message(text=course_info)
            except:
                dispatcher.utter_message(text="Sorry, I don't understand your request.")

        return []