"""Create a new collection."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime
from getpass import getuser

from dotenv import load_dotenv

from raindropiopy import API, Collection

load_dotenv()

with API(os.environ["RAINDROP_TOKEN"]) as api:
    title = f"TEST Collection ({getuser()}@{datetime.now():%Y-%m-%dT%H:%M:%S})"
    print(f"Creating collection: '{title}'...", flush=True, end="")
    try:
        collection = Collection.create(api, title=title)
        print(f"Done, {collection.id=}.")
    except Exception as exc:
        print(f"Sorry, unable to create collection! {exc}")
        sys.exit(1)

    # If you want to actually *see* the new collection, comment this
    # section out and look it up through any Raindrop mechanism (ie.
    # app, url etc.); otherwise, we clean up after ourselves.
    print(f"Removing collection: '{title}'...", flush=True, end="")
    Collection.delete(api, id=collection.id)
    print("Done.")
