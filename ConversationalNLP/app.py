from flask import Flask
from ConversationalService import OpenNLP
app = Flask(__name__)
from flask import Flask, request
import json


@app.route('/')
def hello_world():
    return 'Hello World!'



@app.route('/ConversationalService',methods=["POST","GET"])
def ConversationalService():
    jsonreturn = ""
    if request.method == 'POST':
        #data=json.load(request.data)
        #type(data)
        data=request.get_json()
        query=data['Query']
        intent_detected, score, entity, negation, sentiment,sentimentscore=OpenNLP.NLPcall(query)
        jsondata = {
            'response': {
                "Utterance":query,
                "Intent": intent_detected,
                "Score": score,
                "Entity": entity,
                "Negation": negation,
                "Sentiment": str(sentiment),
                "Sentimentscore":str(sentimentscore)
            }
        }

        jsonreturn = json.dumps(jsondata)
        print(jsondata)
        return jsonreturn
    return 'ConversationalService'

if __name__ == '__main__':

    app.run(debug=True)
