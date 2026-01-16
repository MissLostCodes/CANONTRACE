from collections import defaultdict

def cluster_aliases(name_counts):
    """
    name_counts: Counter { "Edmond Dantès": 120, "Dantès": 300, "Edmond": 90 }

    Returns:
    {
      "Edmond Dantès": ["Edmond", "Dantès", "Edmond Dantès"]
    }
    """
    print("cluster_aliases called ")
    clusters = defaultdict(set)
    names = list(name_counts.keys())

    for name in names:
        parts = name.lower().split()
        last = parts[-1]

        for other in names:
            other_parts = other.lower().split()

            if (
                last in other_parts
                or any(p in other_parts for p in parts)
            ):
                clusters[last].add(name)
                clusters[last].add(other)

    return clusters
