import argparse
from ctypes import *

import speech_recognition as sr
import sys

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Papagaio's Speech Recognition System")
    parser.add_argument("-r", "--recognizer", choices=['google', 'sphinx', 'wit', 'bing', 'api', 'ibm'], default='sphinx')
    parser.add_argument("-s", "--sample_rate", default=44100)
    parser.add_argument("-k", "--key", nargs="*", help='Access key to the speech to text service. Username and '
                                                       'password for IBM')
    args = parser.parse_args()

    if args.recognizer == 'wit' and not args.key:
        print "Missing the key to access the service.\nUse --help for help."
        print "You must sign up for an account <https://wit.ai/> and create an app. You will need to add at least one " \
              "intent to the app before you can see the API key, though the actual intent settings don't matter."
        print "Alternatively, you can use the recognizers 'google' or 'sphinx' (offline) which do not require a key."
        sys.exit(0)
    elif args.recognizer == 'bing' and not args.key:
        print "Missing the key to access the service.\nUse --help for help."
        print "You must sign up for an account <https://www.microsoft.com/cognitive-services/en-us/speech-api> " \
              "with Microsoft Cognitive Services to use the bing recognizer"
        print "Alternatively, you can use the recognizers 'google' or 'sphinx' (offline) which do not require a key."
        sys.exit(0)
    elif args.recognizer == 'api' and not args.key:
        print "Missing the key to access the service.\nUse --help for help."
        print "You must sign up for an account <https://console.api.ai/api-client/#/signup> and create an api.ai " \
              "agent. To get the API client access token, go to the agent settings, go to the section titled " \
              "'API keys', and look for 'Client access token'. API client access tokens are 32-character lowercase " \
              "hexadecimal strings."
        print "Alternatively, you can use the recognizers 'google' or 'sphinx' (offline) which do not require a key."
        sys.exit(0)
    elif args.recognizer == 'ibm' and not args.key:
        print "Missing the key to access the service.\nUse --help for help."
        print "IBM Speech to Text requires an username and password. Unfortunately, these are not available " \
              "without signing up for an account <https://console.ng.bluemix.net/registration/>. Once logged into the " \
              "Bluemix console, follow the instructions for 'creating an IBM Watson service instance " \
              "<http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/getting_started/gs-credentials.shtml>, " \
              "where the Watson service is 'Speech To Text'. IBM Speech to Text usernames are strings of the form " \
              "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX, while passwords are mixed-case alphanumeric strings."
        print "Alternatively, you can use the recognizers 'google' or 'sphinx' (offline) which do not require a key."
        sys.exit(0)

    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

    asound = cdll.LoadLibrary('libasound.so')
    # Set error handler
    asound.snd_lib_error_set_handler(c_error_handler)

    r = sr.Recognizer()
    m = sr.Microphone(sample_rate=args.sample_rate)

    try:
        print("A moment of silence, please...")
        with m as source:
            r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))
        while True:
            print("Say something!")
            with m as source:
                audio = r.listen(source)
            print("Got it! Now to recognize it...")
            try:
                if args.recognizer == 'google':
                    value = r.recognize_google(audio)
                elif args.recognizer == 'wit':
                    value = r.recognize_wit(audio, args.key[0])
                elif args.recognizer == 'bing':
                    value = r.recognize_bing(audio, args.key[0])
                elif args.recognizer == 'api':
                    value = r.recognize_api(audio, args.key[0])
                elif args.recognizer == 'ibm':
                    value = r.recognize_ibm(audio, args.key[0], args.key[1])
                else:
                    value = r.recognize_sphinx(audio)
                print "You said: %s" % value
            except AttributeError:
                print("Oops! Something went wrong :(")
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:
        pass

    asound.snd_lib_error_set_handler(None)
