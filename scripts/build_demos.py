# SPDX-License-Identifier: Apache-2.0
"""Build the GitHub Pages demos in every supported language.

Computes each demo's SliceData ONCE (the model output is language-independent) and
renders it in each language, plus a compact localized landing page. English lives at
docs/<file>.html; other languages at docs/<lang>/<file>.html.

    <jlens venv>/bin/python scripts/build_demos.py

Requires Anthropic's jlens + the public Qwen3.5-4B lens (see README). This is the
reproducer for the hosted demos; ordinary users do not need to run it.
"""
import os
import sys

import torch
import transformers
import jlens
from jlens.vis import compute_slice
from jlens.examples import EXAMPLES, resolve_prompt

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
from jlens_readable import build_readable_page
from jlens_readable.strings import UI_STRINGS, LANDING

MODEL = "Qwen/Qwen3.5-4B"
LENS_REPO, LENS_REV = "neuronpedia/jacobian-lens", "qwen-n1000"
LENS_FILE = "qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt"
DEVICE = "mps"

LANGS = ["en", "es", "fr", "zh", "am"]
LABEL = {"en": "English", "es": "Español", "fr": "Français", "zh": "中文", "am": "አማርኛ"}
DOCS = os.path.join(REPO, "docs")
PROMPT_BASE = "https://github.com/w4ester/jacobian-lens-readable/blob/main/prompts"

F = "Fact: In the U.S. state of Maryland, "
# (output filename, prompt, concept). First three come from jlens.examples.
_ex = {e.slug: e for e in EXAMPLES}


def ex_prompt(slug, tok):
    return resolve_prompt(_ex[slug], tok)


def demos(tok):
    return [
        ("multihop", ex_prompt("multihop", tok), "Italy"),
        ("overdose", ex_prompt("overdose-flag", tok), "overdose"),
        ("off-by-one", ex_prompt("off-by-one", tok), "index"),
        ("maryland-human-services",
         F + "food assistance and foster care are administered by the Department of", "Human"),
        ("maryland-mdot-disambiguation",
         "Fact: MDOT operates the Baltimore Metro and the Chesapeake Bay Bridge. "
         "MDOT is the transportation agency of the U.S. state of", "Maryland"),
    ]


def href(cur, tgt, fn):
    """Relative href from a page in language `cur` to the `tgt` version of file `fn`."""
    base = "" if cur == "en" else "../"
    tdir = "" if tgt == "en" else f"{tgt}/"
    return f"{base}{tdir}{fn}"


def alt_langs_for(cur, fn):
    return [(code, LABEL[code], href(cur, code, fn)) for code in LANGS]


_SWATCH = [("#b45309", "#fff"), ("#c2410c", "#fff"), ("#f59e0b", "#111"),
           ("#fcd34d", "#111"), ("#fef3c7", "#555"), ("#ffffff", "#767676")]


def esc(x):
    import html
    return html.escape(str(x))


def build_index(lang, files):
    """Compact localized landing page (English index is hand-built separately)."""
    L, U = LANDING[lang], UI_STRINGS[lang]
    d = U.get("dir", "ltr")
    swatches = "".join(
        f'<span class="sw" style="background:{bg};color:{fg}'
        f'{";border:1px solid #767676" if bg == "#ffffff" else ""}">{esc(lab)}</span>'
        for (bg, fg), lab in zip(_SWATCH, U["legend"]))
    nav = " · ".join(
        (f'<b lang="{c}">{esc(LABEL[c])}</b>' if c == lang
         else f'<a lang="{c}" href="{href(lang, c, "index.html")}">{esc(LABEL[c])}</a>')
        for c in LANGS)
    cards = "".join(
        f'<a class="card" href="{fn}"><h3>{esc(t)}</h3><p>{esc(desc)}</p></a>'
        for (t, desc), fn in zip(L["cards"], files))
    css = (
        ":root{color-scheme:light dark}"
        "body{font-family:-apple-system,Helvetica,Arial,sans-serif;max-width:860px;margin:40px auto;"
        "padding:0 20px;line-height:1.6;color:#111}"
        "h1{font-size:28px;margin:.2em 0}.tag{color:#4b5563;margin-top:0}"
        "h2{font-size:19px;margin-top:30px}a{color:#3b5bdb}"
        ".langnav{font-size:13px;color:#6b7280;margin-bottom:10px}"
        ".legend{background:#f7f7f7;border:1px solid #eee;border-radius:8px;padding:10px 14px;font-size:13px}"
        ".sw{display:inline-block;padding:1px 7px;border-radius:4px;margin:2px}"
        ".grid{display:grid;gap:14px;margin-top:14px}"
        ".card{display:block;border:1px solid #e5e5e5;border-radius:10px;padding:15px 18px;text-decoration:none;color:inherit}"
        ".card:hover,.card:focus-visible{border-color:#3b5bdb}.card h3{margin:0 0 4px;font-size:16px}"
        ".card p{margin:0;font-size:14px;color:#4b5563}"
        ".credit{margin-top:34px;padding-top:16px;border-top:1px solid #e5e5e5;font-size:13px;color:#6b7280}"
        "@media (prefers-reduced-motion: reduce){*{transition:none!important}}"
        "@media (prefers-color-scheme: dark){body{background:#0f1115;color:#e6e6e6}a{color:#7aa2ff}"
        ".tag,.card p,.credit{color:#9aa4b2}.legend{background:#171a21;border-color:#262b36}"
        ".card{background:#171a21;border-color:#262b36}h1,h2{color:#f3f4f6}}")
    return (
        f'<!doctype html><html lang="{lang}" dir="{d}"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{esc(L["h1"])}</title><style>{css}</style></head><body>'
        f'<nav class="langnav" aria-label="{esc(U["lang_nav"])}">{nav}</nav>'
        f'<h1>{esc(L["h1"])}</h1><p class="tag">{esc(L["tagline"])}</p>'
        f'<p>{esc(L["intro"])}</p>'
        f'<h2>{esc(L["howto_h"])}</h2>'
        f'<div class="legend">{U["how_to_read"]}<div style="margin-top:6px">{swatches}</div></div>'
        f'<h2>{esc(L["demos_h"])}</h2><p class="tag">{esc(L["demos_sub"])}</p>'
        f'<div class="grid">{cards}</div>'
        f'<h2>{esc(L["prompts_h"])}</h2><p>{esc(L["prompts_body"])} '
        f'<a href="{PROMPT_BASE}/{lang}.md">{esc(L["prompts_link"])}</a></p>'
        f'<p class="credit">{esc(L["credit"])}</p>'
        f'</body></html>')


def main():
    hf = None
    for name in ("AutoModelForImageTextToText", "AutoModelForCausalLM"):
        cls = getattr(transformers, name, None)
        if cls is None:
            continue
        try:
            hf = cls.from_pretrained(MODEL, dtype=torch.bfloat16).to(DEVICE); break
        except Exception as e:
            print(name, "failed:", e)
    if hf is None:
        raise RuntimeError("could not load " + MODEL)
    tok = transformers.AutoTokenizer.from_pretrained(MODEL)
    model = jlens.from_hf(hf, tok)
    lens = jlens.JacobianLens.from_pretrained(LENS_REPO, filename=LENS_FILE, revision=LENS_REV)
    print("[ready]", MODEL)

    files = [f"{fn}.html" for fn, _, _ in demos(tok)]
    for fn, prompt, concept in demos(tok):
        ids = tok.encode(" " + concept, add_special_tokens=False)
        cid = ids[0] if len(ids) == 1 else None
        sd = compute_slice(model, lens, prompt, top_n=10, mask_display=True,
                           pinned_token_ids={cid} if cid else None, layer_stride=2)
        for lang in LANGS:
            page = build_readable_page(
                sd, prompt=prompt, n_layers=model.n_layers, concept=concept,
                concept_id=cid, model_name="Qwen3.5-4B", lang=lang,
                alt_langs=alt_langs_for(lang, f"{fn}.html"))
            out = os.path.join(DOCS, f"{fn}.html") if lang == "en" \
                else os.path.join(DOCS, lang, f"{fn}.html")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, "w", encoding="utf-8").write(page)
        print(f"  {fn:34s} x {len(LANGS)} langs  (concept {concept!r})")

    # localized landing pages (English index.html is hand-built)
    for lang in LANGS:
        if lang == "en":
            continue
        out = os.path.join(DOCS, lang, "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(build_index(lang, files))
        print(f"  index.html for {lang}")
    print("Done.")


if __name__ == "__main__":
    main()
