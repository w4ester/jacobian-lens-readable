# SPDX-License-Identifier: Apache-2.0
"""A legible, dependency-free view for Anthropic's Jacobian Lens.

The upstream repo (https://github.com/anthropics/jacobian-lens) ships one
visualization: a dense d3 heat-map of one glyph per token. It answers a
researcher's questions well, but a newcomer or a classroom can't read it.

This module renders the *same* ``jlens.vis.SliceData`` as a plain HTML table
you can read at a glance:

  * rows    = the words of the prompt (reading order, top to bottom)
  * columns = the model's layers, left to right, with the real OUTPUT on the right
  * cell    = the top word that (position, layer) leans toward
  * colour  = how highly the cell ranks a concept you choose to track, in six
              log-spaced buckets (darker = higher)

It is pure Python (only the standard-library ``html`` module), adds no
dependencies, uses only the public ``SliceData`` surface, and emits a single
self-contained HTML string, with no d3 and no JavaScript, e-mailable, works from
``file://``.

The science is entirely Anthropic's: "Verbalizable Representations Form a Global
Workspace in Language Models" (https://transformer-circuits.pub/2026/workspace).
This is only a rendering layer.
"""
from __future__ import annotations

import html

#: The ``SliceData`` fields this renderer reads. Upstream is a frozen reference
#: implementation, so this is effectively a stable contract.
_SLICEDATA_FIELDS = (
    "seq_len", "layers", "context_token_strs", "top_ids", "rank_tensor",
    "tracked_token_ids", "vocab_fragment", "vocab_size", "ctx_offset",
)


def _clean(s: str, cap: int = 12) -> str:
    """Trim, escape, and cap a token string for display (newline -> ⏎)."""
    s = s.replace("\n", "⏎").strip()
    if len(s) > cap:
        s = s[:cap] + "…"
    return html.escape(s) if s else "·"


def _color(rank: int) -> tuple[str, str]:
    """Map a 0-indexed rank (0 == the model's #1 guess) to (background, text)."""
    if rank < 0:      return "#ffffff", "#ccc"   # concept absent from this cell
    if rank == 0:     return "#b45309", "#fff"   # top choice
    if rank <= 4:     return "#ea580c", "#fff"   # top 5
    if rank <= 19:    return "#f59e0b", "#111"   # top 20
    if rank <= 99:    return "#fcd34d", "#111"   # top 100
    if rank <= 999:   return "#fef3c7", "#555"   # top 1000
    return "#ffffff", "#ccc"                      # not close


_LEGEND = "".join(
    f'<span class="lg" style="background:{b};color:{t}">{lab}</span>'
    for b, t, lab in [
        ("#b45309", "#fff", "top choice"), ("#ea580c", "#fff", "top 5"),
        ("#f59e0b", "#111", "top 20"), ("#fcd34d", "#111", "top 100"),
        ("#fef3c7", "#555", "top 1000"), ("#fff", "#bbb", "not close"),
    ]
)

_CSS = """
body{font-family:-apple-system,Helvetica,Arial,sans-serif;margin:22px;color:#111}
h1{font-size:20px;margin:0 0 6px}
.sub{color:#444;font-size:13px;margin:0 0 10px;max-width:940px;line-height:1.55}
.chip{display:inline-block;background:#b45309;color:#fff;font-size:12px;font-weight:600;padding:2px 9px;border-radius:11px}
.key{font-size:14px;background:#fff7ed;border-left:4px solid #ea580c;padding:9px 13px;margin:11px 0;max-width:940px;line-height:1.5}
.note{font-size:13px;background:#f3f4f6;border-left:4px solid #9ca3af;padding:8px 12px;margin:11px 0;max-width:940px}
.legend{margin:9px 0;font-size:12px;color:#555} .lg{display:inline-block;padding:2px 8px;margin:0 4px 4px 0;border-radius:4px;border:1px solid #eee}
.fine{color:#888;font-size:11px;margin-top:8px} .fine a{color:#3b5bdb}
.wrap{overflow:auto;border:1px solid #e5e5e5;max-height:78vh}
table{border-collapse:collapse;font-size:12px}
th,td{border:1px solid #eee}
.corner{font-size:10px;color:#999;font-weight:normal;padding:4px 6px;position:sticky;left:0;top:0;z-index:3;background:#fafafa}
.lyr{font-size:11px;color:#666;font-weight:normal;padding:5px 7px;background:#fafafa;position:sticky;top:0;z-index:2;text-align:center}
.lyr.out{color:#111;font-weight:bold;border-left:2px solid #999}
.tok{font-family:ui-monospace,Menlo,monospace;font-size:11px;padding:4px 8px;background:#fafafa;position:sticky;left:0;z-index:1;white-space:nowrap;text-align:left}
.tok.tgt{background:#3b5bdb;color:#fff} .tok .pn{color:#bbb;margin-right:6px;font-size:10px} .tok.tgt .pn{color:#cdd6ff}
.cell{min-width:56px;max-width:96px;height:32px;padding:2px 4px;text-align:center;vertical-align:middle}
.cell.out{border-left:2px solid #999}
.cell .w{display:block;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;line-height:1.1}
.cell .sup{display:block;font-size:9px;font-weight:400;opacity:.9;line-height:1}
.cell.peak{outline:3px solid #1e40af;outline-offset:-3px}
"""

_CREDIT = (
    'Rendered with <a href="https://github.com/w4ester/jacobian-lens-readable">'
    'jacobian-lens-readable</a> · method: Anthropic Jacobian Lens '
    '(<a href="https://transformer-circuits.pub/2026/workspace">paper</a> · '
    '<a href="https://github.com/anthropics/jacobian-lens">code</a>)'
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
) -> str:
    """Render a ``jlens.vis.SliceData`` into a self-contained readable HTML page.

    Args:
        slice_data: A ``SliceData`` from ``jlens.vis.compute_slice``.
        prompt: The prompt text (shown in the header).
        n_layers: ``model.n_layers``; used to label the final/output column.
        concept: A word to track and colour by (e.g. ``"Italy"``). When empty or
            untracked, the page renders the top word per cell without a heat-map.
        concept_id: The token id of ``concept``. It must be in
            ``slice_data.tracked_token_ids`` for the colouring to appear; pass
            it to ``compute_slice`` via ``pinned_token_ids`` to guarantee that.
        model_name: Display label for the model (e.g. ``"Qwen3.5-4B"``).
        layer_step: Render every Nth layer to keep columns on one screen; the
            final layer and the concept's peak layer are always included.

    Returns:
        A single self-contained HTML document as a string (no JS, no assets).
    """
    sd = slice_data
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

    head = ['<th class="corner">word ⬎ &nbsp; layer →</th>']
    for li in col_lis:
        layer = sd.layers[li]
        out = layer == final
        head.append(f'<th class="lyr{" out" if out else ""}">'
                    f'{"output" if out else "L" + str(layer)}</th>')
    header_row = f"<tr>{''.join(head)}</tr>"

    rows = []
    for pos in range(sd.seq_len):
        tgt = bool(best) and pos == best[2]
        tok = _clean(sd.context_token_strs[sd.ctx_offset + pos], cap=16)
        cells = [f'<th class="tok{" tgt" if tgt else ""}">'
                 f'<span class="pn">{sd.ctx_offset + pos}</span>{tok}</th>']
        for li in col_lis:
            tid = int(sd.top_ids[pos, li, 0])
            word = _clean(vocab.get(tid, "?"))
            rank = rank_at(pos, li)
            bg, fg = _color(rank)
            sup = f'<span class="sup">#{rank + 1}</span>' if 1 <= rank <= 99 else ""
            peak = bool(best) and li == best[1] and pos == best[2]
            cls = "cell" + (" peak" if peak else "") + (" out" if sd.layers[li] == final else "")
            cells.append(f'<td class="{cls}" style="background:{bg};color:{fg}">'
                         f'<span class="w">{word}</span>{sup}</td>')
        rows.append(f"<tr>{''.join(cells)}</tr>")

    vocab_n = f"{sd.vocab_size:,}" if sd.vocab_size else "the vocabulary"
    if tracked and best:
        best_tok = _clean(sd.context_token_strs[sd.ctx_offset + best[2]])
        title = f"Where &ldquo;{html.escape(concept)}&rdquo; lights up inside the model"
        chip = f'<span class="chip">tracking: {html.escape(concept)}</span>&nbsp; '
        rule = (f'The <b>color</b> of a box is how high it ranks '
                f'&ldquo;{html.escape(concept)}&rdquo; there: <b>darker = higher</b>.')
        callout = (f'<div class="key">&#128161; Find the <b>blue-outlined box</b>: on the row for '
                   f'<b>&ldquo;{best_tok}&rdquo;</b>, deep in the model (layer {sd.layers[best[1]]}), '
                   f'&ldquo;{html.escape(concept)}&rdquo; is the model&rsquo;s <b>#{best[0] + 1}</b> pick '
                   f'out of {vocab_n} words, though the prompt never says it. The model has '
                   f'worked out the answer before writing a thing.</div>'
                   f'<div class="legend">how high &ldquo;{html.escape(concept)}&rdquo; ranks in a box:'
                   f'&nbsp; {_LEGEND}</div>')
    else:
        why = (f'&ldquo;{html.escape(concept)}&rdquo; is not tracked'
               if concept.strip() else 'no concept given')
        title = "What the model leans toward, layer by layer"
        chip = ""
        rule = 'Each box shows the top word that spot leans toward.'
        callout = (f'<div class="note">Showing the top word per cell only ({why}, so there&rsquo;s '
                   f'no concept heat-map). Pass a single-token concept to see where it lights up.</div>')

    return (
        f'<!doctype html><html><head><meta charset="utf-8">'
        f'<title>Readable J-lens{": " + html.escape(concept) if tracked else ""}</title>'
        f'<style>{_CSS}</style></head><body>'
        f'<h1>{title}</h1>'
        f'<p class="sub"><b>Prompt:</b> <code>{_clean(prompt, cap=240)}</code><br>'
        f'{chip}Each <b>row</b> is one word of the prompt. Reading a row '
        f'<b>left&nbsp;&rarr;&nbsp;right</b> shows how the model&rsquo;s guess for the '
        f'<b>next</b> word firms up as it goes deeper, ending in the <b>output</b> column '
        f'(what it actually says). {rule}</p>'
        f'{callout}'
        f'<div class="wrap"><table>{header_row}{"".join(rows)}</table></div>'
        f'<p class="fine">{html.escape(model_name)} · {len(col_lis)} of {sd.layers[-1] + 1} '
        f'layers · {sd.seq_len} tokens<br>{_CREDIT}</p>'
        f'</body></html>'
    )
