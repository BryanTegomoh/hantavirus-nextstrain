# Temporal Analysis

This workflow includes optional time-resolved S, M, and L builds for exploratory
assessment of evolutionary rate. These builds are separate from the default
maximum-likelihood trees so that all-record phylogenetic placement is not mixed
with stricter temporal inference.

## What The Time Builds Use

NCBI Virus metadata includes collection, release, and update dates. The
collection date is the relevant biological sampling date. Release and update
dates describe database history and should not be used to estimate mutation
rates.

The temporal builds keep records with usable collection dates:

- `day`
- `month`
- `year`

Records with unknown date precision are excluded from time-resolved builds. The
current public time builds also apply a lower cutoff of 2010 to sampled tip
collection dates. No upper date cutoff is configured, so the latest retained
tips depend on the eligible NCBI records present when the workflow is run.

## What The Time Axis Means

The time-resolved builds use `augur refine --timetree` to estimate node dates
from sampling dates and genetic divergence. In Auspice, this adds calendar-date
coordinates (`num_date`) so the tree can be viewed with time on the x axis.

The 2010 filter applies to sampled tips only. Internal node dates are model
estimates from TreeTime. In a pan-Orthohantavirus tree, deep divergence can push
some internal node estimates far earlier than the modern sampling window. Those
dates should be treated as exploratory clock behavior, not as sampled records
before 2010.

For this reason, public Auspice datasets open on the divergence x-axis by
default. The time axis remains available for clock review, but it is not the
default interpretation surface.

The estimated rate should be interpreted separately for S, M, and L. A single
pan-Orthohantavirus rate can be misleading because the dataset spans deep
divergence, multiple hosts, multiple countries, and segmented genomes with
possible reassortment.

## Interpretation Guardrails

Use the time view to ask whether there is enough temporal signal for a segment,
not as proof of transmission.

Before presenting rate estimates externally:

1. Check root-to-tip regression for each segment.
2. Review outliers removed by the clock filter.
3. Compare day/month/year-date results against a stricter day-only sensitivity
   analysis.
4. Avoid claims from branches driven by sparse dates, ambiguous locations, or
   one segment alone.
