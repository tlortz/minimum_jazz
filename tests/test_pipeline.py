from jazz.data import generate, generate_xml
from jazz.pipeline import to_bronze, to_silver, parse_xml

from pathlib import Path

def test_to_bronze(tmpdir, spark):
    path = str(tmpdir)
    raw_path = path + "/raw"
    generate(raw_path, 3)
    bronze_df = to_bronze(spark, raw_path)
    bronze_df.show()
    schema = bronze_df.schema.fieldNames()
    assert(len(schema) == 1)
    assert(schema[0] == "value")
    assert(bronze_df.count() == 3)


def test_to_silver(tmpdir, spark):
    path = str(tmpdir)
    raw_path = path + "/raw"
    generate(raw_path, 3)
    bronze_df = to_bronze(spark, raw_path)
    silver_df = to_silver(spark, bronze_df)
    fields = silver_df.schema.fieldNames()
    print(fields)
    assert("value" in fields)
    assert("message" in fields)
    silver_df.show()


def test_parse_xml():
    xml_string = generate_xml()
    values = parse_xml(xml_string)
    print(values)
    assert("SUBJECT" in values.keys())
    assert("BODY" in values.keys())
    subject = values.get("SUBJECT")
    assert(len(subject) > 10)