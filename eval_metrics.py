import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("eval_intents.csv")

y_true = df["gold_intent"]
y_pred = df["pred_intent"]

# Rapport complet par classe + moyennes micro/macro/weighted
print(classification_report(y_true, y_pred, digits=3))

# (Optionnel) matrice de confusion
labels = sorted(set(y_true) | set(y_pred))
cm = confusion_matrix(y_true, y_pred, labels=labels)
cm_df = pd.DataFrame(cm, index=[f"true:{l}" for l in labels],
                        columns=[f"pred:{l}" for l in labels])
print("\nConfusion matrix:\n", cm_df)
