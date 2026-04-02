# Paper 1 Scientific Audit (2026-03-22)

This note records the final high-value scientific checks run after the late editorial passes.

## Re-run Status

The core measurement scripts were rerun against the current Enterprise bundle and remain aligned with the manuscript:

- campaigns with techniques: `51`
- intrusion sets with techniques: `172`
- active behavioral `attack-pattern` objects: `691`
- campaign coverage: `43.0%`
- intrusion-set coverage: `70.6%`
- platform-agnostic techniques: `32`
- campaign positive-evidence identifiability: `51/51`
- intrusion-set positive-evidence identifiability: `145/168`

The manuscript values remain synchronized with the generated provenance.

## Strengthening Change Accepted

One substantive strengthening opportunity was identified and incorporated into the paper:

- the main analysis now contrasts campaign identifiability with intrusion-set identifiability;
- this sharpens the paper's central boundary claim by showing that campaign profiles can be sparse yet distinctive, while intrusion-set profiles are richer but not universally separable;
- the added comparison does not change the thesis, but it makes the distinction between profile separability and executability more concrete.

## Strengthening Check Rejected

We also tested whether the campaign identifiability result looked unusually strong under a matched-sparsity random baseline.

Simulation setup:

- 500 random trials;
- same number of campaign profiles (`51`);
- same per-profile technique counts as the observed Enterprise campaigns;
- techniques sampled uniformly without replacement from the observed Enterprise campaign technique universe.

Result:

- mean identifiable profiles: `50.946`
- minimum identifiable profiles across trials: `50`
- maximum identifiable profiles across trials: `51`
- fraction of trials with all `51/51` profiles identifiable: `0.946`

Takeaway:

- full campaign separability is not surprising under matched sparsity alone;
- this check does **not** strengthen the paper's claim and would likely weaken the rhetorical force of the identifiability result if foregrounded;
- the paper therefore keeps identifiability as a structural contrast, not as a surprising-by-chance claim.

## Production Note

The `gap-example` figure required a robustness fix during the clean rebuild. The visual content was preserved, but the center bridge node was simplified to eliminate a TikZ build fragility.
