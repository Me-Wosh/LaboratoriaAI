# -*- coding: utf-8 -*-
"""klasyfikacja.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TE-fGpaSWgryAVIS21_NMyCnk14VBN71
"""

# import bibliotek
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

# wczytanie danych z pliku .csv
csv = pd.read_csv("iris.data")

# csv.columns = ["kolumna1", "kolumna2"] - nadanie nazw kolumn jeśli nie ma

# normalizacja cech w celu łatwiejszej ich interpretacji, skalaryzacja MinMax - czyli cechy przyjmują wartości od 0 do 1
features = csv[["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

# zamiana tekstowych etykiet klas na odpowiedniki liczbowe
classes = csv[["Species"]].replace(["Iris-setosa", "Iris-versicolor", "Iris-virginica"], [0, 1, 2])

# połączenie znormalizowanych cech i zmienionych etykiet klas w jedną całość
csv = pd.concat([features, classes], axis = 1)

# podział na zbiór treningowy i testowy
train, test = train_test_split(csv, test_size = 0.3) # podział danych na 70% danych treningowych i 30% testowych
X_train = train[["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]]
y_train = train.Species
X_test = test[["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]]
y_test = test.Species

# redukcja wymiarowości za pomocą PCA
# algorytm PCA przekształca otrzymane dane tworząc nowe wymiary nazywane principal
# components, które są połączeniem pierwotnych cech ze zbioru danych. Nowo otrzymane
# wymiary są dobrane tak, żeby uzyskać największą wariancję
pca = PCA(n_components = 2)  # redukcja do 2 głównych składowych
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

# wizualizacja danych po PCA
for i in range(len(y_train)):
  plt.scatter(X_train_pca[y_train == i, 0], X_train_pca[y_train == i, 1], edgecolor = "black")

plt.title("Dane po redukcji PCA")
plt.xlabel("Główna składowa 1")
plt.ylabel("Główna składowa 2")
plt.legend(["Iris-setosa", "Iris-versicolor", "Iris-virginica"])
plt.grid()
plt.show()

# pierwszy klasyfikator
sgd = MLPClassifier(hidden_layer_sizes = (4, ), # liczba neuronów na warstwę
                    solver = "sgd", # Stochastic Gradient Descent
                    learning_rate_init = 0.01,
                    max_iter = 10000, # maksymalna ilość iteracji, po której algorytm kończy działanie
                    random_state = 0, # seed
                    tol = 0.0001, # tolerancja - jeżeli następuje postęp mniejszy niż tol algorytm kończy działanie
                    verbose = True) # wyświetlanie na bieżąco przebiegu działania algorytmu

# uruchomienie klasyfikatora
sgd.fit(X_train_pca, y_train)

# predykacja na zbiorze testowym
test_prediction = sgd.predict(X_test_pca)

print(f"Dokładność Multi-layer Perceptronu dla zbioru testowego: {accuracy_score(test_prediction, y_test)}")

# wykres krzywej straty
plt.title("krzywa straty")
plt.plot(sgd.loss_curve_)
plt.xlabel("iteracja")
plt.ylabel("strata")
plt.grid()
plt.show()



# drugi klasyfikator
sequential = Sequential() # model sekwencyjny - kolejne warstwy przypominają stos
# dodanie warstw gęstych - czyli takich, gdzie wszystkie neurony z warstwy
# poprzedniej są połączone ze wszystkimi pojedynczymi neuronami z warstwy następnej
sequential.add(Dense(32, # warstwa z 32 neuronami
                     input_dim = 4, # rozmiar danych wejściowych (4)
                     activation = "relu")) # jedna z najpopularniejszych funkcji aktywacji
sequential.add(BatchNormalization()) # normalizacja danych
sequential.add(Dense(32, activation = "relu")) # kolejna warstwa
sequential.add(BatchNormalization()) # ponowna normalizacja
sequential.add(Dropout(0.2)) # wskaźnik dropout zapobiegający przeuczeniu
# warstwa wyjściowa, aktywacja liniowa oznacza, że nie dokonano żadnej
# transformacji danych wyjściowych; stosuje się ją w celu predykcji rzeczywistej
# wartości
sequential.add(Dense(1, activation = "linear"))

# kompilacja modelu
sequential.compile(loss = "mse", # funkcja straty mse - średni kwadrat różnic między przewidywaną i rzeczywistą wartością
                   optimizer = "adam", # jeden z najpopularniejszy algorytmów optymalizacji
                   metrics = ["mae", "accuracy"]) # interesujące nas metryki

# trenowanie modelu
fit = sequential.fit(X_train, y_train, # dane treningowe
                     batch_size = 16, # ustawienie rozmiaru próbkowania celem mniejszego obciążenia sprzętu
                     epochs = 200, # maksymalna liczba epok
                     verbose = 1, # wyświetlanie postępu treningu
                     validation_data = (X_test, y_test)) # zbiór walidacyjny

# sprawdzenie, jak model poradził sobie ze zbiorem testowym
metrics = sequential.evaluate(X_test, y_test)
print(f"Dokładność modelu sekwencyjnego dla zbioru testowego: {metrics[2]}")

history = fit.history
figure = plt.figure(figsize = (10, 4))
# wykres funkcji straty
subplot = figure.add_subplot(1, 2, 1)
subplot.plot(range(1, len(history["loss"]) + 1), history["loss"])
subplot.plot(range(1, len(history["val_loss"]) + 1), history["val_loss"])
subplot.set_title("Funkcja straty uczenia MSE")
subplot.set_xlabel("Epoka")
subplot.set_ylabel("Loss")
plt.legend(["Loss", "Validation Loss"])
subplot.tick_params(axis = "both", which = "major")
# wykres Mean Absolute Error, czyli średniej różnicy między przewidywaną i rzeczywistą wartością
subplot = figure.add_subplot(1, 2, 2)
subplot.plot(range(1, len(history["mae"]) + 1), history["mae"])
subplot.plot(range(1, len(history["val_mae"]) + 1), history["val_mae"])
subplot.set_title("Mean Absolute Error")
subplot.set_xlabel("Epoka")
subplot.set_ylabel("Mean Absolute Error")
plt.legend(["Mean Absolute Error", "Validation Mean Absolute Error"])
subplot.tick_params(axis = "both", which = "major")
plt.show()


# wnioski

# krzywa straty przedstawia zmniejszanie się funkcji straty w kolejnych iteracjach,
# jej zbieżność świadczy o skuteczności uczenia się modelu - jeżeli krzywa
# stabilizuje się lub osiąga minimalny poziom, oznacza to, że model nie poprawia
# już swoich wyników.

# pierwszy model działa poprawnie, co pokazuje wysoki poziom dokładności (powyżej
# 90%) na zbiorze testowym, a krzywa straty wskazuje na skuteczność uczenia. Dokładność
# nie jest równa 100%, a więc istnieje przestrzeń do dalszej optymalizacji w celu
# poprawy wyników.

# krzywa straty w drugim modelu zaczęła stabilizować się już po około 100 iteracjach,
# zamiast 700 jak w przypadku modelu pierwszego, natomiast model pierwszy osiągnął
# lepszą dokładność