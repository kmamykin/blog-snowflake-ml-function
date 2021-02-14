import json
from pathlib import Path
import en_core_web_md

nlp = en_core_web_md.load()


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

    def doc_to_ner(doc):
        result = {
            'entities': [{'text': ent.text, 'start_char': ent.start_char, 'end_char': ent.end_char, 'label': ent.label_}
                         for ent in doc.ents]
        }
        return result

    # Need to handle isBase64Encoded ?
    body = json.loads(event['body'])
    # Assume the body structure as an array of strings to run NER on
    texts = body
    docs = [doc for doc in nlp.pipe(texts, disable=["tagger", "parser"])]
    return {
        "statusCode": 200,
        "body": json.dumps(
            # [doc_to_ner(doc) for doc in docs]
            "Works"
        ),
    }
