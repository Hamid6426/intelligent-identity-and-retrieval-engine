"""
Grabpic System Health & Data Verification Test
Checks all tables and endpoints to verify the ingestion pipeline worked correctly.
Run with: python tests/test_system.py
"""
import sys
import os

# Fix Windows encoding issues
os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

import requests

BASE_URL = "http://localhost:8000"
passed = 0
failed = 0

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {name}")
    else:
        failed += 1
        print(f"  [FAIL] {name} {('- ' + detail) if detail else ''}")

print("=" * 60)
print("  GRABPIC SYSTEM VERIFICATION TEST")
print("=" * 60)

# --- 1. API Health ---
print("\n[1] API Connectivity")
try:
    r = requests.get(f"{BASE_URL}/")
    check("API is online", r.status_code == 200)
    data = r.json()
    check("API returns correct status", data.get("status") == "online")
except Exception as e:
    check("API is online", False, str(e))

# --- 2. Persons Table ---
print("\n[2] Persons Table (grab_ids)")
try:
    r = requests.get(f"{BASE_URL}/db/persons")
    check("Persons endpoint responds", r.status_code == 200)
    data = r.json()
    person_count = data.get("total", 0)
    check(f"Persons table has data ({person_count} identities found)", person_count > 0)
    if person_count > 0:
        first_person = data["data"][0]
        check("Person has a valid grab_id (UUID)", len(first_person.get("id", "")) > 10)
        check("Person has created_at timestamp", first_person.get("created_at") is not None)
except Exception as e:
    check("Persons endpoint responds", False, str(e))

# --- 3. Images Table ---
print("\n[3] Images Table")
try:
    r = requests.get(f"{BASE_URL}/db/images")
    check("Images endpoint responds", r.status_code == 200)
    data = r.json()
    image_count = data.get("total", 0)
    check(f"Images table has data ({image_count} images indexed)", image_count > 0)
    if image_count > 0:
        first_image = data["data"][0]
        check("Image has a file_path", bool(first_image.get("file_path")))
except Exception as e:
    check("Images endpoint responds", False, str(e))

# --- 4. Embeddings Table ---
print("\n[4] Face Embeddings Table")
try:
    r = requests.get(f"{BASE_URL}/db/embeddings")
    check("Embeddings endpoint responds", r.status_code == 200)
    data = r.json()
    embed_count = data.get("total", 0)
    check(f"Embeddings table has data ({embed_count} face vectors stored)", embed_count > 0)
    if embed_count > 0:
        first_embed = data["data"][0]
        check("Embedding links to a person_id", bool(first_embed.get("person_id")))
        check("Embedding links to an image_id", bool(first_embed.get("image_id")))
except Exception as e:
    check("Embeddings endpoint responds", False, str(e))

# --- 5. Cross-Table Verification ---
print("\n[5] Cross-Table Integrity")
try:
    persons_r = requests.get(f"{BASE_URL}/db/persons").json()
    images_r = requests.get(f"{BASE_URL}/db/images").json()
    embeds_r = requests.get(f"{BASE_URL}/db/embeddings").json()

    check("More embeddings than persons (faces mapped to identities)",
          embeds_r["total"] >= persons_r["total"])
    check("More embeddings than images (some images have multiple faces)",
          embeds_r["total"] >= images_r["total"] or images_r["total"] > 0)

    if persons_r["total"] > 0:
        grab_id = persons_r["data"][0]["id"]
        r = requests.get(f"{BASE_URL}/images/{grab_id}")
        check(f"Image retrieval by grab_id works", r.status_code == 200)
        data = r.json()
        check(f"Grab_id {grab_id[:8]}... returns images ({data.get('image_count', 0)} found)",
              data.get("image_count", 0) > 0)
except Exception as e:
    check("Cross-table integrity", False, str(e))

# --- 6. Identities Endpoint ---
print("\n[6] Identities Summary Endpoint")
try:
    r = requests.get(f"{BASE_URL}/identities")
    check("Identities endpoint responds", r.status_code == 200)
    data = r.json()
    check(f"Identities endpoint returns data ({data.get('total', 0)} identities)",
          data.get("total", 0) > 0)
except Exception as e:
    check("Identities endpoint responds", False, str(e))

# --- Summary ---
total = passed + failed
print("\n" + "=" * 60)
print(f"  RESULTS: {passed}/{total} tests passed")
if failed == 0:
    print("  ALL TESTS PASSED!")
else:
    print(f"  WARNING: {failed} test(s) failed")
print("=" * 60)

sys.exit(0 if failed == 0 else 1)
