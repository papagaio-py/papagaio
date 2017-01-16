import argparse
import timeit
from ctypes import *

import speech_recognition

import settings_accounts as accounts

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass


# AVAILABLE_RECOGNIZERS = ['google', 'sphinx', 'wit', 'bing', 'api', 'ibm', 'all']
AVAILABLE_RECOGNIZERS = ['google', 'sphinx', 'wit', 'all']

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Papagaio's Speech Recognition System")
    parser.add_argument("-r", "--recognizers", nargs='*', choices=AVAILABLE_RECOGNIZERS, default='sphinx')
    parser.add_argument("-s", "--sample_rate", default=44100)
    args = parser.parse_args()

    recognizer_list = args.recognizers
    if 'all' in recognizer_list:
        recognizer_list = filter(lambda x: x != 'all', AVAILABLE_RECOGNIZERS)

    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

    asound = cdll.LoadLibrary('libasound.so')
    # Set error handler
    asound.snd_lib_error_set_handler(c_error_handler)

    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone(sample_rate=args.sample_rate)

    try:
        print("A moment of silence, please...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(recognizer.energy_threshold))
        while True:
            print("\nSay something!")
            with microphone as source:
                audio = recognizer.listen(source)
            print("Got it! Now to recognize it...")
            for current_option in recognizer_list:
                value = ''
                tic = timeit.default_timer()
                try:
                    if current_option == 'google':
                        value = recognizer.recognize_google(audio)
                    elif current_option == 'wit':
                        value = recognizer.recognize_wit(audio, accounts.ACCESS_KEY_WIT)
                    # elif args.recognizer == 'bing':
                    #     value = recognizer.recognize_bing(audio, args.key[0])
                    # elif args.recognizer == 'api':
                    #     value = r.recognize_api(audio, args.key[0])
                    # elif args.recognizer == 'ibm':
                    #     value = r.recognize_ibm(audio, args.key[0], args.key[1])
                    else:
                        value = recognizer.recognize_sphinx(audio)
                    msg = value
                except AttributeError:
                    msg = "Oops! Something went wrong :("
                except speech_recognition.UnknownValueError:
                    msg = "Oops! Didn't catch that"
                except speech_recognition.RequestError as e:
                    msg = "Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e)
                toc = timeit.default_timer()
                print "%s: %s - elapsed time: %s s" % (current_option.upper(), msg, toc - tic)
    except KeyboardInterrupt:
        pass

    asound.snd_lib_error_set_handler(None)
