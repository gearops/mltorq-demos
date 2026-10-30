#!/usr/bin/env python3
"""MLGear Titanic demo trainer. Prefer torch+CUDA when available; else sklearn CPU.
Writes metrics.json next to --outdir for cost Learn.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import pandas as pd


def load_or_synthesize(data_path: Path) -> pd.DataFrame:
    if data_path.exists():
        return pd.read_csv(data_path)
    # tiny synthetic Titanic-like set so demos work offline
    rows = []
    for i in range(200):
        rows.append({
            "PassengerId": i + 1,
            "Survived": int(i % 3 != 0),
            "Pclass": (i % 3) + 1,
            "Sex": "male" if i % 2 == 0 else "female",
            "Age": 20 + (i % 50),
            "SibSp": i % 3,
            "Parch": i % 2,
            "Fare": 10 + (i % 80),
            "Embarked": ["S", "C", "Q"][i % 3],
        })
    return pd.DataFrame(rows)


def prep(df: pd.DataFrame):
    df = df.copy()
    y = df["Survived"].astype(int)
    df["Sex"] = (df["Sex"] == "female").astype(int)
    df["Embarked"] = df["Embarked"].fillna("S").astype("category").cat.codes
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())
    X = df[["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]]
    return X, y


def train_sklearn(X, y):
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42)
    clf = LogisticRegression(max_iter=500)
    t0 = time.time()
    clf.fit(Xtr, ytr)
    elapsed = time.time() - t0
    acc = float(accuracy_score(yte, clf.predict(Xte)))
    return {"backend": "sklearn", "device": "cpu", "accuracy": acc, "train_seconds": elapsed}


def train_torch(X, y, epochs: int):
    import torch
    import torch.nn as nn
    from sklearn.model_selection import train_test_split

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    Xtr, Xte, ytr, yte = train_test_split(X.values, y.values, test_size=0.25, random_state=42)
    xt = torch.tensor(Xtr, dtype=torch.float32, device=device)
    yt = torch.tensor(ytr, dtype=torch.float32, device=device).unsqueeze(1)
    xv = torch.tensor(Xte, dtype=torch.float32, device=device)
    yv = torch.tensor(yte, dtype=torch.float32, device=device).unsqueeze(1)

    model = nn.Sequential(
        nn.Linear(xt.shape[1], 32),
        nn.ReLU(),
        nn.Linear(32, 1),
        nn.Sigmoid(),
    ).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-2)
    loss_fn = nn.BCELoss()
    t0 = time.time()
    model.train()
    for _ in range(epochs):
        opt.zero_grad()
        pred = model(xt)
        loss = loss_fn(pred, yt)
        loss.backward()
        opt.step()
    elapsed = time.time() - t0
    model.eval()
    with torch.no_grad():
        pred = (model(xv) > 0.5).float()
        acc = float((pred == yv).float().mean().item())
    return {
        "backend": "torch",
        "device": str(device),
        "cuda": torch.cuda.is_available(),
        "accuracy": acc,
        "train_seconds": elapsed,
        "epochs": epochs,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="titanic.csv")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--epochs", type=int, default=80)
    ap.add_argument("--prefer-gpu", action="store_true")
    args = ap.parse_args()

    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    df = load_or_synthesize(Path(args.data))
    X, y = prep(df)

    metrics = None
    if args.prefer_gpu:
        try:
            metrics = train_torch(X, y, args.epochs)
        except Exception as e:
            metrics = train_sklearn(X, y)
            metrics["fallback_error"] = str(e)
    else:
        try:
            import torch  # noqa: F401
            metrics = train_torch(X, y, args.epochs)
        except Exception:
            metrics = train_sklearn(X, y)

    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics))


if __name__ == "__main__":
    main()
