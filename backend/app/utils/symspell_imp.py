import importlib

from symspellpy.symspellpy import SymSpell, Verbosity

def load_symspell(max_edit_distance=2, prefix_length=7):
    sym_spell = SymSpell(max_edit_distance, prefix_length)
    dictionary_path = importlib.resources.files("symspellpy") / "frequency_dictionary_en_82_765.txt"
    sym_spell.load_dictionary(str(dictionary_path), 0, 1)
    sym_spell.load_dictionary("../resources/custom_symspell_dictionary.txt", term_index=0, count_index=1)

    return sym_spell

def spell_correct(sym_spell, input_text):
    suggestions = sym_spell.lookup_compound(input_text, max_edit_distance=2)
    return suggestions[0].term if suggestions else input_text
