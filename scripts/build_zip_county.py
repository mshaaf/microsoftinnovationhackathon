"""Build the bundled Census 2020 ZCTA-to-county lookup."""

import csv
import io
import json
from collections import defaultdict
from pathlib import Path
from urllib.request import urlopen

SOURCE_URL = (
    "https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/"
    "tab20_zcta520_county20_natl.txt"
)
MIN_LAND_SHARE = 0.05
STATE_ABBREVIATIONS = {
    "01": "AL",
    "02": "AK",
    "04": "AZ",
    "05": "AR",
    "06": "CA",
    "08": "CO",
    "09": "CT",
    "10": "DE",
    "11": "DC",
    "12": "FL",
    "13": "GA",
    "15": "HI",
    "16": "ID",
    "17": "IL",
    "18": "IN",
    "19": "IA",
    "20": "KS",
    "21": "KY",
    "22": "LA",
    "23": "ME",
    "24": "MD",
    "25": "MA",
    "26": "MI",
    "27": "MN",
    "28": "MS",
    "29": "MO",
    "30": "MT",
    "31": "NE",
    "32": "NV",
    "33": "NH",
    "34": "NJ",
    "35": "NM",
    "36": "NY",
    "37": "NC",
    "38": "ND",
    "39": "OH",
    "40": "OK",
    "41": "OR",
    "42": "PA",
    "44": "RI",
    "45": "SC",
    "46": "SD",
    "47": "TN",
    "48": "TX",
    "49": "UT",
    "50": "VT",
    "51": "VA",
    "53": "WA",
    "54": "WV",
    "55": "WI",
    "56": "WY",
    "60": "AS",
    "66": "GU",
    "69": "MP",
    "72": "PR",
    "78": "VI",
}


def build_zip_map(rows):
    grouped = defaultdict(dict)
    for row in rows:
        zip_code = (row.get("GEOID_ZCTA5_20") or "").strip()
        if not zip_code:
            continue
        county_fips = (row["GEOID_COUNTY_20"] or "").strip()
        state_fips = county_fips[:2]
        if len(county_fips) != 5 or state_fips not in STATE_ABBREVIATIONS:
            raise ValueError(f"invalid county FIPS: {county_fips!r}")
        county = grouped[zip_code].setdefault(
            county_fips, [0, row["NAMELSAD_COUNTY_20"].strip()]
        )
        county[0] += int(row["AREALAND_PART"] or 0)

    result = {
        "_metadata": {
            "source": SOURCE_URL,
            "version": "2020",
            "state_fips_to_abbreviation": STATE_ABBREVIATIONS,
        }
    }
    for zip_code, counties in grouped.items():
        total_area = sum(area for area, _ in counties.values())
        if total_area <= 0:
            continue
        kept = [
            [fips[:2], fips[2:], name, round(area / total_area, 6)]
            for fips, (area, name) in counties.items()
            if area / total_area >= MIN_LAND_SHARE
        ]
        kept.sort(key=lambda county: (-county[3], county[0], county[1]))
        result[zip_code] = kept
    return result


def read_zip_map(source_path):
    with source_path.open(encoding="utf-8-sig", newline="") as source:
        return build_zip_map(csv.DictReader(source, delimiter="|"))


def main():
    with (
        urlopen(SOURCE_URL, timeout=60) as response,
        io.TextIOWrapper(response, encoding="utf-8-sig", newline="") as source,
    ):
        bundle = build_zip_map(csv.DictReader(source, delimiter="|"))

    output = Path(__file__).resolve().parents[1] / "data" / "geo" / "zip_county.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(bundle, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    print(
        f"Wrote {len(bundle) - 1:,} ZIPs to {output} ({output.stat().st_size:,} bytes)"
    )


if __name__ == "__main__":
    main()
