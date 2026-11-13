# Submission notes (draft - edit before submitting)

## Project name
SAR Detective

## One-line description
A website that shows people in flood-prone areas where NISAR radar saw the ground change after a flood, and explains it in plain language.

## Short description
SAR Detective compares two NASA-ISRO NISAR radar images of Pagosa Springs, Colorado, taken before (Oct 14, 2026) and after (Oct 26, 2026) the October San Juan River flood. It removes radar noise, flags places where the radar echo changed by 3 dB or more, and checks the result against the river's path: flagged change is about 8 times more common within 200 m of the river than 1 km away. The website shows before and after images, a change map, a river line and example spots, plus a question box that answers only from verified facts and never claims that a specific home flooded. A printable report lists the data, method, results and limitations.

## How we used NISAR
Two NISAR L2 GCOV scenes (track 27, frame 70, HH polarization), read remotely and cropped to a 10 km area, quality-masked with the product's own flags.

## 2-minute demo script
1. The question: where did the flood change the ground around Pagosa Springs?
2. Before vs after: move the slider.
3. Change map: blue lines follow the San Juan River.
4. Evidence: 8x more change near the river; news reports of the Oct 23 crest.
5. Honesty: a change far from the river that is not the flood; limits of the data.
6. Ask the AI: "Does this mean my street flooded?" - it says the map cannot tell.
7. Report: open and print.

## AI-use disclosure
We used Claude (Anthropic) as a coding assistant to help write and debug parts of the Python notebook, web map, and backend. Our team chose the challenge, study area and flood event, selected the NISAR scenes, made the analysis decisions (quality rules, the 3 dB threshold, the river near/far check), reviewed and tested all code, and wrote the conclusions and limitations. The website's question box can use the Claude API to explain the results in plain language; it answers only from our verified results and does not claim that any specific home flooded. All data comes from NASA-ISRO NISAR (via ASF) and OpenStreetMap; no AI-generated data or images are used.

## Check on the event's submission page before submitting
- [ ] Deadline and time zone
- [ ] Required fields (title, description, team, links)
- [ ] Video: required? maximum length?
- [ ] Repository must be public? License required?
- [ ] Live demo link required? (see Deploy in README)
- [ ] All team members registered and listed
