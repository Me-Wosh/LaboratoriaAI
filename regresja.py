# -*- coding: utf-8 -*-
"""regresja.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1C2qEh13J1jixWMnWMwIrA4MLGjJgN-YC
"""

# import bibliotek
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mlxtend.plotting import heatmap
from mlxtend.plotting import scatterplotmatrix
from sklearn.linear_model import RANSACRegressor, LinearRegression

# wczytanie danych z pliku csv
csv = pd.read_csv("BostonHousing.data.csv", header = None)

# nadanie kolumnom tytułów
csv.columns = ["CRIM", "ZN", "INDUS", "CHAS",
               "NOX", "RM", "AGE", "DIS", "RAD",
               "TAX", "PTRATIO", "B", "LSTAT", "MEDV"]

# wybranie przykładowych kolumn
columns = ["LSTAT", "INDUS", "NOX", "RM", "MEDV"]

# wykresy dla pięciu przykładowych cech zestawu
scatterplotmatrix(csv[columns].values, figsize = (10, 8), names = columns, alpha = 0.5)
plt.tight_layout()
plt.show()

# mapa cieplna pięciu cech zestawu
# pomocna w identyfikacji silnych oraz słabych korelacji między zmiennymi.
# na jej podstawie można wybrać dane do regresji liniowej poprzez identyfikację
# tych zmiennych, które wykazują wysoką korelację liniową (dodatnią lub ujemną)
cm = np.corrcoef(csv[columns].values.T)
hm = heatmap(cm, row_names = columns, column_names = columns)
plt.show()

# obliczenie regresji liniowej dla kolumn RM i MEDV
X = csv[["RM"]].values
y = csv["MEDV"].values
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)
print(f"Nachylenie: {model.coef_[0]}")
print(f"Punkt przecięcia z osią y: {model.intercept_}")

# wykres uśrednionej liczby pomieszczeń RM
plt.scatter(X, y, c = "steelblue", edgecolor = "white", s = 70)
plt.plot(X, model.predict(X), color = "black", lw = 2)
plt.xlabel("Uśredniona liczba pomieszczeń [RM]")
plt.ylabel("Cena w tysiącach dolarów [MEDV]")
plt.show()

# zastosowanie algorytmu RANSAC w celu eliminacji znacznie odstających danych
ransac = RANSACRegressor(LinearRegression(), # bazowy model - w tym przypadku regresja liniowa
                         max_trials = 100, # maksymalna liczba prób wykrycia dopasowanych punktów
                         min_samples = 50, # minimalna liczba pobranych próbek do oszacowania modelu
                         loss = "absolute_error", # kryterium straty do oceny jakości dopasowania
                         residual_threshold = 10.0, # wartość powyżej której punkty będą uznane za odstające
                         random_state = 0) # seed, który eliminuje losowość wyników, celem zapewnienia powtarzalności wyników

# trening RANSAC
ransac.fit(X, y)

# wykres regresji liniowej oszacowanej przez RANSAC wraz z wyróżnionymi punktami odstającymi
inlier_mask = ransac.inlier_mask_
outlier_mask = np.logical_not(inlier_mask)
line_X = np.arange(3, 10, 1)
line_y_ransac = ransac.predict(line_X[:, np.newaxis])
plt.scatter(X[inlier_mask], y[inlier_mask],
            c = "steelblue", edgecolor = "white",
            marker = "o", label = "Punkty nieodstające")
plt.scatter(X[outlier_mask], y[outlier_mask],
            c = "limegreen", edgecolor = "white",
            marker = "s", label = "Punkty odstające")
plt.plot(line_X, line_y_ransac, color = "black", lw = 2)
plt.xlabel("Uśredniona liczba pomieszczeń [RM]")
plt.ylabel("Cena w tysiącach dolarów [MEDV]")
plt.legend()
plt.show()

print(f"Nachylenie: {ransac.estimator_.coef_[0]}")
print(f"Punkt przecięcia z osią y: {ransac.estimator_.intercept_}")


# wnioski

# Regresja liniowa bez filtracji danych była podatna na zakłócenia wynikające z
# obecności odstających wartości.

# Metoda RANSAC pozwoliła na poprawę dokładności modelu poprzez uwzględnienie
# wyłącznie punktów dobrze reprezentujących zależność między zmiennymi.

# Po zastosowaniu RANSAC nachylenie oraz punkt przecięcia z osią Y uległy zmianie,
# co pokazuje, że obecność odstających danych miała wpływ na wcześniejszy model.