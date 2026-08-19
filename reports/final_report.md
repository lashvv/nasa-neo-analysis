# NASA Near-Earth Object Close-Approach Analysis

## Overview

This project analyzes 51,122 recorded close approaches of near-Earth objects (NEOs) to Earth, sourced directly from NASA/JPL's Small-Body Database. The dataset covers approaches within 0.05 AU of Earth, spanning from the year 1900 to 2200 (a mix of historical detections and future projections for already-known objects). The goal was not to build a predictive model, but to explore the data honestly — asking direct questions, testing assumptions rather than accepting them, and paying close attention to *how* the data was generated, since several apparent patterns in this dataset turned out to be artifacts of detection technology and observation limits rather than real astronomical behavior.

## Data Source & Collection

Data was pulled from NASA/JPL's public Close-Approach Data API (`https://ssd-api.jpl.nasa.gov/cad.api`), which requires no API key. The CNEOS website version of this data caps CSV downloads at 20,000 rows, so the API was used instead to retrieve the full dataset (51,122 rows) directly as JSON, converted to a pandas DataFrame, and saved locally.

Query parameters used: `date-min=1900-01-01`, `date-max=2200-01-01`, `dist-max=0.05`, `neo=true`, `diameter=true`, `fullname=true`.

## Data Cleaning

- `cd` (close-approach date) was converted from string to a proper datetime column.
- An `is_comet` flag was added, based on periodic-comet naming conventions in `fullname` (e.g. "289P/Blanpain"). A small number of comets (10 rows) were present alongside asteroids in the `neo=true` results; these were flagged rather than removed, since comets are legitimately near-Earth objects, but they lack `h` values and behave differently in some analyses.
- `v_inf` (25 missing) and `h` (10 missing, all comets) were left as-is — the missing counts are negligible relative to the 51,122 total.
- `diameter` and `diameter_sigma` are missing for the vast majority of rows (~97%) and were left as-is rather than imputed, since a measured diameter is only available for objects that have been specifically studied via radar, infrared, or occultation — filling in the gaps would fabricate data that doesn't exist.

## Distance & Speed

**Is there a relationship between distance and relative velocity?**
No meaningful correlation was found (r ≈ -0.007) across the full dataset, confirmed visually with a scatter plot showing no discernible pattern. How close an object passes appears unrelated to how fast it's moving — this likely reflects that approach speed is driven by an asteroid's own orbital shape, not by the specific geometry of a given Earth encounter. This lack of correlation held up even when checking the fastest and slowest extremes of the dataset individually (though see the note below on that check).

**What does the distribution of close-approach distances look like?**
Frequency increases somewhat steadily from close-in (~620 approaches in the nearest bin) to the 0.05 AU boundary (~1,250 approaches in the farthest bin). Initially this was assumed to be a simple geometric effect — more space exists in a wide outer "shell" around Earth than in a narrow inner one, so more objects would be expected to pass through it by chance. Testing this against a proper r² prediction curve showed the real data grows *faster* than pure geometry would predict, especially at small distances. This means geometry alone does not explain the pattern; a more likely explanation is that close approaches receive disproportionate tracking/confirmation attention (they're the ones NASA's planetary defense programs care most about getting right), making them relatively overrepresented compared to a purely random-geometry expectation.

**How many objects passed closer than the Moon, or closer than geostationary satellites?**
1,712 objects (3.35%) passed closer than the Moon's average distance (~0.00257 AU). Only 55 objects (0.11%) passed within geostationary satellite altitude (~0.00017 AU) — a genuinely rare, closely-tracked group. Every one of these 55 objects is small (high `h`, no measured diameter), consistent with the idea that a large object on a trajectory this close would already be a well-known, tracked body long before its approach.

**What are the fastest and slowest recorded relative velocities?**
Slowest approaches ranged from ~0.07 to 0.28 km/s (at distances of 0.024–0.047 AU). Fastest approaches ranged from ~40.5 to 42.9 km/s (at distances of 0.012–0.049 AU). Neither extreme is concentrated at any particular distance when inspected directly — though checking correlation within the top/bottom 50 by speed (rather than just the top/bottom 5) revealed a real, moderate negative relationship in both groups (fastest 50: r = -0.22; slowest 50: r = -0.38) that the full-dataset correlation (r ≈ -0.007) does not show. This suggests the distance-speed relationship may only emerge at the statistical extremes, and is a useful reminder that a handful of rows is not enough to rule a pattern in or out. Separately, the single fastest object in the dataset (42.9 km/s) is the comet `1999 J6`, plausibly explained by comets generally having more eccentric orbits than typical asteroids.

**Does relative velocity have a typical range?**
Yes, but with meaningful spread. Mean = 10.30 km/s, median = 9.31 km/s, std = 5.27 km/s, with the middle 50% of values falling between 6.57 and 13.00 km/s. The distribution is right-skewed — a peak around 8-10 km/s with a long tail out to 40+ km/s — meaning the mean is pulled upward by a minority of fast outliers, and the median is the more representative "typical" value.

## Size-Related

**Is there a relationship between size (h) and speed?**
A moderate correlation was found between `h` and `v_rel` (r = -0.41). Since lower `h` means a larger object, this means larger objects tend to reach higher speeds, and smaller objects cluster at lower speeds — visually confirmed with a scatter plot showing a clear downward-sloping, fan-shaped trend. However, this is very likely a detection-bias artifact rather than a real physical relationship: there is no known physical mechanism linking an asteroid's size to its orbital speed. The more plausible explanation is that fast-moving small objects are the hardest category for telescope surveys to catch — they're only bright enough to detect in a brief window near closest approach, and high speed shortens that window before the object can be photographed and confirmed. Slow small objects remain detectable for longer, and large objects are detectable from farther away regardless of speed, so they aren't subject to this same filtering. In short: this pattern most likely reflects what we're able to observe, not how asteroids actually behave.

**Is there a relationship between size (h) and distance?**
A moderate correlation was found (r = -0.323): larger objects (low `h`) tend to be detected across the full distance range including far out, while smaller objects (high `h`) tend to only be detected when close. This lines up directly with the Moon/geostationary threshold finding above, where every one of the 55 closest-approaching objects was small. The likely explanation is again observational: large objects are bright enough to spot from far away, while small objects are essentially invisible until they're already close.

**Does the h size proxy actually hold up against real measured diameters?**
Yes, strongly. For the ~1,500 rows with actual measured diameter data, `h` and `diameter` show a strong negative relationship. Plotted on a linear scale it appears as a steep curve; plotted with diameter on a log scale, it becomes a clean, tight straight line — confirming that `h` behaves exactly as expected for a logarithmic size proxy. This validates using `h` as a stand-in for size throughout the rest of the analysis, since the subset with real diameter data confirms the proxy is trustworthy rather than just theoretically reasonable.

## Uncertainty & Tracking Quality

**Which objects have the most uncertain approach times, and why?**
The 20 approaches with the highest timing uncertainty (parsed from the `t_sigma_f` field) all cluster tightly around ~10 days of uncertainty — a surprisingly narrow band, suggesting a practical reporting ceiling rather than these being individually the "worst" cases. These high-uncertainty approaches span both the far past (back to 1902) and far future (up to 2183), and mostly have low `orbit_id` values (objects whose orbits have only been refined a handful of times) along with moderate-to-high `h` values (skewing toward smaller, fainter objects). High timing uncertainty appears driven by a combination of limited observation history and temporal distance from the present, rather than any single dominant cause.

## Frequency & Time Patterns

**Has the number of recorded close approaches increased over time?**
Yes, dramatically — but the shape of the trend reveals more than the increase itself. The data shows a flat baseline (~100-150 approaches/year) from 1900 through roughly 2000, a sharp rise peaking around 1,700-1,800 approaches/year near the present (2026), and then a sudden drop back to baseline (~100-150/year) from roughly 2030 onward, remaining flat all the way through 2200.

The rise into the present matches an expected detection-technology story: modern asteroid surveys are far more capable than those of previous decades. The sudden post-2030 drop, however, is not a real decline in asteroid activity — it's a structural artifact of when this dataset was generated. NASA can only forecast a *future* close approach for an asteroid whose orbit is already well-determined, meaning an object that has already been discovered. Since new asteroids are continually being found, the present moment (2026) marks the boundary between confirmed historical detections and a shrinking pool of currently-known objects with reliable long-term forecasts. Objects that will be discovered between now and 2200 simply cannot appear in this dataset yet.

**Are there seasonal patterns in detection?**
Yes. Restricting to the 2000-2026 period (the reliable, high-detection era), close approaches are recorded noticeably less often from May through August (~1,000-1,500/month) compared to September through February (~1,800-2,500/month), peaking sharply in October. Since asteroids have no reason to follow Earth's calendar, this is best explained by observing conditions rather than any real seasonal astronomical pattern — major survey telescopes are concentrated in specific regions (e.g. the US Southwest, Hawaii), where seasonal weather (such as summer monsoon season) reduces the number of clear observing nights during exactly that May-August window.

## Key Takeaways

- Distance and relative velocity show no meaningful relationship across the dataset as a whole, though a real relationship emerges when looking specifically at the statistical extremes.
- Several patterns that look astronomical at first glance — the distance distribution, the size-speed relationship, the size-distance relationship, and the sharp drop in approaches after 2030 — are best explained by how the data was collected and detected, not by real behavior of near-Earth objects.
- The `h` absolute-magnitude proxy is a reliable stand-in for object size, confirmed against real measured diameters where available.
- Small asteroids are systematically underrepresented at large distances and overrepresented at very close distances, a direct consequence of detection sensitivity limits.
- Detected approaches follow a clear seasonal pattern most plausibly tied to observatory weather conditions rather than orbital mechanics.

## Limitations & Caveats

- Only ~3% of the dataset has a real measured diameter; all size-based conclusions rely primarily on the `h` proxy, which — while validated against the available diameter data — is still an indirect measurement.
- The dataset's future-dated rows (post-2026) represent predictions for currently known objects only, not a complete picture of future close approaches, and should not be read as a forecast of true future asteroid activity.
- Detection-technology and observational biases (survey sensitivity, geographic telescope placement, seasonal weather) appear to influence several patterns in this data more strongly than real physical or orbital relationships. Conclusions here describe what was *recorded*, not necessarily the true underlying population of near-Earth objects.