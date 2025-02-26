# -*- coding: utf-8 -*-
"""klasteryzacja.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10IejNiyj8h8z4S7gjolAUfebWn_f1eUo
"""

# import bibliotek
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# utworzenie skupisk blobów
# X: lista blobów, gdzie blob jest zapisany jako [cecha1, cecha2]
# y: lista przynależności blobów do skupisk
X, y = make_blobs(n_samples = 1000, # liczba blobów
                  n_features = 2, # liczba cech blobów
                  centers = 5, # liczba skupisk
                  cluster_std = 0.8, # współczynnik oddalenia blobów od skupiska
                  random_state = 0) # seed

# obliczenie za pomocą metody łokciowej optymalnej liczby skupisk
clusters = range(1, 7) # sprawdzane możliwe liczby skupisk
inertias = [] # zbiór inercji
plt.figure()
for i in clusters:
  km = KMeans(n_clusters = i, # liczba przewidywanych skupisk/centroidów
              n_init = 5, # liczba wewnętrznych iteracji na dany centroid
              max_iter = 100, # liczba iteracji algorytmu
              random_state = 0) # seed

  km.fit_predict(X) # uruchomienie algorytmu
  inertias.append(km.inertia_)

# wykres inercji
# szukanie tzw. "łokcia", czyli punktu na wykresie, w którym widać stabilizację (wartość inercji przestaje gwałtownie spadać)
# z wykresu widać, że tym punktem jest 5, a więc optymalna liczba skupisk to 5
#plt.figure(figsize = (6, 10))
plt.figure()
plt.plot(clusters, inertias, marker = "o")
plt.xlabel("liczba skupisk")
plt.ylabel("inercja", rotation = 0, labelpad = 20)
plt.show()

# przygotowanie algorytmu KMeans dla określonej poprzednio optymalnej liczby skupisk
kmeans = KMeans(n_clusters = 5,
                n_init = 5,
                max_iter = 100,
                random_state = 0)

# uruchomienie algorytmu i zwrócenie otrzymanych przydziałów blobów do skupisk
labels = kmeans.fit_predict(X)

# zliczenie ile rzeczywiście jest skupisk i jakich są one rozmiarów na podstawie danych z pliku
real_labels, real_labels_sizes = np.unique(y, return_counts = True)

# zliczenie ile za pomocą algorytmu uzyskano skupisk i jakich są one rozmiarów
calculated_labels, calculated_labels_sizes = np.unique(labels, return_counts = True)

# wykresy skupisk
plt.figure()
for i in range(len(calculated_labels)):
  plt.scatter(X[labels == i, 0], X[labels == i, 1],
              s = 30, edgecolor = "black",
              label = f"Skupisko {i + 1}")

# wykres centroidów
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            s = 150, marker = "*", c = "yellow", edgecolor = "black",
            label = "Centroidy")

# dodatkowe parametry wykresu i wyświetlenie wykresu
plt.legend()
plt.xlabel("$x_1$")
plt.ylabel("$x_2$", rotation = 0)
plt.grid()
plt.tight_layout()
plt.show()


# wnioski

# Metoda łokciowa wykazała, że optymalna liczba skupisk to 5, co oznacza. Wykres
# inercji pokazuje wyraźne spowolnienie spadku wartości inercji przy tej liczbie skupisk.

# Liczby i rozmiary wykrytych skupisk są zgodne z rzeczywistym rozkładem.

# Wizualizacja wyników pokazuje, że punkty danych zostały poprawnie przypisane do
# klastrów, a centroidy są zlokalizowane w centralnych punktach każdego skupiska.
# Centroidy dobrze reprezentują środek gęstości danych w każdym klastrze.