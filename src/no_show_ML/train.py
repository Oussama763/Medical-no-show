import os
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

from .preprocessing import load_and_preprocess


def train_all(csv_path, out_dir=None):
    X, y = load_and_preprocess(csv_path)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        'logistic_reg': LogisticRegression(max_iter=1000),
        'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'decision_tree': DecisionTreeClassifier(random_state=42),
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        results[name] = {'model': model, 'accuracy': acc}

    # Ensure out_dir exists
    if out_dir is None:
        out_dir = os.path.join(os.path.dirname(__file__), 'models')
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    # Save each model
    for name, info in results.items():
        path = os.path.join(out_dir, f"{name}.pkl")
        joblib.dump(info['model'], path)

    # Save best model
    best_name = max(results.keys(), key=lambda n: results[n]['accuracy'])
    best_model = results[best_name]['model']
    joblib.dump(best_model, os.path.join(out_dir, 'best_model.pkl'))

    return {k: v['accuracy'] for k, v in results.items()}, best_name


if __name__ == '__main__':
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'noshowappointments.csv')
    print('Training models from', csv_path)
    results, best = train_all(csv_path)
    print('Results:', results)
    print('Best model:', best)
