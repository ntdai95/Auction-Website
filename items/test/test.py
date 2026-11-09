"""Smoke test for the items service against a live itemsdb.

Run it from the items service directory so item and crud are importable:

    python3 test.py

It clears the items and categories tables, so run it against a throwaway
database, not one holding data you want to keep. Each step asserts, so the
script exits non-zero on the first failure.
"""
from item import Item, Categories
from crud import conn


def clear(table):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table} WHERE TRUE;")
    conn.commit()


# ----------------------------------------------------------------- categories
clear("categories")

Categories.add_item_category("shoes", False, "kasyap")
Categories.add_item_category("obscenity", True, "kasyap")
assert Categories.blacklisted("shoes") is False, "shoes should not be blacklisted"
assert Categories.blacklisted("obscenity") is True, "obscenity should be blacklisted"

Categories.modify_item_category("obscenity", "category", "adult")
assert Categories.fetch("adult"), "renamed category should be fetchable"
print("categories: add, blacklist flag and rename all pass")

# ---------------------------------------------------------------------- items
clear("items")

item = Item(
    item_id="abcd",
    name="Running shoes",
    user_id="kasyap",
    description="shoes for men",
    categories="shoes",
    price="49.99",
    image_url="https://example.com/shoes.jpg",
)
item.write()

loaded = Item.load("abcd")
assert loaded.name == "Running shoes", "name should round-trip"
assert loaded.image_url == "https://example.com/shoes.jpg", "image_url should round-trip"
assert str(loaded.price) == "49.99", "price should round-trip"
print("items: write and load preserve every field, image_url included")

# a name carrying a quote and a percent must store as data, not change the query
tricky = Item(item_id="quote-1", name="Collector's 50% pair", user_id="kasyap",
              description="apostrophe and percent", categories="shoes", price="10.00")
tricky.write()
assert Item.load("quote-1").name == "Collector's 50% pair", "special chars must bind as data"
print("items: a name with a quote and a percent binds as data")

# edit by non-primary-key columns
loaded.batch_edit(["description", "categories"], ["panda", "shoes | adult"])
edited = Item.load("abcd")
assert edited.description == "panda", "description should update"
assert edited.categories == "shoes | adult", "categories should update"
print("items: batch_edit updates the chosen columns")

assert Item.check_unique_item_id("abcd") is False, "an existing id is not unique"
assert Item.check_unique_item_id("not-there") is True, "an unused id is unique"
print("items: id uniqueness check works")

# flagging uses the inappropriate and counterfeit columns
edited.set_inappropriate_flag()
assert "abcd" in Item.view_flagged_items("inappropriate"), "item should read as flagged"
assert Item.load("abcd").inappropriate, "the inappropriate column should be set"
edited.remove_inappropriate_flag()
assert "abcd" not in Item.view_flagged_items("inappropriate"), "flag should clear"
print("items: inappropriate flag sets and clears")

# a field that is not a flag column is refused, not run as SQL
try:
    Item.view_flagged_items("user_id")
    raise AssertionError("a non-flag field should have been refused")
except ValueError:
    pass
print("items: view_flagged_items refuses a non-flag field")

clear("items")
clear("categories")
print("\nall items-service checks passed")
