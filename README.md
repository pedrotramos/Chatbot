# Foxbot: A Simple Chatbot With MultinomialNB

### Objective:

This project aims to implement a simple chatbot capable of communicating with the user in portuguese to interpret and answer questions regarding three different intention classes.

### Intention Classes:
- Weather: Obtain weather information
- Bank Account: Check the account's balance
- Interact with IoT devices: Interact with an IoT device

### Dataset:

First of all, the chatbot must be able to identify if a sentence falls into any of the categories above. If it does, then the chatbot must be able to accurately classify the sentence among the three possible intention classes. In case it doesn't, the chatbot must simply answer that it doesn't know how to respond to such request. To do so, with the help of a group of friends and colleagues, a labeled dataset with different sentences was created. The dataset contains more than 100 different examples for each of the possible intentions outlined above, along with more than 100 examples of phrases that do not fit into any of the intention classes expected by the chatbot.

### Cleaning the Dataset:

It's also very important to clean the dataset before training begins. Therefore, the punctuation was removed, every word was converted to lowercase and every occurrence of the word "foxbot" was also removed to avoid any possible bias caused by the chatbot's name. Once all of this was done, the base model was trained.

### Intention Subclasses:

The next step was to implement the concept of subclasses. Once the chatbot identified that a specific sentnece refers to the weather category, for example, it must be able to identify whether the user expects to obtain information related to temperature or related to rain. The subclasses considered in this project were:

- Weather: Temperature or Rain
- Bank Account: Check the Savings Account balance or the Current Account balance
- Interact with IoT devices: Interact with the light or the air-conditioner

The chatbot also needed to learn to classify a sentence into one of the subclasses of the class it predicted for that specific sentence. In order to train the chatbot to do that, three new labeled datasets were created.

### User Interface:

In order for someone to use our chatbot, a simple UI was developed. It's only a CLI, but it enables the user to interact with foxbot, and it asks the user for feedback in order to acquire new data and further develop the classification models.

#### Using Foxbot:

```
python CLI.py
```

**Disclaimer:** The bank account data provided by the chatbot is fake and Foxbot isn't actually able to interact with IoT devices, but the weather information is real and obtained from Google using [Selenium](https://selenium-python.readthedocs.io/).
