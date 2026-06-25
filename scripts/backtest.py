"""Honest evaluation: in-sample vs out-of-sample on one consistent dataset."""
from __future__ import annotations

import argparse
import datetime as dt
import warnings

warnings.filterwarnings("ignore")

from macro_nowcaster.config import get_settings
from macro_nowcaster.data.fred_client import get_client
from macro_nowcaster.features.transforms import standardized_panel
from macro_nowcaster.models.dfm import fit_pca_factor
from macro_nowcaster.models.recession import fit_nowcast
from macro_nowcaster.backtest.pseudo_realtime import replay, evaluate


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="1995-01-01")
    ap.add_argument("--end", default=None)
    args = ap.parse_args()

    settings = get_settings()
    client = get_client(settings)
    mode = "LIVE FRED" if settings.fred_api_key else "SYNTHETIC"
    end = args.end or dt.date.today().isoformat()

    print(f"data source: {mode}")
    print(f"replay window: {args.start} -> {end}")
    print("running replay (this is the slow part)...")

    raw = {c: client.get_series(c) for c in settings.codes}
    raw = {k: v for k, v in raw.items() if v is not None and not v.empty}
    final_z = standardized_panel(raw, settings, mode="full")
    final_factor = fit_pca_factor(final_z).factor
    usrec = (client.get_series(settings.recession_flag).resample("ME").mean() > 0.5).astype(int)

    slope = final_z["T10Y3M"] if "T10Y3M" in final_z else None
    in_sample = fit_nowcast(final_factor, slope, usrec)

    rt = replay(client, settings, start=args.start, end=end)
    metrics = evaluate(rt, final_factor, usrec.astype(float))

    lines = [
        "=" * 60,
        "HONEST EVALUATION RESULTS",
        "=" * 60,
        f"data source:                 {mode}",
        f"replay window:               {args.start} to {end}",
        f"replay months evaluated:     {metrics.get('n_periods', 'n/a')}",
        "",
        f"in-sample recession AUC:     {in_sample.auc:.3f}",
        f"out-of-sample recession AUC: {metrics.get('recession_oos_auc', float('nan')):.3f}",
        f"OOS Brier score:             {metrics.get('recession_oos_brier', float('nan')):.3f}",
        "",
        f"real-time vs final corr:     {metrics.get('composite_realtime_vs_final_corr', float('nan')):.3f}",
        f"composite revision MAE:      {metrics.get('composite_revision_mae', float('nan')):.3f}",
        "=" * 60,
    ]
    report = "\n".join(lines)
    print("\n" + report)

    with open("RESULTS.md", "w") as fh:
        fh.write("# Backtest results\n\n")
        fh.write(f"Generated {dt.date.today().isoformat()} on {mode} data.\n\n")
        fh.write("```\n" + report + "\n```\n")
    print("\nsaved to RESULTS.md")


if __name__ == "__main__":
    main()
