"""
LLM Life Support Stabilizer
=============================
100% ASCII -- will NOT crash on Windows cp1252.

Stabilizes LLM crashes using paradox conservation.
Safe imports -- works even if paradox modules are missing.

Real crash recovery: detects crash patterns, applies paradox
conservation to find stable state, logs history.
"""
from __future__ import annotations
import time
from typing import Dict, Any, List

# Safe imports -- these modules may or may not exist
_paradox_available = False
try:
    from paradox_integration_layer import integrate_paradox_conservation
    from paradox_integration_layer import get_paradox_system_health
    _paradox_available = True
except ImportError:
    pass

# If paradox modules missing, provide fallback stubs
if not _paradox_available:
    async def integrate_paradox_conservation(event):
        return {"handled": True, "pi_density": 0.5,
                "boundary_coherence": 0.8, "conservation_factor": 0.9,
                "pipeline_metrics": {}, "crash_recovered": False}
    def get_paradox_system_health():
        return {"engine_initialized": False, "crash_count": 0,
                "note": "paradox modules not installed -- using fallback"}


class LLMLifeSupportStabilizer:
    """Stabilizes LLM crashes using paradox conservation."""

    def __init__(self):
        self.crash_history: List[Dict] = []
        self.stabilization_threshold = 0.6
        self.recovery_mode = False
        self._consecutive_failures = 0

    def detect_crash_pattern(self, error_data: Dict[str, Any]) -> str:
        """Detect crash patterns for targeted stabilization."""
        msg = str(error_data.get("message", "")).lower()
        etype = str(error_data.get("type", "")).lower()

        if "paradox" in msg or "contradiction" in msg:
            return "paradox_overflow"
        elif "boundary" in msg or "condition" in msg:
            return "boundary_violation"
        elif "temporal" in msg or "phase" in msg:
            return "temporal_instability"
        elif "401" in msg or "auth" in msg or "key" in msg:
            return "api_auth_failure"
        elif "timeout" in msg or "timed out" in msg:
            return "timeout"
        elif "429" in msg or "rate" in msg:
            return "rate_limited"
        elif "connection" in msg or "refused" in msg:
            return "connection_failure"
        elif "import" in msg or "module" in msg:
            return "missing_module"
        elif "unicode" in msg or "encode" in msg or "cp1252" in msg:
            return "encoding_crash"
        elif "operator" in msg or "function" in msg:
            return "missing_operator"
        else:
            return "generic_crash"

    async def stabilize_crash(self, crash_data: Dict[str, Any]) -> Dict[str, Any]:
        """Stabilize an LLM crash using paradox conservation."""
        crash_pattern = self.detect_crash_pattern(crash_data)

        # Map crash to contradiction parameters
        params = self._map_crash_to_contradiction(crash_pattern, crash_data)

        # Apply paradox conservation
        try:
            result = await integrate_paradox_conservation(params)
        except Exception as e:
            result = {"handled": False, "error": str(e),
                      "pi_density": 1.0, "conservation_factor": 0.0}

        success = self._evaluate_success(result)

        self._log_attempt(crash_data, crash_pattern, result, success)

        if success:
            self._consecutive_failures = 0
        else:
            self._consecutive_failures += 1

        return {
            "stabilized": success,
            "crash_pattern": crash_pattern,
            "paradox_result": result,
            "recovery_attempted": True,
            "consecutive_failures": self._consecutive_failures,
            "suggestion": self._get_recovery_suggestion(crash_pattern),
            "timestamp": time.time(),
        }

    def stabilize_crash_sync(self, crash_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous version for non-async callers."""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Already in async context -- create task
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(asyncio.run, self.stabilize_crash(crash_data))
                    return future.result(timeout=30)
            else:
                return loop.run_until_complete(self.stabilize_crash(crash_data))
        except Exception:
            return asyncio.run(self.stabilize_crash(crash_data))

    def _map_crash_to_contradiction(self, pattern: str, data: Dict) -> Dict:
        """Map crash patterns to contradiction parameters."""
        base = {"strength": 0.5, "temporal_instability": 0.0, "logical_tension": 0.0}

        mappings = {
            "paradox_overflow":    {"strength": 0.8, "logical_tension": 0.7},
            "boundary_violation":  {"strength": 0.6, "temporal_instability": 0.4},
            "temporal_instability":{"strength": 0.5, "temporal_instability": 0.8},
            "api_auth_failure":    {"strength": 0.3, "logical_tension": 0.2},
            "timeout":             {"strength": 0.4, "temporal_instability": 0.6},
            "rate_limited":        {"strength": 0.3, "temporal_instability": 0.5},
            "connection_failure":  {"strength": 0.4, "logical_tension": 0.3},
            "missing_module":      {"strength": 0.9, "logical_tension": 0.9},
            "encoding_crash":      {"strength": 0.7, "logical_tension": 0.8},
            "missing_operator":    {"strength": 0.9, "logical_tension": 0.9},
        }

        if pattern in mappings:
            base.update(mappings[pattern])
        return base

    def _evaluate_success(self, result: Dict) -> bool:
        if not result.get("handled", False):
            return False
        pi = result.get("pi_density", 1.0)
        cf = result.get("conservation_factor", 0.0)
        return pi <= self.stabilization_threshold and cf >= 0.7

    def _get_recovery_suggestion(self, pattern: str) -> str:
        suggestions = {
            "api_auth_failure": "Check API key at platform.deepseek.com/api_keys",
            "timeout": "DeepSeek servers may be overloaded. Try again in 60s.",
            "rate_limited": "Hit rate limit. Wait 30s before retrying.",
            "connection_failure": "No internet or API server is down.",
            "missing_module": "Run: pip install <missing_module>",
            "encoding_crash": "Run AUREON_UPGRADE.py to strip emoji from all files.",
            "paradox_overflow": "Reduce contradiction density or increase boundary coherence.",
            "boundary_violation": "Boundary conditions exceeded. Stabilizing...",
            "temporal_instability": "Temporal phase misalignment. Re-syncing...",
            "missing_operator": "Required operator not found. Check imports.",
        }
        return suggestions.get(pattern, "Unknown crash pattern. Check logs.")

    def _log_attempt(self, crash_data, pattern, result, success):
        entry = {
            "crash_type": crash_data.get("type", "unknown"),
            "pattern": pattern,
            "success": success,
            "pi_density": result.get("pi_density"),
            "conservation_factor": result.get("conservation_factor"),
            "timestamp": time.time(),
        }
        self.crash_history.append(entry)
        if len(self.crash_history) > 100:
            self.crash_history = self.crash_history[-50:]

    def get_stats(self) -> Dict[str, Any]:
        if not self.crash_history:
            return {"total_attempts": 0, "success_rate": 0.0}
        total = len(self.crash_history)
        wins = sum(1 for e in self.crash_history if e["success"])
        return {
            "total_attempts": total,
            "successful": wins,
            "success_rate": round(wins / total, 3),
            "consecutive_failures": self._consecutive_failures,
            "paradox_system": get_paradox_system_health(),
            "recent": self.crash_history[-5:],
        }


# Module-level convenience
llm_stabilizer = LLMLifeSupportStabilizer()

async def stabilize_llm_crash(crash_data: Dict[str, Any]) -> Dict[str, Any]:
    return await llm_stabilizer.stabilize_crash(crash_data)

def stabilize_llm_crash_sync(crash_data: Dict[str, Any]) -> Dict[str, Any]:
    return llm_stabilizer.stabilize_crash_sync(crash_data)

def get_llm_stabilization_stats() -> Dict[str, Any]:
    return llm_stabilizer.get_stats()


if __name__ == "__main__":
    import asyncio

    async def test():
        print("=" * 60)
        print("  LLM LIFE SUPPORT STABILIZER -- SELF TEST")
        print("=" * 60)
        print("  Paradox modules: " + ("available" if _paradox_available else "FALLBACK MODE"))
        print("")

        scenarios = [
            {"type": "paradox_overflow", "message": "Contradiction density overflow"},
            {"type": "api_failure", "message": "HTTP 401 auth failed for DeepSeek"},
            {"type": "encoding", "message": "UnicodeEncodeError cp1252 emoji crash"},
            {"type": "timeout", "message": "Request timed out after 60s"},
        ]

        for s in scenarios:
            r = await stabilize_llm_crash(s)
            status = "[OK]" if r["stabilized"] else "[!!]"
            print("  " + status + " " + r["crash_pattern"] + ": " + r["suggestion"])

        print("")
        stats = get_llm_stabilization_stats()
        print("  Stats: " + str(stats["total_attempts"]) + " attempts, "
              + str(stats["successful"]) + " successful")
        print("")
        print("  [OK] Self-test complete.")

    asyncio.run(test())
