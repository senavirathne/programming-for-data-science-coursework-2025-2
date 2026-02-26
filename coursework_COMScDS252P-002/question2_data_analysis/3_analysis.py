"""Run descriptive and inferential analysis on cleaned books data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from scipy import stats

ROOT_DIR = Path(__file__).resolve().parent
CLEANED_FILE = ROOT_DIR / "data" / "cleaned_books_data.csv"


def main() -> None:
    """Print analysis outputs equivalent to the notebook steps."""
    if not CLEANED_FILE.exists():
        raise FileNotFoundError(f"Cleaned input not found: {CLEANED_FILE}")

    df = pd.read_csv(CLEANED_FILE)

    print("Price Statistics:")
    print(df["Price_Cleaned"].describe())

    print(f"\nMode Price: {df['Price_Cleaned'].mode()[0]}")
    print(f"Price Range: {df['Price_Cleaned'].max()} - {df['Price_Cleaned'].min()}")

    top_categories = df["Category"].value_counts().head(5).index
    df_top5 = df[df["Category"].isin(top_categories)]
    print("\nAverage Price by Top 5 Category:")
    print(df_top5.groupby("Category")["Price_Cleaned"].mean())

    rating_counts = df["Rating_Num"].value_counts().sort_index(ascending=False)
    rating_dist_df = pd.DataFrame({"Rating": rating_counts.index, "Frequency": rating_counts.values})
    print("\nRating Frequency Distribution:")
    print(rating_dist_df.to_string(index=False))

    q1 = df["Price_Cleaned"].quantile(0.25)
    q3 = df["Price_Cleaned"].quantile(0.75)
    iqr = q3 - q1
    outliers = df[(df["Price_Cleaned"] < (q1 - 1.5 * iqr)) | (df["Price_Cleaned"] > (q3 + 1.5 * iqr))]
    print(f"\nNumber of price outliers: {len(outliers)}")

    corr, p_value = stats.pearsonr(df["Price_Cleaned"], df["Rating_Num"])
    print(f"Pearson Correlation (Price vs Rating): {corr:.4f}, p-value: {p_value:.4f}")

    df = df.dropna(subset=["Category"]).copy()
    is_fiction_mask = df["Category"].str.contains("fiction", case=False, na=False)

    fiction_prices = df[is_fiction_mask]["Price_Cleaned"]
    non_fiction_prices = df[~is_fiction_mask]["Price_Cleaned"]

    print("\n--- Hypothesis Testing: Fiction vs Non-Fiction ---")
    print(f"Fiction Books Count: {len(fiction_prices)}, Average Price: £{fiction_prices.mean():.2f}")
    print(f"Non-Fiction Books Count: {len(non_fiction_prices)}, Average Price: £{non_fiction_prices.mean():.2f}")

    t_stat, t_p_value = stats.ttest_ind(fiction_prices, non_fiction_prices, equal_var=False)
    alpha = 0.05
    print(f"\nt-statistic: {t_stat:.4f}")
    print(f"p-value: {t_p_value:.4f}")

    if t_p_value < alpha:
        print(f"Conclusion: Reject the null hypothesis (alpha={alpha}).")
    else:
        print(f"Conclusion: Fail to reject the null hypothesis (alpha={alpha}).")

    print("")
if __name__ == "__main__":
    main()
