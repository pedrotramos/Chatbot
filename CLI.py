import re
import os
import pickle
import random
import pandas as pd
from textblob import TextBlob
from spellchecker import SpellChecker
from termcolor import colored
from selenium import webdriver
from chromedriver_py import binary_path


def loadModels():
    modelTypes = ["main", "clima", "conta", "eletro"]
    models = {}
    vectorizers = {}
    files = os.listdir("./models")
    for modelType in modelTypes:
        finalNumber = 0
        if modelType == "main":
            filename = f"model_v{finalNumber}.sav"
            pattern = r"model_v\d+.sav"
            pattern2 = r"model_v(\d)+.sav"
        else:
            filename = f"model_{modelType}_v{finalNumber}.sav"
            pattern = fr"model_{modelType}_v\d+.sav"
            pattern2 = fr"model_{modelType}_v(\d)+.sav"
        for f in files:
            if re.fullmatch(pattern, f):
                current = int(re.sub(pattern2, r"\1", filename))
                possible = int(re.sub(pattern2, r"\1", f))
                if possible > current:
                    filename = f
                    finalNumber = possible
        if modelType == "main":
            model = pickle.load(open(f"models/model_v{finalNumber}.sav", "rb"))
            vectorizer = pickle.load(
                open(f"vectorizers/vectorizer_v{finalNumber}.sav", "rb")
            )
        else:
            model = pickle.load(
                open(f"models/model_{modelType}_v{finalNumber}.sav", "rb")
            )
            vectorizer = pickle.load(
                open(f"vectorizers/vectorizer_{modelType}_v{finalNumber}.sav", "rb")
            )
        models[modelType] = model
        vectorizers[modelType] = vectorizer
    return models, vectorizers


def greetUser():
    print("")
    print(
        colored(text="Olá, eu sou o Foxbot. Como posso te ajudar?", color="yellow"),
    )
    print("Para sair basta digitar 'sair' no campo de pergunta.")
    print("")


def askForInput():
    print(
        "Digite abaixo o que você gostaria de saber:",
    )
    sentence = input()
    return sentence


def predNewSentence(txt, models, vectorizers):
    output_text = ""
    predModel = models["main"]
    vectorizer = vectorizers["main"]
    txt = txt.replace("$", "dinheiro")
    try:
        if TextBlob(txt).detect_language() == "pt":
            sentence = ""
            spellCheck = SpellChecker(language="pt")
            for word in txt.split():
                if word.lower().startswith("foxbot") and len(word) <= len("foxbot") + 1:
                    sentence += word + " "
                else:
                    if word[-1] in ["?", ".", "!", ",", ":", ";"]:
                        sentence += spellCheck.correction(word) + word[-1] + " "
                    else:
                        sentence += spellCheck.correction(word) + " "
            if sentence[:-1] != txt:
                while True:
                    print("")
                    response = input(f"Você quis dizer: '{sentence[:-1]}'? [S/N] ")
                    if response.lower() == "s":
                        text = re.sub(r"\s\-\s|\-\-+", " ", sentence.lower())
                        text = re.sub(r"[^\w\s\-]", " ", text)
                        text = re.sub(r"foxbot ", "", text)
                        output_text = sentence[:-1]
                        break
                    elif response.lower() == "n":
                        text = re.sub(r"\s\-\s|\-\-+", " ", txt.lower())
                        text = re.sub(r"[^\w\s\-]", " ", text)
                        text = re.sub(r"foxbot ", "", text)
                        output_text = txt
                        break
            else:
                text = re.sub(r"\s\-\s|\-\-+", " ", sentence.lower())
                text = re.sub(r"[^\w\s\-]", " ", text)
                text = re.sub(r"foxbot ", "", text)
                output_text = sentence
            counts = vectorizer.transform([text])
            print("")
            return predModel.predict(counts)[0], output_text
        else:
            text = re.sub(r"\s\-\s|\-\-+", " ", txt.lower())
            text = re.sub(r"[^\w\s\-]", " ", text)
            text = re.sub(r"foxbot ", "", text)
            output_text = txt
            counts = vectorizer.transform([text])
            print("")
            return predModel.predict(counts)[0], output_text
    except:
        text = re.sub(r"\s\-\s|\-\-+", " ", txt.lower())
        text = re.sub(r"[^\w\s\-]", " ", text)
        text = re.sub(r"foxbot ", "", text)
        output_text = txt
        counts = vectorizer.transform([text])
        print("")
        return predModel.predict(counts)[0], output_text


def predSubClass(txt, prediction, models, vectorizers):
    if prediction == "Interagir com a luz ou o ar-condicionado":
        model = models["eletro"]
        vectorizer = vectorizers["eletro"]
    elif prediction == "Consultar saldo da conta":
        model = models["conta"]
        vectorizer = vectorizers["conta"]
    elif prediction == "Obter informações relativas ao clima":
        model = models["clima"]
        vectorizer = vectorizers["clima"]
    else:
        raise ValueError(
            "Algo deu errado! Impossível definir subclasse para essa intenção."
        )
    counts = vectorizer.transform([txt])
    return model.predict(counts)[0]


def getTemperature():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(executable_path=binary_path, options=options)
    try:
        browser.get("https://www.google.com/search?q=weather")
        loc_html = browser.find_element_by_css_selector("#wob_loc")
        print(f"Localização: {loc_html.text}")
        temp_html = browser.find_element_by_css_selector("#wob_tm")
        scale_html = browser.find_element_by_css_selector(
            "#wob_wc > div.UQt4rd > div.Ab33Nc > div > div.vk_bk.wob-unit > span"
        )
        print(f"Temperatura: {temp_html.text}{scale_html.text}")
        print("")
    except:
        raise ValueError("Erro ao buscar informações sobre a temperatura.")
    finally:
        browser.quit()


def getRain():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(executable_path=binary_path, options=options)
    try:
        browser.get("https://www.google.com/search?q=weather")
        loc_html = browser.find_element_by_css_selector("#wob_loc")
        print(f"Localização: {loc_html.text}")
        rain_html = browser.find_element_by_css_selector(
            "#wob_wc > div.UQt4rd > div.wtsRwe > div:nth-child(1)"
        )
        print(f"Probabilidade de chuva: {rain_html.text.split()[-1]}")
        print("")
    except:
        raise ValueError("Erro ao buscar informações sobre a probabilidade de chuva.")
    finally:
        browser.quit()


def answerUserInput(prediction):
    if prediction == "Luz":
        print("Ok! Vou alterar o estado da luz.")
        print("")
    elif prediction == "Ar-condicionado":
        print("Ok! Interagindo com o ar-condicionado.")
        print("")
    elif prediction == "Consultar saldo da conta-corrente":
        valor = random.uniform(0, 1_000_000)
        print(f"O saldo da sua conta-corrente é: R$ {valor:,.2f}")
        print("")
    elif prediction == "Consultar saldo da poupança":
        valor = random.uniform(0, 1_000_000)
        print(f"O saldo da sua conta-poupança é: R$ {valor:,.2f}")
        print("")
    elif prediction == "Temperatura":
        getTemperature()
    elif prediction == "Chuva":
        getRain()
    else:
        raise ValueError("O programa não é capaz de responder a essa intenção")


def findOutRealIntention(pred):
    possibleIntentions = [
        "Interagir com a luz ou o ar-condicionado",
        "Consultar saldo da conta",
        "Obter informações relativas ao clima",
        "Nenhuma das opções acima",
    ]
    if pred == "Não sei":
        resp = "n"
        print("Acho que não sei responder a sua pergunta")
    else:
        answerUserInput(pred)
        resp = input(f"Você está satisfeito com o resultado mostrado? [S/N] ")
    print("")
    while True:
        if resp.lower() == "s":
            print(
                colored(text="Obrigado por ajudar a melhorar o Foxbot!", color="green"),
            )
            print("")
            return pred
        elif resp.lower() == "n":
            while True:
                print(
                    "Qual das opções abaixo descreve sua intenção com a pergunta anterior?"
                )
                print("")
                j = 1
                for i in range(len(possibleIntentions)):
                    if possibleIntentions[i] != pred:
                        print(f"{j}) {possibleIntentions[i]}")
                        j += 1
                print("")
                intentionNumber = int(
                    input(
                        "Digite o número correspondente à descrição da sua intenção: "
                    )
                )
                print("")
                if intentionNumber in range(1, j - 1):
                    print(
                        colored(
                            text="Obrigado por ajudar a melhorar o Foxbot!",
                            color="green",
                        ),
                    )
                    print("")
                    return possibleIntentions[intentionNumber - 1]
                elif intentionNumber == j - 1:
                    print(
                        colored(
                            text="Obrigado por ajudar a melhorar o Foxbot!",
                            color="green",
                        )
                    )
                    print("")
                    return "Não sei"
                else:
                    print(
                        colored(
                            text="Opção inválida! Selecione um número correspondente a uma das alternativas.",
                            color="red",
                        )
                    )
                    print("")
        else:
            print("")
            resp = input(f"Não entendi! Você gostaria de {pred.lower()}? [S/N] ")
            print("")


def finalizeInteraction(df):
    data = pd.read_excel("new_sentences/newSentences.xlsx", index_col=0)
    data = data.append(df, ignore_index=True)
    data.to_excel("new_sentences/newSentences.xlsx")
    print("")
    print(
        colored(text="Até logo! Espero ter ajudado!", color="yellow"),
    )


if __name__ == "__main__":

    models, vectorizers = loadModels()
    greetUser()
    sentence = askForInput()
    new_data = pd.DataFrame(columns=["Sentença", "Intenção"])
    while sentence.lower() != "sair":
        prediction, sentence = predNewSentence(sentence, models, vectorizers)
        if prediction != "Não sei":
            prediction = predSubClass(sentence, prediction, models, vectorizers)
        realIntention = findOutRealIntention(prediction)
        new_data = new_data.append(
            dict(zip(new_data.columns, [sentence, realIntention])),
            ignore_index=True,
        )
        sentence = askForInput()
    finalizeInteraction(new_data)