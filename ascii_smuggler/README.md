# Aureon ASCII-Smuggler

Aureon’s zero-width ASCII smuggler enables covert transmission of authenticated text inside ordinary character streams.  
All smuggled data is invisible to humans yet fully recoverable and signature-verified by Aureon.

---

## Overview

Aureon ASCII-Smuggler converts arbitrary plaintext into a sequence of zero-width characters, embedding a cryptographic signature so the receiver can confirm authenticity and detect any corruption or tampering.

The system is designed for:
- Secure covert-channel messaging  
- Embedding hidden metadata inside public posts  
- Protecting provenance of transmitted text  
- High-density invisible annotations  
- Multi-carrier interoperability  

---

## Core Capabilities

- Zero-width encoding and decoding  
- Multi-carrier embedding (space, punctuation, emoji, symbols)  
- Deterministic signature bits derived from Aureon’s internal seed  
- Zero-width signature encoding  
- Full mismatch, tamper, and corruption rejection  

---

## High-Level API

`aureon_smuggler.py` provides:

- `smuggle(text, carrier_key)`  
- `reveal(smuggled, carrier_key)`  
- `is_authentic(smuggled, carrier_key)`  

---

## Full Test Suite

`tests.py` covers:  
- Round-trip encoding  
- Signature verification  
- Carrier integrity  
- Tamper conditions  
- Multi-carrier scenarios  
- Stress testing  

---

## Repository Structure

aureon-ascii-smuggler/  
│  
├── ascii_smuggler.py        # Core zero-width encoding/decoding  
├── carriers.py              # Carrier registry + semantics  
├── signature_verifier.py    # Signature embedding + authenticity checks  
├── aureon_smuggler.py       # High-level Aureon API  
└── tests.py                 # Comprehensive test suite
