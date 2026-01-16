import json
from pathlib import Path


from rag_pipeline.ingestion.preprocessing.cleaning.text_cleaner import clean_text

# --- Character discovery imports ---
from rag_pipeline.ingestion.preprocessing.ner_character_discovery.candidate_extractor import extract_person_candidates
from rag_pipeline.ingestion.preprocessing.ner_character_discovery.alias_clusterer import cluster_aliases
from rag_pipeline.ingestion.preprocessing.ner_character_discovery.canonical_builder import build_canonical_characters

def preprocess_novel(
    novel_path: str,
    novel_id: str,
    *,
    min_char_freq: int = 3,
    debug: bool = True,
    output_root: str = "clean_data"
):
    """
    Preprocessing pipeline (PHASE 1):

    - load novel
    - clean text
    - discover canonical characters
    - validate character coverage
    - persist clean artifacts to disk

    Returns:
        clean_text: str
        canonical_characters: dict
    """

    # ---------------- Load & clean ----------------
    print("Reading novel")
    raw_text = Path(novel_path).read_text(encoding="utf-8")
    print("cleaning started ")
    clean = clean_text(raw_text)
    print("cleaning finished")


    if debug:
        print(f"[DEBUG] Clean text length (chars): {len(clean)}")

    # ---------------- Character discovery ----------------

    print("character discovery started ")
    # name_counts = extract_person_candidates(
    #     clean,
    #     min_freq=min_char_freq
    # )
    # ran on collab ---- RAM issues
    print("Using precomputed PERSON counts (from Colab)")

    from collections import Counter
    # in search of castaways
    # name_counts = Counter({
    #     'Grant': 91,
    #     'Duncan': 201,
    #     'Jacques Paganel': 16,
    #     'Ayrton': 142,
    #     'Glenarvan': 766,
    #     'Lady Helena': 208,
    #     'MacNabb': 29,
    #     'Frith': 7,
    #     'Glasgow': 19,
    #     'John Mangles': 10,
    #     'Mangles': 233,
    #     'Lady Glenarvan': 25,
    #     'Tom Austin': 44,
    #     'Tom': 13,
    #     'Edward': 30,
    #     'Lady': 7,
    #     'Lord Glenarvan': 9,
    #     'Malcolm Castle': 19,
    #     'Pampas': 24,
    #     'Miss Grant': 12,
    #     'Robert': 254,
    #     'Robert Grant': 19,
    #     'Mary': 68,
    #     'Harry Grant': 39,
    #     'Mary Grant': 73,
    #     'Burton': 7,
    #     'Olbinett': 44,
    #     'John': 41,
    #     'Paganel': 194,
    #     'Wilson': 49,
    #     'Thalcave': 33,
    #     'Guamini': 9,
    #     'Austin': 13,
    #     'Thaouka': 27,
    #     'Manuel': 5,
    #     "O'Moore": 17,
    #     'Burke': 5,
    #     'Ben Joyce': 34,
    #     'Michael': 6,
    #     'Delegete': 7,
    #     'Snowy': 6,
    #     "Ben Joyce's": 8,
    #     'Macquarie': 24,
    #     'Halley': 5,
    #     'Will Halley': 12,
    #     'Kara-Tété': 11,
    #     'Maunganamu': 9,
    #     'Maria Theresa': 7
    # })
    # the count of monte cristo
    name_counts = Counter({'Cavalcanti': 71,
                 'Pharaon': 66,
                 'Marseilles': 38,
                 'Dantès': 676,
                 'M. Morrel': 90,
                 'Leclere': 15,
                 'Edmond': 172,
                 'M. Danglars': 68,
                 'Edmond Dantès': 44,
                 'Morrel': 454,
                 'Edmond’s': 25,
                 'Elba': 11,
                 'Mercédès': 241,
                 'Danglars': 54,
                 'Caderousse': 233,
                 'Ma': 30,
                 'Fernand': 16,
                 'Caderousse’s': 5,
                 'Porto-Ferrajo': 6,
                 'Villefort': 116,
                 'M. Villefort': 5,
                 'M. de Villefort': 16,
                 'Renée': 34,
                 'marquis': 13,
                 'Louis XVIII.': 27,
                 'Horace': 5,
                 'Blacas': 10,
                 'Louis XVIII': 10,
                 'M. de Blacas': 12,
                 'Bonaparte': 5,
                 'Tuscany': 7,
                 'Adieu': 16,
                 'M. de Saint-Méran': 17,
                 'Faria': 24,
                 'Dante': 6,
                 'Monte Cristo': 625,
                 'Jacopo': 40,
                 'La Jeune Amélie': 14,
                 'Genoa': 6,
                 'Beaucaire': 6,
                 'Rhône': 6,
                 'La Carconte': 14,
                 'Ali Pasha': 15,
                 'Rue du Helder': 5,
                 'Albert': 718,
                 'M. de Boville': 19,
                 'Emmanuel': 70,
                 'Julie': 65,
                 'Penelon': 8,
                 'Maximilian Morrel': 7,
                 'Maximilian': 189,
                 'Signor Pastrini': 41,
                 'Gaetano': 40,
                 'Ali': 132,
                 'Albert de Morcerf': 23,
                 'Morcerf': 180,
                 'Luigi': 26,
                 'Cucumetto': 34,
                 'Carlini': 11,
                 'Rita': 10,
                 'Diavolaccio': 5,
                 'Carmela': 9,
                 'Beppo': 10,
                 'Albert de\nMorcerf': 5,
                 'M. Franz': 21,
                 'Franz': 5,
                 'M. Bertuccio': 22,
                 'Bertuccio': 126,
                 'Corso': 6,
                 'Andrea': 253,
                 'M. de Morcerf': 34,
                 'M. Albert de Morcerf': 5,
                 'Debray': 166,
                 'Lucien': 32,
                 'Don Carlos': 9,
                 'Eugénie Danglars': 5,
                 'the Count of Morcerf': 6,
                 'Beauchamp': 13,
                 'Château-Renaud': 30,
                 'M. Beauchamp': 7,
                 'M. Debray': 21,
                 'Auteuil': 28,
                 'Abbé Busoni': 42,
                 'Assunta': 10,
                 'Benedetto': 65,
                 'Baptistin': 7,
                 'Lucien Debray': 7,
                 'Edward': 52,
                 'Valentine': 610,
                 'Eugénie': 49,
                 'Monte Cristo’s': 10,
                 'Mademoiselle Danglars': 23,
                 'Louise': 21,
                 'Mademoiselle Eugénie': 10,
                 'Madame Danglars': 7,
                 'Ali Tepelini': 15,
                 'Bartolomeo Cavalcanti': 8,
                 'Andrea Cavalcanti': 17,
                 'M. Cavalcanti': 25,
                 'M. Andrea Cavalcanti': 11,
                 'M. Andrea': 8,
                 'Barrois': 35,
                 'Mademoiselle Valentine': 10,
                 'Madeleine': 6,
                 'Vasiliki': 13,
                 'Selim': 19,
                 'Palikares': 6,
                 'Normandy': 5,
                 'Florentin': 7,
                 'Gutenberg': 10,
                 'License': 6,
                 'Project Gutenberg': 6})

    if debug:
        print(f"[DEBUG] PERSON candidates extracted: {len(name_counts)}")
        print(f"[DEBUG] Top 10 candidates: {name_counts.most_common(10)}")

    print("cluster alias called ")
    clusters = cluster_aliases(name_counts)

    if debug:
        print(f"[DEBUG] Alias clusters formed: {len(clusters)}")
        for i, (_, aliases) in enumerate(clusters.items()):
            if i >= 5:
                break
            print(f"[DEBUG] Cluster {i}: {list(aliases)}")

    canonical_characters = build_canonical_characters(
        name_counts,
        clusters
    )
    print("----------canonical_characters ----------")
    print(canonical_characters)

    # ---------------- Persist outputs ----------------
    print("saving started ")
    _persist_clean_outputs(
        novel_id=novel_id,
        clean_text_data=clean,
        canonical_characters=canonical_characters,
        output_root=output_root,
        debug=debug
    )

    return clean, canonical_characters


# ---------------------------------------------------------------------
# Internal persistence helper (DRY, reusable)
# ---------------------------------------------------------------------

def _persist_clean_outputs(
    *,
    novel_id: str,
    clean_text_data: str,
    canonical_characters: dict,
    output_root: str,
    debug: bool
):
    novel_dir = Path(output_root) / novel_id
    novel_dir.mkdir(parents=True, exist_ok=True)

    clean_text_path = novel_dir / f"{novel_id}.cleaned.txt"
    characters_path = novel_dir / f"{novel_id}.canonical_characters.json"

    clean_text_path.write_text(clean_text_data, encoding="utf-8")
    characters_path.write_text(
        json.dumps(canonical_characters, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


    if debug:
        print(f"[DEBUG] Output directory: {novel_dir.resolve()}")



