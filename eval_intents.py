# eval_intents.py
# ----------------------------------------------------
# Évalue précision / rappel / F1 du classifieur d'intentions
# ----------------------------------------------------

import re
import argparse
import json
import os
from typing import List

import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt


# ----------------------------------------------------
# 1) Initialisation de l’inférence
# ----------------------------------------------------
def load_runtime():
    """
    Prépare les objets nécessaires à la prédiction d'intentions.
    Retourne un dict 'runtime' passé ensuite à predict_intent().
    """
    runtime = {}

    # === OPTION A : via ton DataBot (si accessible) ===
    try:
        from src.app.bot.databot import DataBot
        from src.app.project import Project  # adapte si besoin
        project = Project()
        databot = DataBot(project)           # ou project.train_bot()
        runtime["databot"] = databot
        runtime["method"] = "databot"
        return runtime
    except Exception:
        pass

    # === OPTION B : classifieur BESSER direct (si exposé) ===
    try:
        # Adapte cette section à ton projet si tu as un classifieur sauvegardé
        from besser.agent.nlp.intent_classifier import IntentClassifier  # exemple
        ic = IntentClassifier.load("models/intent_classifier")
        runtime["intent_classifier"] = ic
        runtime["method"] = "besser_direct"
        return runtime
    except Exception:
        pass

    # === OPTION C : fallback — classifieur à règles ===
    runtime["method"] = "rules"
    return runtime


# ----------------------------------------------------
# 2) Prédiction d’intention
# ----------------------------------------------------
_INTENTS = [
    "bar_chart", "line_chart", "max_value", "min_value", "pie_chart",
    "select_fields_with_conditions", "show_table", "unknown",
    "value1_vs_value2", "value_frequency"
]

_KEYWORDS = {
    "line_chart": [
        r"\bline chart\b", r"\btrend\b", r"over time", r"\bby year\b", r"\bevolution\b"
    ],
    "bar_chart": [
        r"\bbar chart\b", r"\bcompare\b", r"\bby category\b", r"\bhistogram\b"
    ],
    "pie_chart": [
        r"\bpie\b", r"\bshare\b", r"\bpercentage\b", r"\bdistribution\b"
    ],
    "show_table": [
        r"\b(show|display|list)\b.*\b(table|rows|all)\b"
    ],
    "max_value": [
        r"\bmax(imum)?\b", r"\bhighest\b", r"\bmost (expensive|price|rent)\b"
    ],
    "min_value": [
        r"\bmin(imum)?\b", r"\blowest\b", r"\bcheapest\b"
    ],
    "value_frequency": [
        r"\bhow many\b", r"\bcount\b", r"\bfreq(uency)?\b", r"\bnumber of\b"
    ],
    "value1_vs_value2": [
        r"\b(vs|versus)\b", r"\bcompare\b.*\b(and|vs|versus)\b"
    ],
    "select_fields_with_conditions": [
        r"\b(sum|total|average|mean)\b", r"\bfilter\b", r"\bwhere\b"
    ],
}

def _predict_with_rules(text: str) -> str:
    q = text.lower().strip()
    if not q:
        return "unknown"
    for intent, patterns in _KEYWORDS.items():
        for pat in patterns:
            if re.search(pat, q):
                return intent
    return "unknown"


def predict_intent(text: str, runtime: dict) -> str:
    """
    Retourne le nom de l'intention prédite pour 'text' en fonction de la méthode disponible.
    """
    method = runtime.get("method")

    # A) via DataBot
    if method == "databot" and "databot" in runtime:
        databot = runtime["databot"]
        # essaie d'abord via platform, sinon fallback sur un autre attribut
        try:
            pred = databot.platform.intent_classifier.predict(text)
            return getattr(pred, "name", str(pred))
        except Exception:
            pred = databot.intent_classifier.predict(text)
            return getattr(pred, "name", str(pred))

    # B) classifieur direct
    if method == "besser_direct" and "intent_classifier" in runtime:
        ic = runtime["intent_classifier"]
        pred = ic.predict(text)
        return getattr(pred, "name", str(pred))

    # C) règles
    return _predict_with_rules(text)


# ----------------------------------------------------
# 3) Matrice de confusion
# ----------------------------------------------------
def save_confusion_matrix(y_true: List[str], y_pred: List[str], labels: List[str], out_path: str):
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    fig, ax = plt.subplots(figsize=(max(6, len(labels)*0.8), max(5, len(labels)*0.6)))
    im = ax.imshow(cm, interpolation='nearest', cmap="Blues")
    ax.figure.colorbar(im, ax=ax)

    ax.set(xticks=range(len(labels)),
           yticks=range(len(labels)),
           xticklabels=labels, yticklabels=labels,
           ylabel='Vraies intentions',
           xlabel='Intentions prédites',
           title='Matrice de confusion (intent classification)')

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, cm[i, j],
                    ha="center", va="center",
                    color="white" if cm[i, j] > cm.max()/2. else "black")

    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close(fig)


# ----------------------------------------------------
# 4) Main
# ----------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Eval intents (precision/recall/F1)")
    parser.add_argument("--csv", type=str, required=True, help="Chemin vers eval_intents.csv (colonnes: text,gold_intent)")
    parser.add_argument("--outdir", type=str, default="eval_results", help="Dossier de sortie")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    df = pd.read_csv(args.csv)
    if not {"text", "gold_intent"}.issubset(df.columns):
        raise ValueError("Votre CSV doit contenir les colonnes : text,gold_intent")

    runtime = load_runtime()
    print(f"[INFO] Méthode de prédiction détectée : {runtime.get('method')}")

    y_true, y_pred = [], []
    for _, row in df.iterrows():
        text = str(row["text"])
        gold = str(row["gold_intent"]).strip()
        pred = predict_intent(text, runtime).strip()
        y_true.append(gold)
        y_pred.append(pred)

    labels_sorted = sorted(set(y_true) | set(y_pred))
    report = classification_report(y_true, y_pred, labels=labels_sorted, output_dict=True, zero_division=0)
    report_txt = classification_report(y_true, y_pred, labels=labels_sorted, zero_division=0)

    with open(os.path.join(args.outdir, "classification_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    with open(os.path.join(args.outdir, "classification_report.txt"), "w", encoding="utf-8") as f:
        f.write(report_txt)

    pd.DataFrame(report).transpose().to_csv(os.path.join(args.outdir, "classification_report.csv"))

    save_confusion_matrix(y_true, y_pred, labels_sorted, os.path.join(args.outdir, "confusion_matrix.png"))

    print("\n===== Classification report =====")
    print(report_txt)
    print(f"\n[OK] Rapports enregistrés dans : {args.outdir}")


if __name__ == "__main__":
    main()

