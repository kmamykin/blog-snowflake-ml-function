FROM public.ecr.aws/lambda/python:3.8

RUN python3.8 -m pip install --upgrade pip && \
    python3.8 -m pip install spacy && \
    python3.8 -m spacy download en_core_web_md

COPY app.py ./

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
