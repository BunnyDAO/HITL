# CONTEXT — domain glossary

Glossary only. No implementation details. Terms are canonical: use these
spellings and meanings in code, templates, skills, and docs.

## Display-metrology terms

- **FGR (Flat Gray Raster)** — a uniform mid-gray test pattern shown
  full-screen. Used to measure how evenly a display emits light. In this
  mock repo the "display" is simulated; an FGR field is a numpy array that
  is *nominally* uniform but carries a tunable gentle non-uniformity so
  uniformity tests are meaningful.

- **ROI (Region of Interest)** — a rectangular sub-area of a captured
  image, identified by pixel bounds. Measurements are computed per-ROI,
  not per-pixel, for uniformity work.

- **Lv (luminance)** — photometric brightness. This repo has no real
  photometer; the `uint8` grayscale pixel value is used as a **luminance
  proxy**. "Lv" and "mean pixel value of an ROI" are interchangeable here.

- **Uniformity** — the canonical metric for "is the panel evenly lit":

      uniformity = (max_ROI_mean_Lv - min_ROI_mean_Lv) / max_ROI_mean_Lv

  expressed as a percentage. Lower is better. A perfectly even field has
  uniformity 0%. This is a **cross-ROI** metric (compares ROIs to each
  other), NOT a within-ROI or per-pixel metric.

- **Within-ROI pixel spread** — a *different* metric (per-pixel
  coefficient of variation inside one ROI). Explicitly NOT what
  `assert_roi_uniformity` checks. Named here only to keep the distinction
  sharp; not implemented.

- **Mura** — large-area display non-uniformity (blotches, gradients,
  hot-spots). The thing high uniformity values indicate. Used informally;
  the measurable proxy is `uniformity` above.
