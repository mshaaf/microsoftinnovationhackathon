# R11: ZIP to county

Checked 2026-09-23.

## Answer
Use the Census **2020 ZCTA5 to County relationship file**:
`https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_county20_natl.txt`

- Pipe-delimited, UTF-8 with a BOM (open with `encoding="utf-8-sig"`), 6.8 MB.
- Columns used: `GEOID_ZCTA5_20` (ZIP), `GEOID_COUNTY_20` (5-digit state+county FIPS), `NAMELSAD_COUNTY_20` (for example "Hawaii County"), `AREALAND_PART` (land area of the overlap).
- Skip rows with an empty `GEOID_ZCTA5_20`. These are county-only rows.
- 33,791 ZCTAs, and 10,186 of them touch more than one county. Most of those are slivers.
- State abbreviation comes from the first 2 FIPS digits (map is in the script).

**Primary county** = largest `AREALAND_PART`. **Multi-county rule:** keep counties with at least 5% of the ZCTA's land area, sorted by share. `needs_confirmation = len(kept) > 1`. Put the 5% in one named constant.

**Bundle:** `scripts/build_zip_county.py` downloads the file and writes `data/geo/zip_county.json` as `{"96704": [["15","001","Hawaii County",1.0]], ...}`. That's about 1.5 MB, under the 5 MB limit. Commit the output, not the raw file.

**Limitation (show on About):** ZCTAs approximate USPS ZIP codes. PO-box-only ZIPs and new ZIPs may be missing, so we return `zip_not_found` with a hint to call 211.

Verified examples: 96704 and 96740 map only to Hawaii County (15001). 39426 maps to Pearl River 90% and Hancock 10%, so it needs confirmation. 00601 maps to Adjuntas PR (the leading-zero test; the Utuado sliver is 1%, so it gets dropped). 02134 maps only to Suffolk MA.

Azure Maps: skip. It's optional, the file is exact enough, and it's one fewer key.

## Evidence
- https://www.census.gov/geographies/reference-files/time-series/geo/relationship-files.2020.html
- File downloaded and parsed 2026-09-23.

## Impact
P1-01. ARCHITECTURE.md geo row. Leave `AZURE_MAPS_KEY` out of .env.example.
