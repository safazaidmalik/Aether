import speech_recognition as sr

def main():
    flag = 1

    while (flag):

        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)

            print("Please say something")

            audio = r.listen(source)

            print("Recognizing Now .... ")


            # recognize speech using google

            try:
                print("You have said \n" + r.recognize_google(audio))
                user_input = input("Press 1 if this is correct: ")
                if int(user_input) == 1:
                    flag = 0

            except Exception as e:
                print("Error :  " + str(e))

        # write audio
        with open("recorded.wav", "wb") as f:
            f.write(audio.get_wav_data())


if __name__ == "__main__":
    main()