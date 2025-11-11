import pandas as pd
from django.conf import settings
from thefuzz import process, fuzz
import numpy as np

class SearchAgent:
    def __init__(self):
        self.df = None
        data_path = getattr(settings, "MEDICINE_DATA_PATH", None)
        if not data_path:
            print("SearchAgent ERROR: MEDICINE_DATA_PATH missing in settings.")
            return

        try:
            self.df = pd.read_csv(data_path, dtype={"EAN": str})
            self.df["EAN"] = self.df["EAN"].astype(str).str.strip()
            self.df["Name"] = self.df["Name"].astype(str).str.strip()
            self.name_list = self.df["Name"].tolist()
            print(f" Search Agent: Loaded {len(self.df)} medicines from {data_path}.")
        except Exception as e:
            print(f"SearchAgent ERROR loading CSV: {e}")

    # ---------------------------------------------------------------------
    def search(self, identifier, is_barcode=False):
        """Find medicine via barcode (exact) or name (fuzzy multi-stage)."""
        if self.df is None or not identifier:
            return None

        # 🔹 1️⃣ BARCODE SEARCH – exact match only
        if is_barcode:
            clean_id = str(identifier).strip()
            result = self.df[self.df["EAN"] == clean_id]
            return result.iloc[0].to_dict() if not result.empty else None

        # 🔹 2️⃣ TEXT SEARCH – fuzzy & token-based
        query = str(identifier).lower().strip()
        print(f"Rapid fuzzy triggered for query: {query}")

        # --- Phase 1: Direct QRatio match
        best_q = process.extractOne(query, self.name_list, scorer=fuzz.QRatio)
        if best_q and best_q[1] >= 85:
            print(f" QRatio matched: {best_q}")
            return self.df[self.df["Name"] == best_q[0]].iloc[0].to_dict()

        # --- Phase 2: Token set (handles word order / missing parts)
        best_t = process.extractOne(query, self.name_list, scorer=fuzz.token_set_ratio)
        if best_t and best_t[1] >= 80:
            print(f" TokenSet matched: {best_t}")
            return self.df[self.df["Name"] == best_t[0]].iloc[0].to_dict()

        # --- Phase 3: Weighted rescue matching (substring + loose ratio)
        print("Keyword Rescue triggered...")
        possible = []
        for name in self.name_list:
            n = name.lower()
            ratio = (
                fuzz.partial_ratio(query, n) * 0.6
                + fuzz.token_sort_ratio(query, n) * 0.4
            )
            if ratio > 70:
                possible.append((name, ratio))

        if possible:
            best = max(possible, key=lambda x: x[1])
            print(f"Weighted Rescue match: {best}")
            return self.df[self.df["Name"] == best[0]].iloc[0].to_dict()

        print(" No reliable match found.")
        return None

# ---------------------------------------------------------------------
# Wrapper for Django views
# ---------------------------------------------------------------------
search_agent_instance = SearchAgent()

def run_search_agent(query_text, is_barcode=False):
    """Exposes fuzzy search to Django views."""
    return search_agent_instance.search(query_text, is_barcode)
