## Content

* Introduction
* The model for task (Trump tweets NER)
* The model deployed as SageMaker multi-model endpoint
* Snowflake external function
* Analysis in Snowflake

## Introduction

Goals:
* Explore simple model to get ML model to production analytical environment
* Explore how to minimize the accidental complexity of deploying ML model to production
* Explore how Snowflake external functions can be used to invoke ML models
* Explore how to simply support multiple model
* Explore how to optimize development pipeline
* Explore the cost implications

in the process of researching the options several technologies cought my attentions. 

AWS CDK, released a year or so ago, is a library to define AWS resources in your favorite programming language.
This is definitely a positive evolution of infrastructure as code movement, as it gets us away from "death by yml" configuration and introduces a much better reuse model for templating infrastructure setup, which is lacking in CloudFormation's json/yml toolkit.
For the same of simplicity in this prototype I chose to stick with the AWS SAM tool, as the AWS CDK usage does not add anything to the point of this prototype and it can be added later on.
But I am very excited about the value AWS CDK brings to IoC and would like to explore that further.

Container image support for AWS Lambda - this is another significant development in the world of serverless computing.
Lambda evolution: from inflexible few runtimes, to more runtimes with layer support, to the full support of Docker container images.
Reminds me of the evolution Heroku made a few years back from supporting just rails apps, to more lang/framework support to custom buildpacks (i.e. containers).
Overall this simplifies development and deployment of serverless applications while leaning on the well known and used toolset of docker containerization. 
I predict that container image support for Lambda will pick up momentum and eventually replace the ziped code + layer packaging for the lambda functions.

Sagemaker Multi-Model endpoint. 
Package a model in a zip and Sagemaker will create a cluster/endpoint to invoke and auto-scale the model.
Alternatively, a model can be packaged as a docker image (the image must confirm to Sagemaker's container API spec (link)) and Sagemaker will provision a cluster and run inference with auto-scaling on demand.
The multi-model endpoint choice allows for combining of multiple models (packaged as zip or docker image) in the same endpoint/cluster. In usecases where the models are relatively small (i.e. one container can load and serve inference of multiple models) it is a good cost optimization choice.
This is an option to pursue if the model requires GPU support, as the lambda's runtime does not support GPU hardware yet.

Rephrase the use-case for multi-model endpoint:

> Businesses are increasingly developing per-user machine learning (ML) models instead of cohort or segment-based models. They train anywhere from hundreds to hundreds of thousands of custom models based on individual user data. For example, a music streaming service trains custom models based on each listener’s music history to personalize music recommendations. A taxi service trains custom models based on each city’s traffic patterns to predict rider wait times.

> While the benefit of building custom ML models for each use case is higher inference accuracy, the downside is that the cost of deploying models increases significantly, and it becomes difficult to manage so many models in production. These challenges become more pronounced when you don’t access all models at the same time but still need them to be available at all times. Amazon SageMaker multi-model endpoints addresses these pain points and gives businesses a scalable yet cost-effective solution to deploy multiple ML models.

> Source [AWS blog](https://aws.amazon.com/blogs/machine-learning/save-on-inference-costs-by-using-amazon-sagemaker-multi-model-endpoints/)


There are two ways MME can be deployed:
* Saving the models in S3 and allowing SageMaker to manage loading/unloading/inference on the models
* Creating a custom Docker container/image that is managed by SageMaker

## Overall architecture

### ML model repository

Where data scientists store model artifacts.

MLFlow, Sagemaker, S3, EFS, whatever.

### Inference service

Incoming HTTP requests -> ML results responses

Serverless Lambda

There will be multiple inference service lambdas if deployment is 1 lambda fn == 1 model, or 1 inference service function that dynamically load the right model.

Thought: Lambda functions - static models iteration at build time vs dynamic model retrieval from MLFlow?

Thought: combining SF HTTPS Proxy Service (API Gateway) with the inference plumbing? Cost and security implications?

This service does not need API Gateway resources, lambda functions have their own implicit invoke endpoint.

Immutability! invoking the same function with the same parameters should produce the same result. 
This principle guides us towards the models deployed during the build time, as oppose to dynamically querying model repository for artifacts.
Runtime dependency of "production grade" inference system on "development grade" model repository. Reliability requirements are different, if a model repository is down and unavailable that should not impact the production inference pipeline.
Data Scientists should be free to create new versions of the model without fear of breaking anything in production. Every new model instance will be additive and the old models should be available if the client still desires to use that version of the model.
That means will be many instances of the inference service serving many models with many versions.
What are the steps to deploy a new model artifact? Flipping status to "Production" in the model repository?
Or have to re-build/re-deploy the inference service? and/or have to re-define the external function?

### Snowflake Proxy Service 

API Gateway to receive calls from Snowflake and invoke the Inference Service. 
The proxy service must conform to Snowflake's external function proxy service specification and must be secured to only allow your Snowflake account to invoke it.

There is certain overhead in setting this up, so ideally we would want only one instance of this proxy service be deployed that can proxy requests to difference inference services.

### Snowflake API Integration

Only account admins can set this up, ideally set it up once and use for many external functions.

### Snowflake External Function

There will be multiple external functions, one per each deployed ML model. 
What's the best way to define it and manage input/output parameters, pass meta info to the proxy service to invoke the right inference service?

### Client program

This is the process that connects to Snowflake database and runs SQL queries, using defined external functions. 
This can be a Snowflake console web app, snowsql CLI, a python process, or (in our case [DBT](https://www.getdbt.com/) models).

## The Model

### The Task


## The Model Deployment


For this task I am using the custom Docker image approach. It is a more flexible of the two as there is a minimal dependency on the SageMaker, and any framework or library can be used.


At this point we have a deployed model accessible through an HTTP endpoint.

aws ecr create-repository --repository-name snowflake-ml-inference --image-tag-mutability IMMUTABLE --image-scanning-configuration scanOnPush=true
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:us-east-1:183626424367:repository/snowflake-ml-inference",
        "registryId": "183626424367",
        "repositoryName": "snowflake-ml-inference",
        "repositoryUri": "183626424367.dkr.ecr.us-east-1.amazonaws.com/snowflake-ml-inference",
        "createdAt": "2020-12-31T18:13:27-05:00",
        "imageTagMutability": "IMMUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": true
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 183626424367.dkr.ecr.us-east-1.amazonaws.com



## Snowflake external function

## Processing data and analysis


## Links

* https://www.thetrumparchive.com/

https://docs.aws.amazon.com/cdk/latest/guide/home.html - AWS CDK guide
https://cdkworkshop.com/ for initial setup and tutorial on AWS CDK

Using container image support for AWS Lambda with AWS SAM
https://aws.amazon.com/blogs/compute/using-container-image-support-for-aws-lambda-with-aws-sam/


## Thoughts


### Authentication of AWS CLI with MFA
https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/
```bash
eval "$(./login.sh ...2FA.code...)"
```

### SAM local memory issues

`Max Memory Used` always shows the same size as `Memory Size` - seems to be a problem running locally
https://github.com/aws/aws-sam-cli/issues/2464


