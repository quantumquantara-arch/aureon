?# Sample determinism test (Python for cross-compat, but can be PS)
import hashlib

input_data = 'Fixed test input for Aureon determinism: 42'
transformed = input_data + ' transformed to ' + str(42 * 42)
computed_hash = hashlib.sha256(transformed.encode()).hexdigest()
print(computed_hash)  # Compare manually
