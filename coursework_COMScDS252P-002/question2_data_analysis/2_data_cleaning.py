"""Clean raw book data and write cleaned CSV."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
RAW_FILE = DATA_DIR / "raw_books_data.csv"
CLEANED_FILE = DATA_DIR / "cleaned_books_data.csv"

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def clean_price(price_str: str) -> float:
    """Convert '£51.77' to 51.77."""
    if isinstance(price_str, str):
        return float(price_str.replace("£", ""))
    return float(price_str)


def clean_rating(rating_str: str) -> int:
    """Convert text rating to numeric score."""
    return RATING_MAP.get(rating_str, 0)


def clean_availability(availability: str) -> bool:
    """Map availability string to bool."""
    return "In stock" in str(availability)


def categorize_price(price: float) -> str:
    """Bucket cleaned price into ranges."""
    if price < 20:
        return "Budget"
    if price <= 40:
        return "Mid-range"
    return "Premium"


def main() -> None:
    """Load raw data, clean it, and persist cleaned output."""
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Raw input not found: {RAW_FILE}")

    df = pd.read_csv(RAW_FILE)

    df["Price_Cleaned"] = df["Price"].apply(clean_price)
    df["Rating_Num"] = df["Rating"].apply(clean_rating)
    df["In_Stock"] = df["Availability"].apply(clean_availability)

    print("Before cleaning")
    print(df.isnull().sum())
    print(f"Duplicates: {df.duplicated().sum()}")

    df = df.drop_duplicates().copy()
    df["Price_Category"] = df["Price_Cleaned"].apply(categorize_price)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEANED_FILE, index=False)
    print(f"Saved cleaned dataset to {CLEANED_FILE} ({len(df)} rows)")


if __name__ == "__main__":
    main()
