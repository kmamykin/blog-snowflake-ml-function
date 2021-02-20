import json
import psutil


def log_memory_usage(msg: str):
    print(f"{msg}:{psutil.virtual_memory()}")


log_memory_usage("Before import en_core_web_md")
import en_core_web_md
log_memory_usage("After import en_core_web_md")
nlp = en_core_web_md.load()  # Insufficient MemorySize for a lambda function crashes function execution right here!
log_memory_usage("After NLP model loaded")


def _doc_to_output(doc):
    return {
        "text": doc.text,
        "lang": doc.lang_,
        "lemmas": [token.lemma_ for token in doc if not token.is_stop],
        'entities': [{
            'text': ent.text,
            'start_char': ent.start_char,
            'end_char': ent.end_char,
            'label': ent.label_
        } for ent in doc.ents]
    }


def _process_inputs(texts):
    return [_doc_to_output(doc) for doc in nlp.pipe(texts, disable=[])]


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html

    context: object, required
        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    """
    try:
        log_memory_usage("Entered lambda_handler")
        payload = json.loads(event['body']) if event['body'] else []
        texts = payload if isinstance(payload, list) else [payload]
        responses = _process_inputs(texts)
        log_memory_usage("Documents processed")
        return {
            "statusCode": 200,
            "body": json.dumps(responses),
        }
    except Exception as err:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "errorMessage": f"{err}"
            }),
        }