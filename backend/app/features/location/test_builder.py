from scripts.build_zip_county import read_zip_map


def test_builder_reads_bom_pipe_file_and_applies_five_percent_rule(tmp_path):
    source = tmp_path / "census.txt"
    source.write_text(
        "\ufeffGEOID_ZCTA5_20|GEOID_COUNTY_20|NAMELSAD_COUNTY_20|AREALAND_PART\n"
        "00001|01001|County A|901\n"
        "00001|01003|County B|50\n"
        "00001|01005|County C|49\n"
        "|01007|County-only row|1000\n",
        encoding="utf-8",
    )

    result = read_zip_map(source)

    assert result["00001"] == [
        ["01", "001", "County A", 0.901],
        ["01", "003", "County B", 0.05],
    ]
    assert "" not in result
    assert result["_metadata"]["version"] == "2020"
    assert result["_metadata"]["source"].endswith("tab20_zcta520_county20_natl.txt")
