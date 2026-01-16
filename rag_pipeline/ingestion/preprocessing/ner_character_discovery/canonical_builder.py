import re

def normalize_id(name: str) -> str :
    print("normalize_id called ")
    name = name.lower()
    name = re.sub(r"[^a-z\s]", "", name)
    return "_".join(name.split())


def build_canonical_characters(name_counts, clusters):
    """
    Returns:
    {
      "edmond_dantes": {
          "canonical_name": "Edmond Dantès",
          "aliases": ["Edmond", "Dantès", "Edmond Dantès"]
      }
    }
    """
    print("build_canonical_characters called ")
    canonical_map = {}

    for _, names in clusters.items():
        # pick longest + most frequent
        canonical_name = max(
            names,
            key=lambda n: (len(n.split()), name_counts.get(n, 0))
        )

        canonical_id = normalize_id(canonical_name)

        canonical_map[canonical_id] = {
            "canonical_name": canonical_name,
            "aliases": sorted(names)
        }

    return canonical_map
