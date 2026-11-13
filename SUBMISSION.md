# SAR Detective - NASA Space Apps Cairo 2026 submission

Challenge: Dancing with the SARs (NASA-ISRO NISAR radar)

## Project demo
Seven-slide presentation: [paste the public link to the deck here]

Live demo of the working tool: https://sar-detective.vercel.app

## Project links
- Final project (live website): https://sar-detective.vercel.app
- GitHub repository: https://github.com/nabilramyy/sar-detective
- Development notebook (Google Colab): [paste the shared Colab link here]

## Project summary
**Problem.** After a flood, people who live in flood-prone areas cannot easily see where the ground changed. Storm clouds block ordinary satellite photos, and news reports do not show what changed near home.

**Solution.** SAR Detective compares two NASA-ISRO NISAR L-band radar images of Pagosa Springs, Colorado, taken 12 days apart on the same track: before (Oct 14, 2026) and after (Oct 26, 2026) the October San Juan River flood. It applies the product's own quality masks, filters radar speckle, removes a whole-scene processing offset, and flags places where the radar echo changed by 3 dB or more. A website shows before and after images with a slider, a change map, the river line, a clear example and a probable false alarm, a question box that answers only from verified results, and a printable report.

**Results.** Flagged change is about 8 times more common within 200 m of the San Juan River (2.85% of ground) than 1 km or more away (0.35%), mostly brighter along the banks. The USGS river gauge confirms the timing: the river peaked at 15.02 ft on Oct 23 and was still about 9 ft (about 4 ft above normal) at the after pass.

**Impact.** Residents, responders and planners get a plain-language map of where the ground changed, with honest limits, so they know where to look and when to rely on official flood maps instead.

**How it meets the challenge.** It uses NISAR observations to visualize a real change on Earth's surface and explains it for non-experts.

## Project resources
- NASA-ISRO NISAR L2 GCOV scenes via ASF (track 27, frame 70, HH): NISAR_L2_PR_GCOV_033_027_D_070_4005_DHDH_A_20261014T015823_20261014T015857_P05023_N_F_J_001 (before) and NISAR_L2_PR_GCOV_034_027_D_070_4005_DHDH_A_20261026T015823_20261026T015858_P05036_N_F_J_001 (after)
- NASA Earthdata login and the earthaccess library for remote reading
- USGS NWIS gauge 09342500, San Juan River at Pagosa Springs, CO (provisional instantaneous gage height and discharge)
- OpenStreetMap contributors: San Juan River line and base map (ODbL)
- News reports of the Oct 2026 flood: NPR (Oct 23, 2026) and AP (Nov 2, 2026), linked on the website
- NASA NISAR mission pages (science.nasa.gov/mission/nisar)
- Tools: Python, Google Colab, h5py, NumPy, SciPy, rasterio, pyproj, pandas, Matplotlib, Leaflet, FastAPI, Vercel, GitHub

## AI-use disclosure
We used Claude (Anthropic) as a coding assistant to help write and debug parts of the Python notebook, web map, and backend. Our team chose the challenge, study area and flood event, selected the NISAR scenes, made the analysis decisions (quality rules, the 3 dB threshold, the river near/far check), reviewed and tested all code, and wrote the conclusions and limitations. The website's question box can use the Claude API to explain the results in plain language; it answers only from our verified results and does not claim that any specific home flooded. All data comes from NASA-ISRO NISAR (via ASF) and OpenStreetMap; no AI-generated data or images are used.

## Team
- Ramy Slait
- Reem Elsayed
- Mohamed Hesham
- Shadw Abdel Aziz
- Habiba Hashem
- Nabil Ramy
