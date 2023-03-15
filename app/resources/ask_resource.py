import json
from datetime import datetime

from flask import request
from flask_restful import Resource

from app.service.record_service import get_records, get_statistical_record, get_statistical_value

import openai


class AskResource(Resource):

    def get(self):
        params = request.args

        natural_question = params.get('question')

        question_instructions = '''        
The topic of the conversation is weather records just from Peru, so remember all the regions, provinces and districts from Peru.
        
You are going to analyze a question in natural language and identify which function will answer it (there are 3), 
then you have to identify which parameters the question provides, and output the result according to the following 
vocabulary. 

question:

function 1:
{
    name: get_weather_record, 
    parameters: {
        date[mandatory]: %Y-%m-%d,
        station_name[mandatory]: ,
    }
}

function 2:
{
    name: get_statistical_record, 
    parameters: {
        start_date[optional]: %Y-%m-%d,
        end_date[optional]: %Y-%m-%d,
        stat_type[mandatory]: (min, max)
        parameter[mandatory]: (max_temp, min_temp precipitation),
        region[optional]: ,
        province[optional]: ,
        district[optional]: 
    }
}

function 3:
{
    name: get_statistical_value, 
    parameters: {
        start_date[optional]: %Y-%m-%d,
        end_date[optional]: %Y-%m-%d,
        stat_type[mandatory]: (average, standard_deviation)
        parameter[mandatory]: (max_temp, min_temp, precipitation),
        region[optional]: ,
        province[optional]: ,
        district[optional]: 
    }
}

error:

{
    error[mandatory]: ,
}

Notice that in the above vocabulary each function has a name an its corresponding parameters, this parameters can be mandatory or optional (specified between '[]'), if the question does not provide a value for a mandatory parameter output an error, and for an optional parameter you can set it to null, also notice that some parameters can have only take some values which are specified between '()'.

Notice also that station names does not include the word station, e.g ...in Miraflores station (station_name='Miraflores')

Also be careful and don't confuse cities from other countries with the regions, provinces, and districts from Peru. 

Finally if you receive an off-topic question, output an error.
       
Rules: 

    - NEVER answer in natural language, just in JSON; if you can't do it, output an error in JSON explaining why.
    - All messages should start with '{' and end with '}'
'''

        answer_instructions = '''
You are going to analyze a question formulated in natural language, then which function was executed to answer it, then 
with the given result you will elaborate a proper answer for the natural question, adding extra useful information. 

Take into account that if a result is the null then there is not enough data to answer the question.

Additionally you could receive an error instead of a function and result, and you will have to inform it.

The topic will be weather records from Peru, so remember all the regions, provinces and districts 
from Peru. 

Just show the natural language answer, don't explain it.
'''

        completion_question = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': "system", 'content': question_instructions},
                {'role': "user", 'content': natural_question}
            ]
        )

        print(completion_question.choices[0].message.content)

        json_question: dict = json.loads(completion_question.choices[0].message.content)

        error = json_question.get('error')

        if error is not None:

            json_answer = {
                'natural_question': natural_question,
                'error': error
            }

            completion_answer = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {'role': "system", 'content': answer_instructions},
                    {'role': "user", 'content': json.dumps(json_answer)}
                ]
            )

            return {'answer': completion_answer.choices[0].message.content, 'error': error}, 200

        function_name: str = json_question['name']
        function_parameters: dict = json_question['parameters']

        result = execute_function_from_question(function_name, function_parameters)

        json_answer = {
            'natural_question': natural_question,
            'executed_function': json_question,
            'result': result
        }

        completion_answer = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': "system", 'content': answer_instructions},
                {'role': "user", 'content': json.dumps(json_answer)}
            ]
        )

        return {'answer': completion_answer.choices[0].message.content, 'function_result': result}, 200


def execute_function_from_question(function_name: str, function_parameters: dict):

    if function_name == 'get_weather_record':

        date = function_parameters['date']
        station_name = function_parameters['station_name']

        records = get_records(
            start_date=datetime.strptime(date, '%Y-%m-%d') if date is not None else None,
            end_date=datetime.strptime(date, '%Y-%m-%d') if date is not None else None,
            station_name=station_name
        )

        return records[0].to_dict()
    elif function_name == 'get_statistical_record':

        start_date = function_parameters['start_date']
        end_date = function_parameters['end_date']
        stat_type = function_parameters['stat_type']
        parameter = function_parameters['parameter']
        region = function_parameters['region']
        province = function_parameters['province']
        district = function_parameters['district']

        record, error = get_statistical_record(
            start_date=datetime.strptime(start_date, '%Y-%m-%d') if start_date is not None else None,
            end_date=datetime.strptime(end_date, '%Y-%m-%d') if end_date is not None else None,
            stat_type=stat_type,
            parameter=parameter,
            region=region,
            province=province,
            district=district
        )

        return record.to_dict()

    elif function_name == 'get_statistical_value':

        start_date = function_parameters['start_date']
        end_date = function_parameters['end_date']
        stat_type = function_parameters['stat_type']
        parameter = function_parameters['parameter']
        region = function_parameters['region']
        province = function_parameters['province']
        district = function_parameters['district']

        value, error = get_statistical_value(
            start_date=datetime.strptime(start_date, '%Y-%m-%d') if start_date is not None else None,
            end_date=datetime.strptime(end_date, '%Y-%m-%d') if end_date is not None else None,
            stat_type=stat_type,
            parameter=parameter,
            region=region,
            province=province,
            district=district
        )

        return value