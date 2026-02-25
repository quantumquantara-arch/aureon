# Aureon ASCII-Smuggler — Carrier & Zero-Width Lexicon

A complete, fixed lexicon of all symbols, carriers, and zero-width entities used by Aureon’s covert-channel system.  
This file defines the authoritative source of every encoding element.

---

## Zero-Width Core Channel (Invisible Bitstream)

These characters form Aureon’s hidden binary stream. They never appear visibly but encode all payload bits and signature material.

- U+200B — ZERO WIDTH SPACE  
- U+200C — ZERO WIDTH NON-JOINER  
- U+200D — ZERO WIDTH JOINER  
- U+2060 — WORD JOINER  
- U+FEFF — ZERO WIDTH NO-BREAK SPACE  

**Usage:** deterministic binary mapping, tamper detection, signature verification.

---

## Visible Carrier Families

Visible carriers never contain hidden bits themselves;  
they define **where** zero-width characters may be injected, establishing smuggling geometry.

### Whitespace Family
- ` ` space  
- `\t` tab  
- `\n` newline  

### Punctuation Family
- `.`  
- `,`  
- `:`  
- `;`  
- `!`  
- `?`  
- `-`  
- `—`  
- `(` `)`  
- `[` `]`  
- `{` `}`  

### Symbol Family
- `*`  
- `+`  
- `=`  
- `/`  
- `|`  
- `_`  
- `#`  
- `%`  
- `@`  
- `&`  

---

## Emoji Carrier Set

High-entropy anchors ideal for high-density multi-carrier smuggling.

- 🙂  
- 🤍  
- 🔹  
- 🌿  
- 🔒  
- 🜂  
- 🜁  
- 🜄  
- 🜃  
- 🜔  

---

## High-Entropy Glyph Carriers

Used when the carrier_key requests maximum unpredictability.

- 𐍊  
- 𐌿  
- 𐌾  
- 𐌳  

---

## Structural Markers

Reserved for synchronization boundaries.  
Never hold payload bits.

- `<<<`  
- `>>>`  
- `||`  
- `::`  

---

## Invariance Rules

- Lexicon is fixed and non-expandable at runtime.  
- Zero-width mapping is deterministic and seed-dependent.  
- Carriers define geometry, not payload.  
- Structural markers must not appear in plaintext without escaping.  

---

## Version

Lexicon v1.0 — Aureon ASCII-Smuggler  
Authoritative and canonical for all future implementations.
