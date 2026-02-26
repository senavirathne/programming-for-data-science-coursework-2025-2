"""Train a simple price prediction model using rating and category features."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

ROOT_DIR = Path(__file__).resolve().parent
CLEANED_FILE = ROOT_DIR / "data" / "cleaned_books_data.csv"


def main() -> None:
    """Fit linear regression and report model metrics and top coefficients."""
    if not CLEANED_FILE.exists():
        raise FileNotFoundError(f"Cleaned input not found: {CLEANED_FILE}")

    df = pd.read_csv(CLEANED_FILE)

    x = pd.get_dummies(df[["Rating_Num", "Category"]], drop_first=True)
    y = df["Price_Cleaned"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"R^2 Score: {r2:.4f}")
    print(f"Mean Absolute Error (MAE): £{mae:.2f}")

    coefficients = pd.DataFrame({"Feature": x.columns, "Coefficient": model.coef_})
    coefficients["Abs_Coefficient"] = coefficients["Coefficient"].abs()
    top_features = coefficients.sort_values(by="Abs_Coefficient", ascending=False)

    print("\nTop 5 Influential Features on Price:")
    print(top_features.head(5).to_string(index=False))


if __name__ == "__main__":
    main()
