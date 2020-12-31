## Content

* Introduction
* The model for task (Trump tweets NER)
* The model deployed as SageMaker multi-model endpoint
* Snowflake external function
* Analysis in Snowflake

## Introduction

## The Model

### The Task


## The Model Deployment

Rephrase the usecase for multi-model endpoint:

> Businesses are increasingly developing per-user machine learning (ML) models instead of cohort or segment-based models. They train anywhere from hundreds to hundreds of thousands of custom models based on individual user data. For example, a music streaming service trains custom models based on each listener’s music history to personalize music recommendations. A taxi service trains custom models based on each city’s traffic patterns to predict rider wait times.

> While the benefit of building custom ML models for each use case is higher inference accuracy, the downside is that the cost of deploying models increases significantly, and it becomes difficult to manage so many models in production. These challenges become more pronounced when you don’t access all models at the same time but still need them to be available at all times. Amazon SageMaker multi-model endpoints addresses these pain points and gives businesses a scalable yet cost-effective solution to deploy multiple ML models.

> Source [AWS blog](https://aws.amazon.com/blogs/machine-learning/save-on-inference-costs-by-using-amazon-sagemaker-multi-model-endpoints/)


There are two ways MME can be deployed:
* Saving the models in S3 and allowing SageMaker to manage loading/unloading/inference on the models
* Creating a custom Docker container/image that is managed by SageMaker

For this task I am using the custom Docker image approach. It is a more flexible of the two as there is a minimal dependency on the SageMaker, and any framework or library can be used.


At this point we have a deployed model accessible through an HTTP endpoint.

## Snowflake external function

## Processing data and analysis


## Links

* https://www.thetrumparchive.com/

