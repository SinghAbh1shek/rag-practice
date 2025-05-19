import speech_recognition as sr
from langgraph.checkpoint.mongodb import MongoDBSaver
from graph import create_chat_graph
import json


MONGODB_URI = 'mongodb+srv://hellykoptar:TuAurMai@cluster0.heyeysg.mongodb.net/'
config = {'configurable': {"thread_id": "1"}}


filename = "harvard.wav"

def speech_recognizer():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph = create_chat_graph(checkpointer=checkpointer)
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                r.pause_threshold = 2

                # print("Say something!")
                audio = r.listen(source)

                # sst = r.recognize_google(audio)
                # print("Processing audio...")
                # print("You Said:", sst)




                
                query = input(">>> ")

                    # for event in graph.stream({'messages': [{'role': 'user', 'content': query}]}, config, stream_mode='values'):
                        # event["messages"][-1].pretty_print()
                        # print(event)
                    

                ans = graph.invoke({'messages': [{'role': 'user', 'content': query}]}, config)
                # print(ans["messages"][-1].content)
                result = ans["messages"][-1].content
                print(result)
                return result


        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        
# speech_recognizer()