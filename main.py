#!/usr/bin/env python
# coding: utf-8

# # Formation pandas
#'
#' Ce notebook permet de s'assurer que tu maitrises un minimum Pandas
#'
#' Tout d'abord lis https://towardsdatascience.com/pandas-dataframe-a-lightweight-intro-680e3a212b96
#' pour comprendre ce qu'est un `dataframe` (et la différence avec les `series`).
#' Garde aussi cette cheat sheet à porté de main : https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf
#'
#' Tu devrais pouvoir jouer ce Notebook cellule par cellule avec le raccourci Ctrl+Enter. Cela te permet
#' de dérouler efficacement ce notebook, étape par étape.
#' Enfin, n'oublie pas d'utiliser les raccourcis de ton IDE et l'auto-complétion !

#' --------------------------------------------------------------------------

# ## Premier setup
#'
#' - Importer pandas (et l'installer s'il n'est pas présent : `pip install pandas`).
#' - Importer numpy (et l'installer s'il n'est pas présent : `pip install numpy`).
#'
#' Utiliser l'alias `pd` pour désigner pandas, et `np` pour désigner numpy.

#%%
import pandas as pd
import numpy as np


# %%
#' Initialiser un premier dataframe

df = pd.DataFrame(
    {
        "age": [5, 2, 6, 8, 2, 4, np.NaN],
        "animal": ["cat", "dog", "cat", "cat", "dog", "bird", "bird"],
    }
)

# ## Play with data 101

#' Je sais récupérer les animaux qui ont exactement 2 ans (filtrage)
df[df["age"] == 2]

#' ou :
df.query("age == 2")

#' mais il préférable d'utiliser `loc` pour éviter de faire des eval de string
df.loc[lambda df: df.age == 2]

# %%
#' Je sais effectuer une opération sur une nouvelle colonne et incrémenter
#' l'age de tous les animaux de 1
df["ageplus1"] = df["age"] + 1

#' ou
df = df.assign(ageplus1=lambda l_df: l_df.age + 1)

# %%
#' Je sais supprimer la colonne que je viens de créer
df = df.drop("ageplus1", axis=1, inplace=True)

# %%
#' Je sais assigner de deux façons une nouvelle colonne à la dataframe avec des surnoms :
#' `['Louis', 'Jack', 'Felix', 'Croquette', 'Alfred', 'Sifflet', 'Piou']`

nicknames = ["Louis", "Jack", "Felix", "Croquette", "Alfred", "Sifflet", "Piou"]
df["nickname"] = nicknames
df.drop("nickname", axis=1, inplace=True)
df.insert(2, "nickname", nicknames)

# %%
#' Je sais compter le nombre d'éléments de chaque classe (récupérer le nombre de chats,
#' de chiens et d'oiseaux)

df.animal.value_counts()
# %%
#' Je sais supprimer une ligne

df = df.drop(2)

# %%
#' Je sais remettre à jour l'index suite à cette suppression

df = df.reset_index()

#' Je sais utiliser insert et df.assign pour ajouter des timestamp (`dtype='datetime64[s]'`) au dataframe.
#'
#' exemple de timestamp : `[1524379940,1524379910,1524379230,1524379420,1524349940,1524379440]`


# With the insert method
timestamps = [1524379940, 1524379910, 1524379230, 1524379420, 1524349940, 1524379441]
df.insert(
    4,
    "timestamp",
    timestamps,
)
df["date"] = pd.to_datetime(df["timestamp"])
df = df.assign(date=lambda l_df: pd.to_datetime(l_df.timestamp, unit="s"))

# We drop the column before doing the same thing with assign
df.drop(columns=["date", "timestamp"], axis=1, inplace=True)

df = df.assign(timestamp=timestamps).assign(
    date=lambda l_df: pd.to_datetime(l_df.timestamp, unit="s")
)

# %%
# Je sais filtrer de trois façons sur des timestamps

print(df[(df["date"] > "2018-04-22 06:52:10") & (df["date"] < "2018-04-23 22:00:00")])
print(df[df["date"] == "2018-04-22 06:52:20"])

# %%
#' Je sais retirer des lignes où des valeurs `NA` apparaissent tout en gardant l'index (et sans le reset)
df = df.dropna()

# %%
#' Je sais renommer une colonne

df = df.rename(columns={"date": "date_renamed"})

# %%
#' Je sais repérer et retirer des duplicats d'une dataframe tout en gardant l'index (et sans le reset)
df.drop_duplicates()

# ##' Transform values 101

# %%
#' Je sais couper un mot en deux (`Jack` -> `['Ja','ck']`) dans une partie d'un dataframe.
#'
#' Je sais créer une nouvelle colonne `surname` pour stocker ce nouveau résultat.
#'
#' Hint :
#  - comprendre la différence entre `map`, `applymap` et `apply` :
#' https://www.geeksforgeeks.org/difference-between-map-applymap-and-apply-methods-in-pandas/


def split_str(s):
    if type(s) is str:
        return [s[: len(s) // 2], s[len(s) // 2 :]]
    else:
        return s


df["surname_splitted"] = df.nickname.map(split_str)

# %%
#' Je sais utiliser la colonne créée pour créer un nouveau dataframe (`df_surname`) qui contient
#' deux colonnes distinctes : `prefix_surname`, `suffix_surname`.
#'
#' J'ai compris qu'une ligne d'un dataframe à plus d'une colonne est un simple objet Series.
# df_surname["prefix_surname"] = df.surname.map(lambda x: x[0])
# df_surname["suffix_surname"] = df.surname.map(lambda x: x[1])
df_surname = (
    pd.DataFrame()
    .assign(prefix_surname=df.surname_splitted.map(lambda x: x[0]))
    .assign(suffix_surname=df.surname_splitted.map(lambda x: x[1]))
)
# %%
#' Remplacer la colonne `surname_splitted` de l'objet `df` par ces deux colonnes
pd.concat([df, df_surname], axis=1)
df.drop("surname_splitted", axis=1)

# %%
#' Pour chaque type d'animal je sais donner le surnom du plus vieux.
#'
#' Hint : utiliser `loc` et `idxmax`

df.loc[df.groupby("animal").apply(lambda g: g.age.idxmax())].nickname

# %%
#' Je sais concaténer deux dataframes, sans oublier de reset l'index et n'avoir
#' que les deux colonnes qui m'intéressent. Je fait tout cela en une ligne.

df1 = pd.DataFrame(
    {
        "age": [5, 2, 6, 8, 2, 4, np.NaN],
        "animal": ["cat", "dog", "cat", "cat", "dog", "bird", "bird"],
    }
)

df2 = pd.DataFrame(
    {"age": [4, 2, 6, 1, 5], "animal": ["cat", "dog", "bird", "cat", "bird"]}
)

df3 = pd.concat([df1, df2], ignore_index=True)

# %%
# ###' Bravo !
#'
#' Tu as finis ce notebook, il te reste encore plein de petits détails à comprendre
#' mais tu as pu commencer à te familiariser avec les dataframes !
#'
#' Envoie ce notebook à ton coach pour qu'il puisse le corriger.

# %% Bonus
# ## Bonus numpy
#'
#' Comprendre l'utilisation de `::` et `,`
#'
#' Créer un échequier en 3 lignes, sans compréhension de liste :
#'
#' ```
#' [[0, 1, 0, 1, 0, 1, 0, 1],
#'  [1, 0, 1, 0, 1, 0, 1, 0],
#'  [0, 1, 0, 1, 0, 1, 0, 1],
#'  [1, 0, 1, 0, 1, 0, 1, 0],
#'  [0, 1, 0, 1, 0, 1, 0, 1],
#'  [1, 0, 1, 0, 1, 0, 1, 0],
#'  [0, 1, 0, 1, 0, 1, 0, 1],
#'  [1, 0, 1, 0, 1, 0, 1, 0]]
#' ```
#'

x = np.zeros((8, 8), dtype=int)
x[1::2, ::2] = 1
x[::2, 1::2] = 1
print(x)
