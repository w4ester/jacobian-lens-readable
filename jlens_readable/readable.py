# SPDX-License-Identifier: Apache-2.0
"""A legible, accessible, multilingual, dependency-free view for the Jacobian Lens.

The upstream repo ships one visualization: a dense, researcher-oriented d3 grid of
tiny per-cell tokens. It answers a researcher's questions well, but a newcomer or a
classroom cannot read it, and a screen-reader user cannot use it at all.

This module renders the *same* ``jlens.vis.SliceData`` as a plain HTML table you
can read at a glance, and that a screen reader or braille display can read too:

  * rows    = the words of the prompt (reading order, top to bottom)
  * columns = the model's layers, left to right, with the real OUTPUT on the right
  * cell    = the top word that (position, layer) leans toward
  * colour  = how highly the cell ranks a concept you choose to track, in six
              log-spaced buckets (darker = higher). The rank is ALSO printed as
              text in every meaningful cell, so colour is never the only signal.

Accessibility: real table semantics (``<caption>``, ``<thead>``/``<tbody>``,
``<th scope>``), a plain-language "Key finding" that a blind user hears first, a
keyboard-focusable scroll region, WCAG-checked contrast, and a ``lang``/``dir``
aware document. It is pure Python (only the standard-library ``html`` module),
adds no dependencies, and emits a single self-contained HTML string: no d3, no
JavaScript, e-mailable, works from ``file://``.

Localization: fixed chrome (labels, callout, legend, how-to-read) flows through
``UI_STRINGS`` (see ``strings.py``) so it can be translated by passing ``lang=``
or ``ui_strings=``. The model's own token output is never translated.

The science is entirely Anthropic's: "Verbalizable Representations Form a Global
Workspace in Language Models" (https://transformer-circuits.pub/2026/workspace).
This is only a rendering layer.
"""
from __future__ import annotations

import html

from jlens_readable.strings import UI_STRINGS

#: The ``SliceData`` fields this renderer reads. Upstream is a frozen reference
#: implementation, so this is effectively a stable contract.
_SLICEDATA_FIELDS = (
    "seq_len", "layers", "context_token_strs", "top_ids", "rank_tensor",
    "tracked_token_ids", "vocab_fragment", "vocab_size", "ctx_offset",
)

#: (background, text) for each rank bucket, WCAG-checked against its text colour.
_BUCKETS = [
    ("#b45309", "#ffffff"),  # rank 0, top choice
    ("#c2410c", "#ffffff"),  # <= 4, top 5   (darkened from #ea580c for 4.5:1)
    ("#f59e0b", "#111111"),  # <= 19, top 20
    ("#fcd34d", "#111111"),  # <= 99, top 100
    ("#fef3c7", "#555555"),  # <= 999, top 1000
    ("#ffffff", "#767676"),  # else, not close (grey passes 4.5:1 on white)
]


def _clean(s: str, cap: int = 12) -> str:
    """Trim, escape, and cap a token string for display (newline -> ⏎ marker)."""
    nl = "⏎"
    s = s.replace("\n", nl).strip()
    if len(s) > cap:
        s = s[:cap] + "…"
    if not s:
        return "·"
    esc = html.escape(s)
    if nl in esc:  # give the newline glyph an accessible name
        esc = esc.replace(nl, f'<span aria-hidden="true">{nl}</span>'
                              f'<span class="sr-only"> (newline) </span>')
    return esc


def _bucket(rank: int) -> int:
    """0-indexed rank -> bucket index into _BUCKETS."""
    if rank < 0:     return 5
    if rank == 0:    return 0
    if rank <= 4:    return 1
    if rank <= 19:   return 2
    if rank <= 99:   return 3
    if rank <= 999:  return 4
    return 5


def _legend(labels) -> str:
    return "".join(
        f'<span class="lg" style="background:{bg};color:{fg}'
        f'{";border:1px solid #767676" if bg == "#ffffff" else ""}">{html.escape(lab)}</span>'
        for (bg, fg), lab in zip(_BUCKETS, labels)
    )


_CSS = """
body{font-family:-apple-system,Helvetica,Arial,sans-serif;margin:22px;color:#111}
main{display:block}
h1{font-size:20px;margin:0 0 6px}
.langnav{font-size:12px;margin:0 0 10px;color:#6b7280}
.langnav a{color:#3b5bdb} .langnav a:focus-visible{outline:2px solid #1e40af;outline-offset:2px}
.sub{color:#3f3f3f;font-size:13px;margin:0 0 10px;max-width:940px;line-height:1.55}
.chip{display:inline-block;background:#b45309;color:#fff;font-size:12px;font-weight:600;padding:2px 9px;border-radius:11px}
.key{font-size:14px;background:#fff7ed;border-left:4px solid #c2410c;padding:9px 13px;margin:11px 0;max-width:940px;line-height:1.5}
.note{font-size:13px;background:#f3f4f6;border-left:4px solid #6b7280;padding:8px 12px;margin:11px 0;max-width:940px}
.legend{margin:9px 0;font-size:12px;color:#3f3f3f} .lg{display:inline-block;padding:2px 8px;margin:0 4px 4px 0;border-radius:4px}
.fine{color:#6b7280;font-size:11px;margin-top:8px} .fine a{color:#3b5bdb}
.wrap{overflow:auto;border:1px solid #d1d5db;max-height:78vh}
.wrap:focus-visible{outline:3px solid #1e40af;outline-offset:2px}
table{border-collapse:collapse;font-size:12px}
caption{text-align:left}
th,td{border:1px solid #e5e5e5}
.corner{font-size:11px;color:#4b5563;font-weight:normal;padding:4px 6px;position:sticky;left:0;top:0;z-index:3;background:#f3f4f6;text-align:left}
.lyr{font-size:11px;color:#4b5563;font-weight:normal;padding:5px 7px;background:#f3f4f6;position:sticky;top:0;z-index:2;text-align:center}
.lyr.out{color:#111;font-weight:bold;border-left:2px solid #6b7280}
.tok{font-family:ui-monospace,Menlo,monospace;font-size:11px;padding:4px 8px;background:#f3f4f6;position:sticky;left:0;z-index:1;white-space:nowrap;text-align:left;font-weight:normal}
.tok.tgt{background:#1e40af;color:#fff} .tok .pn{color:#4b5563;margin-right:6px;font-size:10px} .tok.tgt .pn{color:#c7d2fe}
.cell{min-width:56px;max-width:96px;height:32px;padding:2px 4px;text-align:center;vertical-align:middle}
.cell.out{border-left:2px solid #6b7280}
.cell .w{display:block;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;line-height:1.1}
.cell .sup{display:block;font-size:10px;font-weight:400;line-height:1}
.cell.peak{outline:3px solid #1e40af;outline-offset:-3px}
.cell.peak .pk{display:block;font-size:9px;font-weight:700;background:#1e40af;color:#fff;border-radius:3px;padding:0 4px;margin:1px auto 0;width:max-content;line-height:1.45;letter-spacing:.02em}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0}
@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important}}
@media (forced-colors: active){.cell.peak,.tok.tgt{outline:3px solid Highlight}}
"""

_CREDIT = (
    'Rendered with <a href="https://github.com/w4ester/jacobian-lens-readable">'
    'jacobian-lens-readable</a> · method: Anthropic Jacobian Lens '
    '(<a href="https://transformer-circuits.pub/2026/workspace">paper</a> · '
    '<a href="https://github.com/anthropics/jacobian-lens">code</a>) · lens fitted by '
    '<a href="https://huggingface.co/neuronpedia/jacobian-lens">Neuronpedia</a>'
)


def build_readable_page(
    slice_data,
    *,
    prompt: str,
    n_layers: int,
    concept: str = "",
    concept_id: int | None = None,
    model_name: str = "the model",
    layer_step: int = 1,
    lang: str = "en",
    ui_strings: dict | None = None,
    alt_langs: list | None = None,
) -> str:
    """Render a ``jlens.vis.SliceData`` into a self-contained, accessible HTML page.

    Args:
        slice_data: A ``SliceData`` from ``jlens.vis.compute_slice``.
        prompt: The prompt text (shown in the header).
        n_layers: ``model.n_layers``; used to label the final/output column.
        concept: A word to track and colour by (e.g. ``"Italy"``). When empty or
            untracked, the page renders the top word per cell without a heat-map.
        concept_id: The token id of ``concept``. It must be in
            ``slice_data.tracked_token_ids`` for the colouring to appear; pass it
            to ``compute_slice`` via ``pinned_token_ids`` to guarantee that.
        model_name: Display label for the model (e.g. ``"Qwen3.5-4B"``).
        layer_step: Render every Nth layer to keep columns on one screen; the
            final layer and the concept's peak layer are always included.
        lang: BCP-47 code for the fixed chrome (``"en"``, ``"es"``, ...). Sets the
            document ``lang``/``dir`` and picks a ``UI_STRINGS`` entry.
        ui_strings: Optional per-call overrides merged on top of the language dict.
        alt_langs: Optional list of ``(code, label, href)`` for a language switcher
            nav. The entry whose code == ``lang`` renders as bold, others as links.

    Returns:
        A single self-contained HTML document as a string (no JS, no assets).
    """
    sd = slice_data
    s = {**UI_STRINGS["en"], **UI_STRINGS.get(lang, {}), **(ui_strings or {})}
    esc_concept = html.escape(concept)
    final = n_layers - 1
    vocab = {int(k): v for k, v in sd.vocab_fragment.items()}
    tracked = concept_id is not None and concept_id in sd.tracked_token_ids
    track_idx = sd.tracked_token_ids.index(concept_id) if tracked else None

    def rank_at(pos: int, li: int) -> int:
        return int(sd.rank_tensor[pos, li, track_idx]) if tracked else -1

    col_lis = list(range(0, len(sd.layers), max(1, layer_step)))
    fin_li = sd.layers.index(final) if final in sd.layers else len(sd.layers) - 1
    if fin_li not in col_lis:
        col_lis.append(fin_li)

    best = None  # (rank, layer_index, pos)
    if tracked:
        for pos in range(sd.seq_len):
            for li in range(len(sd.layers)):
                r = rank_at(pos, li)
                if r >= 0 and (best is None or r < best[0]):
                    best = (r, li, pos)
    if best and best[1] not in col_lis:
        col_lis.append(best[1])
    col_lis = sorted(set(col_lis))

    # --- table head: real column headers with scope + screen-reader layer names
    head = [f'<th class="corner" scope="col">{html.escape(s["corner"])}</th>']
    for li in col_lis:
        layer = sd.layers[li]
        if layer == final:
            head.append(f'<th class="lyr out" scope="col">{html.escape(s["col_output"])}</th>')
        else:
            head.append(f'<th class="lyr" scope="col"><span aria-hidden="true">L{layer}</span>'
                        f'<span class="sr-only">{html.escape(s["col_layer"].format(n=layer))}</span></th>')
    thead = f'<thead><tr>{"".join(head)}</tr></thead>'

    # --- table body
    rows = []
    for pos in range(sd.seq_len):
        tgt = bool(best) and pos == best[2]
        tok = _clean(sd.context_token_strs[sd.ctx_offset + pos], cap=16)
        cells = [f'<th class="tok{" tgt" if tgt else ""}" scope="row">'
                 f'<span class="pn">{sd.ctx_offset + pos}</span><bdi>{tok}</bdi></th>']
        for li in col_lis:
            tid = int(sd.top_ids[pos, li, 0])
            word = _clean(vocab.get(tid, "?"))
            rank = rank_at(pos, li)
            bg, fg = _BUCKETS[_bucket(rank)]
            # rank as TEXT in every meaningful cell (0..999), so colour is never
            # the only signal (colourblind, grayscale, braille, forced-colors).
            sup = f'<span class="sup">#{rank + 1}</span>' if 0 <= rank <= 999 else ""
            peak = bool(best) and li == best[1] and pos == best[2]
            peak_mark = (f'<span class="pk">{html.escape(s["peak_label"])}</span>'
                         f'<span class="sr-only">{html.escape(s["peak_sr"])}</span>') if peak else ""
            cls = "cell" + (" peak" if peak else "") + (" out" if sd.layers[li] == final else "")
            cells.append(f'<td class="{cls}" style="background:{bg};color:{fg}">'
                         f'<span class="w"><bdi>{word}</bdi></span>{sup}{peak_mark}</td>')
        rows.append(f"<tr>{''.join(cells)}</tr>")
    tbody = f'<tbody>{"".join(rows)}</tbody>'

    vocab_n = f"{sd.vocab_size:,}" if sd.vocab_size else "the vocabulary"

    # --- headline text: a blind user should hear the finding first, as a finding
    if tracked and best:
        best_tok = _clean(sd.context_token_strs[sd.ctx_offset + best[2]])
        title = s["title_tracked"].format(concept=esc_concept)
        chip = f'<span class="chip">{html.escape(s["tracking"].format(concept=concept))}</span>&nbsp; '
        rule = s["rule_tracked"].format(concept=esc_concept)
        # Depth word must match the data: early (<1/3), midway (1/3..2/3), deep (>2/3).
        # A hardcoded "deep" would be wrong for an early peak (e.g. overdose at layer 10).
        peak_layer = sd.layers[best[1]]
        frac = peak_layer / n_layers if n_layers else 1.0
        depth_key = "depth_deep" if frac > 2 / 3 else "depth_mid" if frac >= 1 / 3 else "depth_early"
        depth = s[depth_key].format(layer=peak_layer)
        key = (f'<p class="key"><span aria-hidden="true">&#128161;</span> '
               f'<b>{html.escape(s["key_finding"])}</b> '
               + s["callout_tracked"].format(word=f"<bdi>{best_tok}</bdi>", depth=depth,
                                              concept=esc_concept, rank=best[0] + 1, vocab=vocab_n)
               + '</p>')
        legend = (f'<div class="legend">{html.escape(s["legend_label"].format(concept=concept))}'
                  f'&nbsp; {_legend(s["legend"])}</div>')
    else:
        why = (s["not_tracked"].format(concept=esc_concept)
               if concept.strip() else s["no_concept"])
        title = s["title_plain"]
        chip = ""
        rule = s["rule_plain"]
        key = f'<p class="note">{s["callout_plain"].format(why=why)}</p>'
        legend = ""

    # --- optional language switcher nav
    nav = ""
    if alt_langs:
        parts = []
        for code, label, href in alt_langs:
            if code == lang:
                parts.append(f'<b lang="{html.escape(code)}">{html.escape(label)}</b>')
            else:
                parts.append(f'<a lang="{html.escape(code)}" href="{html.escape(href)}">{html.escape(label)}</a>')
        nav = (f'<nav class="langnav" aria-label="{html.escape(s["lang_nav"])}">'
               + " · ".join(parts) + "</nav>")

    caption = f'<caption class="sr-only" translate="yes">{html.escape(s["caption"])}</caption>'
    region = html.escape(s["region_label"])
    footer = html.escape(s["footer"].format(
        model=model_name, shown=len(col_lis), total=sd.layers[-1] + 1, tokens=sd.seq_len))
    # best-effort translation note only appears on non-English pages (English has
    # nothing translated, so the note there would be noise). Absent key -> skipped.
    tnote = f'{html.escape(s["translation_note"])}<br>' if s.get("translation_note") else ""

    return (
        f'<!doctype html><html lang="{html.escape(lang)}" dir="{html.escape(s["dir"])}">'
        f'<head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>Readable J-lens{": " + esc_concept if tracked else ""}</title>'
        f'<style>{_CSS}</style></head><body><main>'
        f'{nav}'
        f'<h1>{title}</h1>'
        f'{key}'
        f'<p class="sub"><b>{html.escape(s["prompt_label"])}</b> '
        f'<code translate="no">{_clean(prompt, cap=240)}</code><br>'
        f'{chip}{s["how_to_read"]} {rule}</p>'
        f'{legend}'
        f'<div class="wrap" role="region" aria-label="{region}" tabindex="0">'
        f'<table translate="no">{caption}{thead}{tbody}</table></div>'
        f'<p class="fine">{footer}<br>{tnote}{_CREDIT}</p>'
        f'</main></body></html>'
    )
