# Chatbot Insper: FoxBot

## Projeto 2 de Processamento de Linguagem Natural

Pedro Ramos e Thiago Verardo

### Objetivo:

Criar um chatbot capaz de se comunicar através de uma conversação em linguagem natural com o usuário, com o intuito de interpretar e responder perguntas a respeito do clima, conta bancária e interagir com dispositivos IoT da casa.

### Implementação:

#### Dados:

Primeiramente, um dataset com frases e suas devidas intenções foi desenvolvido coletivamente para que mais dados fossem adicionados, deixando o modelo mais rico.

#### Intenções:
* Clima: Obter informações relativas ao clima
* Conta Bancária: Consultar saldo da conta
* Interagir com dispositivos IoT: Interagir com a luz ou o ar-condicionado

#### Limpeza:

Com o dataset em mãos, o mesmo foi limpo através da tokenização e normalização de texto no arquivo ```baseModel.ipynb```. A limpeza é essencial para que os dados cheguem lapidados para o bot interpretar.

#### Separação dos dados em treinamento e teste:

Para um modelo probabilístico ser criado, é necessária a divisão do dataset original em teste e treinamento. No dataset de treinamento o bot entende o padrão e a resposta esperada e no de teste ele testa se seu entendimento é bom ou não, isso depende da probabilidade encontradada na frase analisada de ser a respeito de uma das intenções.

Caso a probabilidade de ser uma Intenção seja muito baixa, o bot responde o usuário com "Não sei".

#### Novas intenções:

No arquivo ```baseSubModels.ipynb```, foram criados novas subdivisões no classificador de palavras. Para cada intenção anterior, duas intenções substituiram a mesma com o intuito de deixar o bot mais completo.

* Clima: Temperatura e Chuva
* Conta Bancária: Consultar saldo da poupança e Consultar saldo da conta-corrente
* Interagir com dispositivos IoT: Ar-condicionado e Luz

E da mesma maneira, foram separados em treinamento e teste para, enfim, serem analisadas e preditas pelo bot.

#### Integração com o usuário:

Para o usuário conseguir interagir de maneira simples com o bot, um cliente foi implementado no arquivo ```CLI.py```, que ao ser rodado já inicia uma conversação com o usuário. Ele aguarda uma resposta e, ao recebela, interpreta e devolve o resultado esperado.

#### Realimentação da base de dados (aprendizado "online"):

A realimentação da base de dados é boa para manter o modelo sempre melhor e com mais opções para prever um resultado. Como o projeto não entrará em circulação e as respostas ao bot serão sempre cofiáveis, implementamos no cliente a opção de dizer se a resposta dada pelo bot foi válida ou não, caso tenha sido a pergunta e a intenção são mandadas para um dataset que, no arquivo ```retraining.ipynb``` realimenta a base de dados inicial com os dados novos.

#### Extra:

Ao perguntar seu saldo ao FoxBot, o usuário recebe um dado fictício gerado por ele para a experiência ficar melhor, sem contar com os dados do clima do local em que o usuário está de acordo como google.

#### Para rodar o chatbot:

```
$ pthon CLI.py
```
