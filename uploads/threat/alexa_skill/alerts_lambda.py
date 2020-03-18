# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.utils import get_slot_value, get_user_id
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
import requests
from requests.exceptions import ConnectionError
from datetime import datetime
from dateutil import tz

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

number_string = {1: 'first', 2: 'second', 3: 'third', 4: 'forth', 5: 'fifth', 6: 'sixth', 7: 'seventh', 8: 'eighth',
                 9: 'ninth', 10: 'tenth'}


# Created Skill Launch/Open/Start
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch/Open/Start."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        user_id = get_user_id(handler_input=handler_input)
        print(user_id)
        speak_output = "Welcome, You can ask for top threats or alarms?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# Custom top 5/10/15/20/30...and so on threats intent
class NumberofThreatsIntentHandler(AbstractRequestHandler):
    """Handler for Number of threats Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NumberofThreatsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # domain = 'http://threatdb.leosys.net'
        domain = 'http://123.252.203.115'
        # # getting the number of top threats requires to end user
        threats_number = get_slot_value(
            handler_input=handler_input, slot_name="number_of_required")
        # threats_number = 3
        uri = '/api/threats/top/' + str(threats_number)
        # top_or_critical = get_slot_value(
        #     handler_input=handler_input, slot_name="top_or_critical")
        url = domain + uri
        # headers = {
        #     "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGl0eSI6IjE3Mi4xNi4wLjE2NyJ9."
        #                      "RrHDpg1dHhWEZDdNeoJhSdhnz33yHjaqvEk-xGYe7Lk",
        # }
        try:
            response = requests.get(url)
            if response.status_code == 200:
                threats_results = response.json()
                speech_text = 'The top {} threats of the day are. '.format(threats_number)
                for index, threats_result in enumerate(threats_results):
                    threat_name = threats_result['threat_name']
                    threat_type = threats_result['threat_type']
                    if threats_result['file_type_extension']:
                        file_type_extension = threats_result['file_type_extension']
                        # file_type = ' '.join(file_type_extension[i:i + 1] for i in range(0, len(file_type_extension), 1))
                    else:
                        file_type = "Unknown"
                    if threats_number == 1:
                        speech_text = 'The top threats for the day is. '
                        speech_text += "Threat name is {0} <break time='0.5s'/>" \
                                       "of type {1} <break time='0.5s'/> with extension" \
                                       "is <say-as interpret-as='spell-out'>{2}</say-as>.".format(threat_name,
                                                                                                  threat_type,
                                                                                                  file_type_extension)
                    else:
                        speech_text += "{0}. Threat name is {1} <break time='0.5s'/>" \
                                       "of type {2} <break time='0.5s'/> with extension is " \
                                       "<say-as interpret-as='spell-out'>{3}</say-as> <break time='0.5s'/>".format(
                            number_string[index + 1],
                            threat_name,
                            threat_type,
                            file_type_extension)
                speak_output = speech_text
            else:
                speak_output = "Sorry, couldn't able to get threats. Try again."
        except ConnectionError as e:
            speak_output = "Sorry, I am having trouble with the request. Try again."
        # speak_output = "Sorry, I am having trouble with the request. Try again." + str(threats_number)
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask(speak_output)
                # ask "add a reprompt if you want to keep the session open for the user to respond"
                .response
        )


# Custom top 1 or 5 threat intent
class TopOneorFiveThreatIntentHandler(AbstractRequestHandler):
    """Handler for Top One threats Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TopOneorFiveThreatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # domain = 'http://threatdb.leosys.net'
        domain = 'http://123.252.203.115'
        is_or_are = get_slot_value(
            handler_input=handler_input, slot_name="is_or_are")
        if is_or_are == 'is':
            threats_number = 1
        else:
            threats_number = 5
        top_or_critical = get_slot_value(
            handler_input=handler_input, slot_name="top_or_critical")
        if top_or_critical == 'top' or top_or_critical == 'critical':
            pass
        else:
            # speak_output = top_or_critical
            speak_output = "Sorry, I don't know that. Pleas ask for what are the top or critcal threats for the day or what is the top or critical threats for the day."
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    # .ask(speak_output)
                    # ask "add a reprompt if you want to keep the session open for the user to respond"
                    .response
            )
        uri = '/api/threats/top/' + str(threats_number)
        url = domain + uri
        headers = {
            "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGl0eSI6IjE3Mi4xNi4wLjE2NyJ9."
                             "RrHDpg1dHhWEZDdNeoJhSdhnz33yHjaqvEk-xGYe7Lk",
        }
        try:
            response = requests.get(url)
            if response.status_code == 200:
                threats_results = response.json()
                if threats_number == 1:
                    speech_text = 'The {} threat of the day is. '.format(top_or_critical)
                else:
                    speech_text = 'Here are the {} threats for the day. '.format(top_or_critical)
                for index, threats_result in enumerate(threats_results):
                    threat_name = threats_result['threat_name']
                    threat_type = threats_result['threat_type']
                    file_type_extension = threats_result['file_type_extension']
                    # file_type = ' '.join(file_type_extension[i:i + 1] for i in range(0, len(file_type_extension), 1))
                    if threats_number == 1:
                        speech_text += "Threat name is {0} <break time='0.5s'/>" \
                                       "of type {1} <break time='0.5s'/> with extension" \
                                       "is <say-as interpret-as='spell-out'>{2}</say-as>.".format(threat_name,
                                                                                                  threat_type,
                                                                                                  file_type_extension)
                    else:
                        speech_text += "{0}. Threat name is {1} <break time='0.5s'/>" \
                                       "of type {2} <break time='0.5s'/> with extension is " \
                                       "<say-as interpret-as='spell-out'>{3}</say-as> <break time='0.5s'/>".format(
                            number_string[index + 1],
                            threat_name,
                            threat_type,
                            file_type_extension)
                speak_output = speech_text

            else:
                speak_output = "Sorry, couldn't able to get threats. Try again."
        except ConnectionError as e:
            speak_output = "Sorry, I am having trouble with the request. Try again."
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask(speak_output)
                # ask "add a reprompt if you want to keep the session open for the user to respond"
                .response
        )


# Custom alert notification intent
class AlertNotifiactionThreatsIntentHandler(AbstractRequestHandler):
    """Handler for Alert notification threats Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AlertNotifiactionThreatsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # domain = 'http://threatdb.leosys.net'
        domain = 'http://123.252.203.115'
        # getting the number of top threats requires to end user
        # threats_number = get_slot_value(
        #     handler_input=handler_input, slot_name="number_of_threats_required")
        uri = '/api/alarm/alerts'  # + str(threats_number)
        url = domain + uri
        headers = {
            "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGl0eSI6IjE3Mi4xNi4wLjE2NyJ9."
                             "RrHDpg1dHhWEZDdNeoJhSdhnz33yHjaqvEk-xGYe7Lk",
        }
        try:
            utc_tz = tz.gettz('UTC')
            india_tz = tz.gettz('Asia/Kolkata')
            current_time = datetime.now()  # .strftime('%B %d %Y %I:%M %p')
            utc = current_time.replace(tzinfo=utc_tz)
            india_time_with_offset = utc.astimezone(india_tz)
            india_time_without_offset = india_time_with_offset.replace(tzinfo=None)
            current_time = india_time_without_offset.strftime('%d %B %Y %I:%M %p')
            response = requests.get(url)
            if response.status_code == 200:
                threats_results = response.json()
                if not threats_results['last_read']:
                    last_read = india_time_without_offset.strftime('%d %B %Y 12:00 AM')
                else:
                    last_read = threats_results['last_read']
                speech_text = "The new alarm from time {} to time {} are <break time='0.5s'/> ".format(last_read,
                                                                                                       current_time)
                if len(threats_results['data']) > 0:
                    for index, threats_result in enumerate(threats_results['data']):
                        threat_name = threats_result['name']
                        risk = threats_result['risk']
                        source_ip = threats_result['source_ip']
                        destination_ip = threats_result['destination_ip']
                        speech_text += "{0}. Alarm with name is <break time='0.5s'/> {1}, has been triggered inside your environment with a" \
                                       " risk value of <break time='0.5s'/> {2}. It's source IP is <break time='0.5s'/> {3} and destination " \
                                       " IP is <break time='0.5s'/> {4}. <break time='0.5s'/>".format(
                            number_string[index + 1],
                            threat_name, risk,
                            source_ip,
                            destination_ip)
                    speak_output = speech_text
                else:
                    speak_output = "You don't have any L T S alarm"
            else:
                # speak_output = "The new alarm from time {} to time {}. ".format(current_time, current_time)
                speak_output = "Sorry, couldn't able to get alarms. Try again."
        except ConnectionError as e:
            speak_output = "Sorry, I am having trouble with the request. Try again."
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask(speak_output)
                # ask "add a reprompt if you want to keep the session open for the user to respond"
                .response
        )


# Amazon help intent
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can ask to alexa for help"
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask(speak_output)
                .response
        )


# Amazon fallback intent
class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for fallback Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Sorry, I had trouble doing what you asked. Please try again."
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask(speak_output)
                .response
        )


# Amazon Cancel or Stop Intent
class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


# Amazon Session end Intent
class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.
        return handler_input.response_builder.response


# Amazon Navigate or reflect Intent
class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


# Amazon Exception Intent
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        speak_output = "Sorry, I had trouble doing what you asked. Please try again."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(NumberofThreatsIntentHandler())
sb.add_request_handler(TopOneorFiveThreatIntentHandler())
sb.add_request_handler(AlertNotifiactionThreatsIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()