import json

INPUT_FILE = "mysite_data.json"
OUTPUT_FILE = "mysite_data_clean.json"

EXCLUDE_MODELS = {
    "contenttypes.contenttype",
    "auth.permission",
    "admin.logentry",
    "sessions.session",
}


def clean_fixture(input_path: str, output_path: str) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_data = [obj for obj in data if obj.get("model") not in EXCLUDE_MODELS]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Cleaned fixture saved to {output_path}. Removed {len(data) - len(cleaned_data)} system records.")


if __name__ == "__main__":
    clean_fixture(INPUT_FILE, OUTPUT_FILE)
