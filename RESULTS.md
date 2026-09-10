# Backtest results

Generated 2026-09-10 on LIVE FRED data.

## Provenance

```
commit:           6eae64b
data source:      LIVE FRED
vintage mode:     ALFRED vintages where available, release-lag proxy otherwise
replay window:    1995-01-01 to 2026-09-10
replay factor:    DFM (all 380 months converged)
recognition lag:  4 months
seed:             n/a (replay is deterministic)
python:           3.11.16 on linux
packages:         pandas 3.0.5, numpy 2.4.6, scipy 1.17.1, scikit-learn 1.9.0, statsmodels 0.15.0, hmmlearn 0.3.3, fredapi 0.5.2, pyyaml 6.0.3, plotly 7.0.0, requests 2.34.2, streamlit 1.63.0
```

## Results

```
============================================================
HONEST EVALUATION RESULTS
============================================================
data source:                 LIVE FRED
replay window:               1995-01-01 to 2026-09-10
replay months evaluated:     380
replay factor:               DFM (all 380 months converged)

in-sample recession AUC:     0.949
out-of-sample recession AUC: 0.934
OOS Brier score:             0.058

real-time vs final corr:     0.897
composite revision MAE:      0.327
============================================================
```
