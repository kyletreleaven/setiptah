
# Design

Scrape WALKING routes.

Use Directions API.
Provides routes with GPS waypoints [and distance/duration data].
Waypoints are not "identified" :(

Current idea is to generate a regular 10x10 grid (100 locations) over Somerville/Cambridge.
Then, obtain WALKING directions for each combination (10,000 routes), and fuse the results.

