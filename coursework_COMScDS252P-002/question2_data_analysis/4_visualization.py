"""Generate and save visualization files from cleaned books data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px

ROOT_DIR = Path(__file__).resolve().parent
CLEANED_FILE = ROOT_DIR / "data" / "cleaned_books_data.csv"
VIZ_DIR = ROOT_DIR / "visualizations"


def main() -> None:
    """Create histogram, boxplot, scatter, and top-category bar chart."""
    if not CLEANED_FILE.exists():
        raise FileNotFoundError(f"Cleaned input not found: {CLEANED_FILE}")

    VIZ_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(CLEANED_FILE)

    fig_hist = px.histogram(
        df,
        x="Price_Cleaned",
        nbins=20,
        title="Price Distribution",
        labels={"Price_Cleaned": "Price (£)"},
    )
    fig_hist.add_vline(
        x=df["Price_Cleaned"].mean(),
        line_dash="dash",
        line_color="red",
        annotation_text="Mean",
    )
    fig_hist.write_html(VIZ_DIR / "price_distribution_histogram.html")

    top_categories = df["Category"].value_counts().head(5).index
    df_top5 = df[df["Category"].isin(top_categories)]

    fig_box = px.box(
        df_top5,
        x="Category",
        y="Price_Cleaned",
        title="Price Distribution by Category (Top 5)",
    )
    fig_box.write_html(VIZ_DIR / "price_by_top5_category_boxplot.html")

    fig_scatter = px.scatter(
        df,
        x="Rating_Num",
        y="Price_Cleaned",
        title="Price vs Rating",
        hover_data=["Title", "Category"],
    )
    fig_scatter.write_html(VIZ_DIR / "price_vs_rating_scatter.html")

    top_8_categories = (
        df.groupby("Category")["Rating_Num"]
        .mean()
        .nlargest(8)
        .reset_index()
    )

    fig_bar = px.bar(
        top_8_categories,
        x="Rating_Num",
        y="Category",
        orientation="h",
        title="Top 8 Categories by Average Rating",
        labels={"Rating_Num": "Average Rating", "Category": "Category"},
    )
    fig_bar.write_html(VIZ_DIR / "top8_categories_by_average_rating.html")

    print(f"Saved visualization files to {VIZ_DIR}")


if __name__ == "__main__":
    main()
