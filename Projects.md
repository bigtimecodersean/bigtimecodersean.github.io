---
title: "Projects"
permalink: "/about/"
layout: page
---
Projects I've done 

# Smaller Projects

## [Transformer Explainer](https://gabby-foxtrot-8e2.notion.site/Transformers-1066353a15494d8f82b677e226e777e0)
Here are a series of brief explainers I made for myself on the Transformer architecture. Many images taken from Jay Alammar's "The Illustrated Transformer"

---------

# AI Coding Projects
## [Transformer-From-Scratch ](https://github.com/bigtimecodersean/Transformer_From_Scratch)

This project was inspired by Andrej Karpathy's work at: https://www.youtube.com/watch?v=kCc8FmEb1nY

We built a decoder-only Transformer from scratch, and training it on a corpus of Wikipedia data, to try and generate Wikipedia-style text. We will be training on: Wikitext - V2. Wikitext - V2 is a 2M word subset of the Wikipedia corpus.

The goal for the project was to:
- Define a decoder transformer architecture
- Train on the WikiText dataset
- Generate infinite Wikipedia-like text

(Due to model complexity, of course, the generated text does not resemble Wikipedia-style English)

## [Vision Transformer-From-Scratch](https://github.com/bigtimecodersean/Vision_Transformer_Replication)

I replicated a Vision Transformer, as developed in: https://arxiv.org/abs/2010.11929

... and applied it to a classifying food categories 

This project was part of Zero-to-Mastery's: Deep Learning with Pytorch

## [Fine-Tuning Stanford Cars Classifier](https://github.com/bigtimecodersean/Fine_Tuning_Stanford_Cars_Classification)
We are fine-tuning a few vision models (effnetb0 & GoogleNet) on the StanfordCars dataset to classify cars. We then deploy our top-performing model as a Gradio app to Hugging Face Spaces.

Dataset = StanfordCars (https://pytorch.org/vision/stable/generated/torchvision.datasets.StanfordCars.html#torchvision.datasets.StanfordCars)

# AI Research (non-coding) 

## [Numenta Active Dendrite](https://5744f6c2-4ed8-4ec0-a6a4-51909cc8f220.filesusr.com/ugd/e97160_d98a19334c954743adf683cb1df2b919.pdf)

Here is a written companion I wrote to a talk by Numenta's Subutai Ahmad Numenta titled: Active Dendrites Enable Flexible Context Integration 

Active dendrites are a more biologically realistic model of individual neurons, enabling better prediction, more flexible learning, and efficient, sparse representations in Artificial Neural Networks.  

# Basic Data Science Projects

## [Predicting Heart Disease](https://github.com/bigtimecodersean/Key_Indicators_of_Heart_Disease)

The aim of this project was to predict a patient's heart disease status (0 or 1), based on a variety of markers (personal and biological)

I used the Kaggle Heart Disease dataset, located: https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease

For our ML models, we will explore:
- Logistic Regression
- Support Vector Machines
- Random Forest Classifiers

## [Predicting Banking Subscription](https://github.com/bigtimecodersean/Banking_Subscription_Prediction)

The aim of this project is to see whether we can predict whether a client subscribed to a term deposit after a direct marking campaign from a Portugese bank.

The data is related with direct marketing campaigns of a Portuguese banking institution, based on phone calls (Moro, Cortez, and Rita 2014).

The goal of the campaigns were to get the clients to subscribe to a term deposit. There are 20 input variables and 1 binary output variable (y) that indicates whether the client subscribed to a term deposit with values ‘yes’,‘no’.

We try a few different classification methods, including:

- Logistic Regression
- Random Forests
- K-Nearest Neighbours
- Support Vector Machines
- Neural Networks



