# Classificando buscas utilizando biblioteca de analise de dados Pandas.

from collections import Counter
import pandas as pd
from sklearn.model_selection import cross_val_score
import numpy as np

df = pd.read_csv ("situacao_do_cliente.csv")

X_df = df [["recencia", "frequencia", "semanas_de_inscricao"]]
Y_df = df ["situacao"]

X_dummies = pd.get_dummies(X_df)
Y_dummies = Y_df

X = X_dummies.values
Y = Y_dummies.values

porcentagem_treino = 0.8

tamanho_treino = int (len (Y) * porcentagem_treino)

treino_dados = X[:tamanho_treino]
treino_marcacoes = Y[:tamanho_treino]

validacao_dados = X[tamanho_treino:]
validacao_marcacoes = Y[tamanho_treino:]

def fit_and_predict (nome ,modelo,treino_dados, treino_marcacoes):

	k = 10
	score = cross_val_score (modelo, treino_dados, treino_marcacoes, cv = k)
	taxa_acertos = np.mean (score)

	msg = "Taxa de acerto do algoritmo {0}: {1}".format(nome, taxa_acertos)
	print(msg)

	return taxa_acertos

resultado = {}

from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
modelo_OneVsRest = OneVsRestClassifier (LinearSVC (random_state = 0))
Resultado_OneVSRest = fit_and_predict ("OneVsRest", modelo_OneVsRest, treino_dados, treino_marcacoes)
resultado [Resultado_OneVSRest] = modelo_OneVsRest

from sklearn.multiclass import OneVsOneClassifier
modelo_OneVsOne = OneVsOneClassifier (LinearSVC (random_state = 0))
Resultado_OneVSOne = fit_and_predict ("OneVsOne", modelo_OneVsOne, treino_dados, treino_marcacoes)
resultado [Resultado_OneVSOne] = modelo_OneVsOne

from sklearn.naive_bayes import MultinomialNB
modelo_Multinomial = MultinomialNB ()
Resultado_Multinomial = fit_and_predict ("MultinomialNB", modelo_Multinomial, treino_dados, treino_marcacoes)
resultado [Resultado_Multinomial] = modelo_Multinomial

from sklearn.ensemble import AdaBoostClassifier
modelo_AdaBoost = AdaBoostClassifier ()
Resultado_AdaBoost = fit_and_predict ("AdaBoostClassifier", modelo_AdaBoost, treino_dados, treino_marcacoes)
resultado [Resultado_AdaBoost] = modelo_AdaBoost


# Teste do algoritimo base:
acertos_base = (Counter(validacao_marcacoes).itervalues())
taxa_de_acerto_base = 100.0 * max(acertos_base)/ len (validacao_marcacoes)
print ("A porcentagem do Algoritimo base no Mundo Real: %f" % (taxa_de_acerto_base)) 


maximo = max (resultado)
vencedor = resultado [maximo]

vencedor.fit (treino_dados, treino_marcacoes)
resultado = vencedor.predict(validacao_dados)

acertos = (resultado == validacao_marcacoes)

total_acertos = sum (acertos)
total_elementos = len (validacao_dados)
taxa_acertos = 100.0 * total_acertos / total_elementos

print ("Taxa de acerto do algoritmo Vencedor no mundo real: %f " % (taxa_acertos))
print ("Numero de dados da validacao: %d" % (total_elementos))





