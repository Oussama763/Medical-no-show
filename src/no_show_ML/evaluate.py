import os
from .preprocessing import load_and_preprocess
import joblib
from sklearn.metrics import accuracy_score


def evaluate_models(models_dir=None):
    if models_dir is None:
        models_dir = os.path.join(os.path.dirname(__file__), 'models')

    X, y = load_and_preprocess(os.path.join(os.path.dirname(__file__), 'data', 'noshowappointments.csv'))

    results = {}
    for fname in os.listdir(models_dir):
        if not fname.endswith('.pkl'):
            continue
        path = os.path.join(models_dir, fname)
        model = joblib.load(path)
        try:
            preds = model.predict(X)
            acc = accuracy_score(y, preds)
            results[fname] = acc
        except Exception:
            results[fname] = None

    return results


if __name__ == '__main__':
    print(evaluate_models())
