#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

def speech_recognition():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    audio_input = r.recognize_google(audio)

    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`

        print("Google Speech Recognition thinks you said " + audio_input)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # # recognize speech using Google Cloud Speech
    # GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{"type": "service_account",
    #       "project_id": "smartspeaker-1516075682745",
    #       "private_key_id": "d82b997de2986807c7447be758272454056c22c5",
    #       "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCvpysDPQyxcbDt\nTd5JIkPbdhBE7nkVHr7DI4iWeFzVxVEgfz63Erssi+mPELNIJnDKEHibK0I67wZe\n6eVGYG3/sAbz3ptTwSNuRSCFHj2WccP3afSYP0ki4KY4ot91+mY4FqR1RIdsSeFx\nYNexuoBlmldY/nkuvNQwy0B5GD4thdQbSl/aiGXkFfMnT/Uueo6LtaIncQcsKJeV\nDxaX3IUyMPwnI0kvi9P/qSNrRG1yQ/1N3cJOK8oA2SlcogezbEEGhWJu2VE7kaJq\nusFyHdk1k6KigPNndKmYQfqxoEGLubzhiFAEYfDckSpfbdOAZ8k14TFvhZv5qWNW\nlPJw/3GDAgMBAAECggEAUiCFGeSHdMfFg46u6d7df1T6UmB1uIxBgReyGzh3n3O8\ndMdJ2WsmnLNmJoAWcxuWDMQav+I/+zIa9nHBw1/+zlfNSGTClyxslng3tkXnYdob\nWCjwNecRGP+UeFKezJihBoR/rFy4PMdmYw52iyC6O8coI/IHUvTy+UVvBa9yEvIB\nnOtOBOf7Eh8bGLqJ0U45WvuyIkyPBwV8Kuhf50QJFatfufaMMT6Dd6nzMYO4wxjc\nKCbIbJNLxd6O+ukuMINzBIMV1Nd1raGdPFvm0siRSMR15/8Y9qZMJCFijxJd/sjo\nADl8WMzWzpOq8ZBgE+MKD4nfBNIlezD4D18TLIptUQKBgQDykKHX+xCmT7o9SBxG\n77nPH6crWlBGMO4fdu2uypp/JzC/QOp9FOuGpAG0bTQPeKg9o2WFK+CoFq5hazkd\nZ0cvvNVQr7eSxP4yQWdzLzQTFxYa4DVdYhyp0N6DnMJu18yEt4k5ReVbG0ESdOM5\nNW8HARj2R6M8umf+jxCxzJ2ubwKBgQC5Yce8SZ7hmS+JwuINWsYSiiyZElkRsJWo\nUfUi5YDYzBZdo1D9oanFMbPOzo1mH0phs8TPz82T09uSpTtS2UodkcDTX0cVoBqb\ngUoOQoRqffOXU/kzwb60DLfwyWaHJsK9AjMdvijGhGM2bvMwGrklxVVEku3/wpoT\nOC0xjpi4LQKBgHUVXymzpHvCrDD8Z7nN6TCTJMwGUg0vfSFu9JeUcDLEJgGLQiSS\nPoXFEJWYyLJXGU53Wn+HiG9aU13utaj9uxzN12GVD9UmhVSYwWiV9lron+DlLJ0g\nyJknmuCIgEmknLHLLc+Zb3Ykl6pjBXMN2cPVwcjPF3ouuBfl0rcf/1S9AoGACp2v\n23d30sF7+G6hlVQybZNeFHH5icrL9zSiThpIc6HUUg5tL+kXGMTM4DXx4Pw/vTKX\nPbNPuXxzYYV2zTrGRMU4/qHBJ1rgyzDvNbvXa2XFElBrv+wDaLolunM+HNU6Z6p9\nlOFz4lJogBCAequ9GI2hYWjsmi3htuILrH/W/Q0CgYEA0QC0KFZS95FghbnGDh6y\nYOdp2LwFWPV+YF9wiuQekgo9JoqcNQr8CVx2dNis5nbPtaCyauaGO1r6S8CaLDrp\ndJDNq9yl4fCHD4tx0SClEnjVd0FeJxo1/vA24go4YIc3ZjUU06N20Kvt1QoA35QN\nzR0qPRtwhZo0fVfqOPqQqvg=\n-----END PRIVATE KEY-----\n",
    #       "client_email": "starting-account-taca3qbo9sim@smartspeaker-1516075682745.iam.gserviceaccount.com",
    #       "client_id": "116241000196186236724",
    #       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    #       "token_uri": "https://accounts.google.com/o/oauth2/token",
    #       "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    #       "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/starting-account-taca3qbo9sim%40smartspeaker-1516075682745.iam.gserviceaccount.com"
    #     }"""
    # try:
    #     print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio,
    #                                                                             credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
    # except sr.UnknownValueError:
    #     print("Google Cloud Speech could not understand audio")
    # except sr.RequestError as e:
    #     print("Could not request results from Google Cloud Speech service; {0}".format(e))

    return audio_input

# if(audio_input == "play music"):
