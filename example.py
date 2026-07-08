# SPDX-License-Identifier: Apache-2.0
"""Minimal end-to-end example: compute a Jacobian-lens slice and render it as a
readable page. Requires Anthropic's `jlens` installed from source (see README)
plus a fitted lens. Uses the public Qwen3.5-4B lens on Hugging Face.

    python example.py            # -> slice.html (open it in a browser)
"""
import torch, transformers, jlens
from jlens.vis import compute_slice

from jlens_readable import build_readable_page

MODEL = "Qwen/Qwen3.5-4B"
# Pin to an exact commit for reproducibility and supply-chain safety. A tag or
# branch name (like the lens revision below) pins a NAME, not the bytes; only a
# commit hash pins the bytes. Leave None to take the repo's current revision.
MODEL_REVISION = None
LENS_REPO, LENS_REV = "neuronpedia/jacobian-lens", "qwen-n1000"
LENS_FILE = "qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt"
DEVICE = "mps"   # "mps" (Apple Silicon) | "cuda" (NVIDIA) | "cpu"

# Qwen3.5-4B ships as a multimodal wrapper; try the image-text class first.
hf = None
for name in ("AutoModelForImageTextToText", "AutoModelForCausalLM"):
    cls = getattr(transformers, name, None)
    if cls is None:
        continue
    try:
        # We deliberately do NOT pass trust_remote_code=True: this example does not
        # need it, and enabling it runs Python straight from the model repo. If a
        # load fails, do not "fix" it by turning that on.
        hf = cls.from_pretrained(MODEL, revision=MODEL_REVISION,
                                 dtype=torch.bfloat16).to(DEVICE); break
    except Exception as e:
        print(name, "failed:", e)
if hf is None:
    raise RuntimeError("could not load " + MODEL)

tok = transformers.AutoTokenizer.from_pretrained(MODEL)
model = jlens.from_hf(hf, tok)
# The lens is a .pt file loaded (by jlens) via torch, which uses pickle and can
# execute code on load. We pin the revision and only load lenses from a source we
# trust. For stronger guarantees, pin LENS_REV to a commit hash.
lens = jlens.JacobianLens.from_pretrained(LENS_REPO, filename=LENS_FILE, revision=LENS_REV)

# Pick a prompt and a single-token concept to track. Pin it so compute_slice
# keeps its full rank grid (that's what the colour encodes).
prompt = ("Fact: The capital of Japan is Tokyo.\n"
          "Fact: The currency used in the country shaped like a boot is")
concept = "Italy"
cid = tok.encode(" " + concept, add_special_tokens=False)
cid = cid[0] if len(cid) == 1 else None

sd = compute_slice(model, lens, prompt, top_n=10, mask_display=True,
                   pinned_token_ids={cid} if cid else None, layer_stride=2)

html = build_readable_page(sd, prompt=prompt, n_layers=model.n_layers,
                           concept=concept, concept_id=cid, model_name="Qwen3.5-4B")
open("slice.html", "w", encoding="utf-8").write(html)
print("wrote slice.html: open it and watch 'Italy' climb across the layers")
