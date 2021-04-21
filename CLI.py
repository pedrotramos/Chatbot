import re
import os
import pickle
import pandas as pd
from textblob import TextBlob
from spellchecker import SpellChecker
from termcolor import colored


def loadModel():
    finalNumber = 0
    filename = f"model_v{finalNumber}.sav"
    files = [f for f in os.listdir("./models") if os.path.isfile(f)]
    for f in files:
        if re.fullmatch(r"model_v\d+.sav", f):
            current = int(re.sub(r"model_v(\d+).sav", r"\1", filename))
            possible = int(re.sub(r"model_v(\d+).sav", r"\1", f))
            if possible > current:
                filename = f
                finalNumber = possible
    model = pickle.load(open(f"models/model_v{finalNumber}.sav", "rb"))
    vectorizer = pickle.load(open(f"vectorizers/vectorizer_v{finalNumber}.sav", "rb"))

    return model, vectorizer


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


def predNewSentence(txt, predModel, vectorizer):
    output_text = ""
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
        resp = input(f"Você gostaria de {pred.lower()}? [S/N] ")
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

    model, vectorizer = loadModel()
    greetUser()
    sentence = askForInput()
    new_data = pd.DataFrame(columns=["Sentença", "Intenção"])
    while sentence.lower() != "sair":
        prediction, sentence = predNewSentence(sentence, model, vectorizer)
        if prediction != None:
            realIntention = findOutRealIntention(prediction)
            new_data = new_data.append(
                dict(zip(new_data.columns, [sentence, realIntention])),
                ignore_index=True,
            )
        sentence = askForInput()
    finalizeInteraction(new_data)