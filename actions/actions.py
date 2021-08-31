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

        with open('./knowledge_base_data/study_programme_info.json', encoding="utf8") as json_file:
            data = json.load(json_file)

            try:
                if not programme:
                    dispatcher.utter_message(text="Please specify programme.")
                    return []
                elif programme and not degree:

                    for (_degree, _programmes) in data.items():
                        if programme in _programmes:
                            for (key, info) in data[_degree][programme].items():
                                dispatcher.utter_message(text=info)
                else:
                    for (key, info) in data[degree][programme].items():        
                        dispatcher.utter_message(text=info)
            except:
                dispatcher.utter_message(text="Sorry, I don't understand your request.")

        return []

class ActionAdmissionInfo(Action):

    def name(self) -> Text:
        return "action_admission_info"

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

        print("more admission action")
        print(f"program {programme}, degree {degree}")

        with open('./knowledge_base_data/admission_info.json', encoding="utf8") as admission_file:
                admission_info = json.load(admission_file)
                message = ""

                try:
                    if not programme:
                        dispatcher.utter_message(text="Please specify programme.")
                        return []
                    elif programme and not degree:

                        for (_degree, _programmes) in admission_info.items():
                            
                            if programme in _programmes:

                                for (key, info) in admission_info[_degree][programme].items():
                                    
                                    if type(info) is dict:
                                        for (k, i) in info.items():
                                            dispatcher.utter_message(text=i)
                                    else:
                                        dispatcher.utter_message(text=info)

                                break
                    else:
                        for (key, info) in admission_info[degree][programme].items():   
                            if type(info) is dict:
                                for (k, i) in info.items():
                                    dispatcher.utter_message(text=i)
                            else:
                                dispatcher.utter_message(text=info)
                except:
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

        with open('./knowledge_base_data/course_list.json', encoding="utf8") as json_file:
            data = json.load(json_file)
            message = ""
            try:
                if not programme:
                    dispatcher.utter_message(text="Please specify a programme that you are interested in.")
                    return []
                elif not degree:
                    for (degrees, content) in data.items():
                        
                        if programme in content:
                            for (year, courses) in content[programme].items():
                                k = year.replace('#', ' ')
                                message += k + "\n"
                                                                
                                for (id, name) in courses.items():
                                    message += id + ", " + name + "\n"

                                message += " \n"
                            break
                else:
                    for (key, courses) in data[degree][programme].items():
                        k = key.replace('#', ' ')
                        message += k + "\n"
                        
                        for (id, name) in courses.items():
                            message += id + ", " + name + " \n"

                        message += " \n"

                dispatcher.utter_message(text=str(message))
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

        with open('./knowledge_base_data/course_info.json', encoding='utf8') as json_file:
            data = json.load(json_file)
            message = ""
            try:
                for (key, course_info) in data.items():
                    csId = key.split('/')[0]
                    csName = key.split('/')[1]

                    if course_id.lower() in csId.lower() and course_name.lower() in csName.lower():
                        dispatcher.utter_message(text=str(course_info))
                        break
            except:
                dispatcher.utter_message(text="Sorry, I don't understand your request.")

        return []

class ActionStaffEmail(Action):

    def name(self) -> Text:
        return "action_staff_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        staff = ""

        for e in tracker.latest_message['entities']:
            if e['entity'] == 'staff':
                staff = e['value']
        
        print("course info")
        print(f"staff {staff}")

        with open('./knowledge_base_data/staff_email.json', encoding="utf8") as json_file:
            data = json.load(json_file)

            try:
                dispatcher.utter_message(text=f"The email you're looking for is {data[staff]}")
            except:
                dispatcher.utter_message(text="Sorry, I don't understand your request.")

        return []