from backend.app.utils.symspell_imp import spell_correct, load_symspell
from backend.app.utils.textblob_imp import spell_correct_textblob


def optimize_query(text: str):
    # 1. Fast spell check
    sym_spell = load_symspell()
    text = spell_correct(sym_spell, text)

    # 2. Optional grammar fix
    #text = spell_correct_textblob(text)

    return text


if __name__ == "__main__":

    test_query = "Documents required for HUF account opening"
    optimized_query = optimize_query(test_query)
    print(f"Original Query: {test_query}")
    print(f"Optimized Query: {optimized_query}")
    # Expected output: "This is a sample query with some spelling errors."

