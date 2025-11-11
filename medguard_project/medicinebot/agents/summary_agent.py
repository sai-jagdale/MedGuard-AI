import ollama
import markdown
import pandas as pd
from django.conf import settings


class SummaryAgent:
    def _get_context_from_df(self, search_results_dict_or_df):
        """Extract reliable data from DataFrame or dict."""
        if isinstance(search_results_dict_or_df, dict):
            row = search_results_dict_or_df
        elif isinstance(search_results_dict_or_df, pd.DataFrame) and not search_results_dict_or_df.empty:
            row = search_results_dict_or_df.iloc[0].to_dict()
        else:
            return "No relevant data found in the database.", "Unknown Medicine"

        db_data = {
            "Name": row.get("Name", "Not Found"),
            "Type": row.get("Type", "Not Found"),
            "Ingredients": row.get("Content", "Not Found"),
            "Uses": row.get("Uses", "Not Found"),
            "Side Effects": row.get("Side Effects", "Not Found"),
        }

        context = "\n".join(
            [f"{k}: {v}" for k, v in db_data.items() if v and v != "Not Found"]
        )
        return context, db_data["Name"]

    # ----------------------------------------------------------
    def _generate_summary(self, db_context, medicine_name, extracted_data=None, is_barcode=False):
        """Unified summary generator for both OCR and barcode."""
        is_legal = not ("No relevant data found" in db_context or not db_context)
        legal_status = (
            "✅ Legal Status: Legal"
            if is_legal
            else "⚠️ Legal Status: Not Legal in India"
        )

        warning_md = ""
        if extracted_data and extracted_data.get("Is Expired", False):
            warning_md = f"🚨 WARNING: Expired medicine detected (Expiry Date: {extracted_data['Expiry Date']}). DO NOT USE.\n\n"

        # 🩶 Handle unknown medicine fallback quickly
        if not is_legal:
            return markdown.markdown(
                f"### {medicine_name}\n\n{legal_status}\n"
            )

        # 🧠 AI summary for known medicine
        full_context = f"""
        NAME: {medicine_name}
        DATABASE DATA: {db_context}
        IMAGE/BARCODE DATA: {extracted_data if extracted_data else 'N/A'}
        """

        prompt = f"""
        You are MedGuard AI’s summarizer.
        Generate a structured and neat medical summary using the provided data.
        Each line should be compact (1–2 short sentences).
        Do not bold keywords, do not use multiple emojis or end-of-line icons.
        Keep layout clean and factual.

        CONTEXT:
        {full_context}

        Format (exactly this order):
        📜 MFG Date: <short factual line or 'Not Found'>
        ⏳ Expiry Date: <short factual line or 'Not Found'>
        💰 MRP: <short factual line or 'Not Found'>
        💊 Type: <concise 1–2 sentence description>
        🌿 Ingredients: <concise 1–2 sentence summary of components>
        💗 Uses: <concise 1–2 sentence summary of medical use>
        ⚠️ Side Effects: <concise 1–2 sentence summary of possible side effects>
        """

        response = ollama.chat(model="phi3", messages=[{"role": "user", "content": prompt}])
        ai_md = response["message"]["content"]

        # 🧹 Clean markdown noise and formatting
        cleaned_md = (
            ai_md.replace("**", "")
            .replace("✅", "")
            .replace("⚠️⚠️", "⚠️")
            .replace("##", "")
            .replace("###", "")
            .replace("*", "")
            .strip()
        )

        return markdown.markdown(
            f"### {medicine_name}\n\n{legal_status}\n\n{warning_md}{cleaned_md}"
        )

    # ----------------------------------------------------------
    def generate_ocr_summary(self, search_results, extracted_data):
        """Generate structured, detailed OCR summary."""
        db_context, medicine_name = self._get_context_from_df(search_results)
        return self._generate_summary(db_context, medicine_name, extracted_data, is_barcode=False)

    def generate_barcode_summary(self, search_results):
        """Generate structured, detailed summary for barcode data."""
        db_context, medicine_name = self._get_context_from_df(search_results)
        return self._generate_summary(db_context, medicine_name, extracted_data=None, is_barcode=True)


# ----------------------------------------------------------
# ✅ FUNCTION WRAPPER for Django views
# ----------------------------------------------------------

summary_agent_instance = SummaryAgent()

def run_summary_agent(search_results, extracted_data, is_barcode=False):
    """Unified public entry point."""
    if is_barcode:
        return summary_agent_instance.generate_barcode_summary(search_results)
    else:
        return summary_agent_instance.generate_ocr_summary(search_results, extracted_data)
