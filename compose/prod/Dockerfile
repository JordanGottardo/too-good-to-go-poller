FROM public.ecr.aws/lambda/python:3.9

COPY requirements/prod.txt ${LAMBDA_TASK_ROOT}

RUN python3 -m ensurepip
RUN pip install -r prod.txt

ADD src ${LAMBDA_TASK_ROOT}

CMD ["main.handler"]