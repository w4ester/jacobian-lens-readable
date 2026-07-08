# jacobian-lens-readable

A legible, dependency-free HTML view for **[Anthropic's Jacobian Lens](https://github.com/anthropics/jacobian-lens)**.

**Accessible intelligence:** the goal here is to make a model's reasoning legible to anyone
curious enough to look, not just to people who can read a research-grade heat-map.

> **This is a rendering layer, not the science.** All the interpretability work (the Jacobian
> Lens itself, the "J-space" / global-workspace findings) is Anthropic's, from
> *[Verbalizable Representations Form a Global Workspace in Language Models](https://transformer-circuits.pub/2026/workspace)*.
> This project only draws the readout differently.

## Why

When a language model answers you, it lines up ideas a few steps before it writes any of them.
The Jacobian Lens turns that internal activity back into readable words. The official tool
draws it as a dense d3 heat-map with a single glyph per token, which speaks fluent researcher.
This project renders the **same `jlens.vis.SliceData`** as a plain table that speaks plain
language, so the same insight is open to a student, a teacher, a superintendent, or anyone else:

- **rows** = the words of your prompt (reading order, top to bottom)
- **columns** = the model's layers, left to right, with the real **output on the right**
- **cell** = the top word that `(position, layer)` leans toward
- **color** = how highly the cell ranks a **concept you choose to track**, in six log-spaced
  buckets (darker means higher)

So on a two-hop prompt like *"the country shaped like a boot"* you can literally read `Italy`
climb from absent to `#3` across the layers, the model working out the answer before it writes
a word.

**Live demos:** https://w4ester.github.io/jacobian-lens-readable/

## Set it up by pasting a prompt (no coding required)

You do not have to write any code. Copy the prompt below, keep the one line that matches your
computer, and paste it into whichever large model you already use as an assistant. It will
install everything and run the first example for you.

**Works with any of these three assistants:** **Claude** (Claude Code, or claude.ai) &middot;
**ChatGPT** (GPT-5.5, or the Codex CLI) &middot; **Google Gemini**.

```text
I want to watch the concepts a language model lines up in its head just before it
speaks, using Anthropic's Jacobian Lens and the readable view at
https://github.com/w4ester/jacobian-lens-readable. Please set this up on my machine
and explain each step in plain language as you go.

My hardware / operating system (KEEP THE ONE THAT MATCHES ME, DELETE THE OTHER TWO):
  - macOS on Apple Silicon (M1/M2/M3/M4)  ->  use device "mps"
  - Linux with an NVIDIA GPU              ->  use device "cuda"
  - Windows                               ->  use WSL2 with an NVIDIA GPU ("cuda"),
                                              or "cpu" if the machine has no GPU

Please do all of this yourself, running the commands rather than asking me to:
  1. Make a fresh Python 3.10+ environment.
  2. Install Anthropic's Jacobian Lens from source:
     git clone https://github.com/anthropics/jacobian-lens
     pip install -e ./jacobian-lens
  3. Install the readable view from source:
     git clone https://github.com/w4ester/jacobian-lens-readable
     pip install -e ./jacobian-lens-readable
  4. Download the open Qwen3.5-4B model and Neuronpedia's fitted lens
     (Hugging Face repo "neuronpedia/jacobian-lens", revision "qwen-n1000").
  5. Run jacobian-lens-readable/example.py using the device for my hardware above.
  6. Open the slice.html it writes and tell me, in one sentence, what rank the word
     "Italy" reaches and in which layer, for the prompt about the country shaped
     like a boot.

If a step fails, read the error, try the most likely fix, and keep going before
asking me anything.
```

That is the whole "getting started" experience: pick your machine, paste, watch it work.

## How to read the tables

Each **row** is one word of the prompt. Reading a row **left to right** shows how the model's
guess for the **next** word firms up as it goes deeper, ending in the **output** column (what it
actually says). The **color** of a box is how highly it ranks the tracked concept, darker for
higher: top choice, top 5, top 20, top 100, top 1000, or not close.

## Install (manual, for developers)

The renderer is **pure standard-library Python** (no dependencies of its own). To *produce* a
`SliceData` you need Anthropic's `jlens`, which is installed from source:

```bash
# 1. Anthropic's Jacobian Lens (source only, not on PyPI)
git clone --depth 1 https://github.com/anthropics/jacobian-lens.git
cd jacobian-lens && pip install -e . && cd ..

# 2. this renderer
git clone https://github.com/w4ester/jacobian-lens-readable.git
cd jacobian-lens-readable && pip install -e .
```

## Use

```python
from jlens.vis import compute_slice
from jlens_readable import build_readable_page

# pin the concept token so compute_slice keeps its full rank grid
sd = compute_slice(model, lens, prompt, mask_display=True,
                   pinned_token_ids={concept_id}, layer_stride=2)

html = build_readable_page(
    sd,
    prompt=prompt,
    n_layers=model.n_layers,
    concept="Italy",          # a word to track and color by ("" = top-word-only)
    concept_id=concept_id,    # its single token id (must be pinned/tracked above)
    model_name="Qwen3.5-4B",  # display label
)
open("slice.html", "w").write(html)   # self-contained, no JS, e-mailable
```

See [`example.py`](example.py) for a complete runnable script using the public Qwen3.5-4B lens.

## The `SliceData` contract

Upstream is a frozen reference implementation, which is an advantage: the fields this renderer
reads are effectively a stable contract, so this package cannot be broken by upstream churn. It
uses only:

```
seq_len · layers · context_token_strs · top_ids · rank_tensor ·
tracked_token_ids · vocab_fragment · vocab_size · ctx_offset
```

Ranks from `jlens` are **0-indexed** (rank 0 = the #1 guess); the page displays `rank + 1`.

## How this was built

Small tool, bigger idea: **accessible intelligence, built by orchestrated intelligence.** It came
together inside the **WF-AI Platform**, where a local model runs the show and pulls in frontier peers
only when a second (or third) brain earns its keep.

The cast:

- **Conductor:** a local **Gemma-4 31B**, coordinating from `wf-ai chat`, deciding who to bring in
  and when.
- **The panel**, summoned through the platform's `invoke-*` skills:
  - `invoke-codex` &rarr; **Codex (GPT-5.5)**, the cross-family second opinion.
  - `invoke-opus` &rarr; **Claude Opus 4.8**, the builder and lead reviewer.
  - `invoke-fable` &rarr; **Claude Fable 5**, the fast, Claude-native fresh-context pass.

What the ensemble actually settled: the **readable table layout** (rows = words, columns = layers,
color = concept rank) and the decision to ship this as a **companion package rather than an upstream
PR**. On both, Codex and Fable reached the same verdict independently and Opus synthesized it, so the
credit belongs to the coordination, not to any single model.

Built under the banner **"w4ester & ai orchestration."** Onward, and let's grow. 🌱

## Credits & acknowledgments

This project is a thin rendering layer. The hard parts belong to others:

- **The Jacobian Lens & the science:** Anthropic. From *Verbalizable Representations Form a
  Global Workspace in Language Models*, Gurnee et al., *Transformer Circuits Thread*, July 6 2026
  ([paper](https://transformer-circuits.pub/2026/workspace) · [code](https://github.com/anthropics/jacobian-lens)).
- **The fitted lens:** [Neuronpedia](https://neuronpedia.org/jlens), who trained and published
  the lens this project loads (`neuronpedia/jacobian-lens` on Hugging Face, revision `qwen-n1000`)
  and built the hosted interactive explainer.
- **The model:** [`Qwen/Qwen3.5-4B`](https://huggingface.co/Qwen/Qwen3.5-4B) by the Qwen team
  (Alibaba), the model whose internals every demo reads.
- **The lens's fitting corpus:** Salesforce
  [WikiText-103](https://huggingface.co/datasets/Salesforce/wikitext).

### Citation

If you reference the underlying method, cite the paper, not this repo:

```bibtex
@article{gurnee2026workspace,
  title   = {Verbalizable Representations Form a Global Workspace in Language Models},
  author  = {Gurnee, Wes and Sofroniew, Nicholas and Pearce, Adam and Piotrowski, Mateusz
             and Kauvar, Isaac and Chen, Runjin and Soligo, Anna and Bogdan, Paul and Ong, Euan
             and Wang, Rowan and Thompson, Ben and Abrahams, David and Kantamneni, Subhash
             and Ameisen, Emmanuel and Batson, Joshua and Lindsey, Jack},
  year    = {2026},
  journal = {Transformer Circuits Thread},
  url     = {https://transformer-circuits.pub/2026/workspace}
}
```

## License

Apache-2.0 (matching upstream). Not affiliated with or endorsed by Anthropic, Neuronpedia, or the
Qwen team; naming them states interoperability and credit only.
