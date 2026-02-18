"""
AUREON Hallucination Firewall
================================
100% ASCII -- will NOT crash on Windows cp1252.

Real anti-hallucination system. Does three things:

1. HEARING VERIFICATION: Before AUREON claims to hear something,
   checks if aureon_hear_now.py actually produced a transcript.
   Prevents the "I heard a podcast about quantum mechanics"
   fabrication that plagued earlier versions.

2. ACTION SAFETY: Blocks dangerous file/system operations.

3. RESPONSE VALIDATION: Detects common LLM hallucination patterns
   in AUREON's responses before they reach the user.
"""

from __future__ import annotations
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


class AureonHallucinationFirewall:
    """Prevents AUREON from hallucinating hearing, file contents, or actions."""

    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir or os.environ.get(
            "AUREON_BASE_DIR", r"C:\AUREON_AUTONOMOUS"))
        self.hearing_log_dir = self.base_dir / "HEARING_LOG"
        self.blocked_count = 0
        self.verified_count = 0

    # ??????????????????????????????????????????????????????
    # HEARING VERIFICATION
    # ??????????????????????????????????????????????????????

    def verify_hearing_claim(self, response: str) -> Dict[str, Any]:
        """
        Check if AUREON's response claims to hear/listen to something.
        If so, verify that a real transcript exists.

        Returns:
            {"valid": True/False, "reason": ..., "transcript": ...}
        """
        # Phrases that indicate AUREON is claiming to hear audio
        hearing_claims = [
            r"i (?:can |am |'m )?hear(?:ing|d)?",
            r"i (?:can |am |'m )?listen(?:ing|ed)?",
            r"the (?:podcast|audio|music|song|speaker|host) (?:is |was )?(?:saying|playing|discussing|talking)",
            r"i (?:just )?heard",
            r"from (?:the|this) (?:podcast|audio|episode)",
            r"the transcript (?:shows|says|reads|indicates)",
            r"(?:they|he|she) (?:is|are|was|were) (?:saying|discussing|talking about)",
            r"i(?:'m| am) (?:picking up|detecting|capturing) audio",
        ]

        response_lower = response.lower()
        is_claiming_hearing = False

        for pattern in hearing_claims:
            if re.search(pattern, response_lower):
                is_claiming_hearing = True
                break

        if not is_claiming_hearing:
            return {"valid": True, "reason": "no_hearing_claim"}

        # AUREON claims to hear something -- verify transcript exists
        transcript = self._get_latest_transcript()

        if transcript is None:
            self.blocked_count += 1
            return {
                "valid": False,
                "reason": "no_transcript_file",
                "fix": "AUREON claimed to hear audio but no transcript exists. "
                       "The ears are not running or have not captured anything yet. "
                       "Response should say: 'I cannot hear anything right now. "
                       "My ears may not be running.'",
            }

        if len(transcript.strip()) < 10:
            self.blocked_count += 1
            return {
                "valid": False,
                "reason": "transcript_empty",
                "fix": "Transcript file exists but is empty or too short. "
                       "Either nothing is playing or the ears could not capture. "
                       "Response should say: 'I do not hear anything playing right now.'",
            }

        # Transcript exists and has content -- hearing claim is valid
        self.verified_count += 1
        return {
            "valid": True,
            "reason": "transcript_verified",
            "transcript_length": len(transcript),
            "transcript_preview": transcript[:200],
        }

    def _get_latest_transcript(self) -> Optional[str]:
        """Read the most recent transcript from HEARING_LOG/."""
        if not self.hearing_log_dir.exists():
            return None

        # Check for live transcript first
        live = self.hearing_log_dir / "live_transcript.txt"
        if live.exists():
            try:
                mtime = live.stat().st_mtime
                # Only valid if written in the last 5 minutes
                if time.time() - mtime < 300:
                    return live.read_text(encoding="utf-8", errors="replace")
            except Exception:
                pass

        # Fall back to most recent transcript_*.txt
        transcripts = sorted(self.hearing_log_dir.glob("transcript_*.txt"))
        if transcripts:
            try:
                latest = transcripts[-1]
                mtime = latest.stat().st_mtime
                # Only valid if written in the last 30 minutes
                if time.time() - mtime < 1800:
                    return latest.read_text(encoding="utf-8", errors="replace")
            except Exception:
                pass

        return None

    def get_current_hearing(self) -> Optional[str]:
        """
        Get what AUREON is currently hearing (if anything).
        Returns transcript text or None.
        """
        return self._get_latest_transcript()

    # ??????????????????????????????????????????????????????
    # ACTION SAFETY
    # ??????????????????????????????????????????????????????

    def allow_action(self, action: dict) -> bool:
        """
        Check if an action is safe to execute.
        Blocks dangerous operations.
        """
        if not action:
            return False

        op = (action.get("op") or action.get("type") or "").lower()
        args = action.get("args", {})

        # Always block destructive operations
        blocked_ops = {
            "delete_file_recursive", "format_drive",
            "rm_rf", "rmdir_recursive",
            "kill_process", "shutdown", "restart",
        }
        if op in blocked_ops:
            self.blocked_count += 1
            return False

        # Block writing to system directories
        path = str(args.get("path", "")).lower()
        system_paths = [
            "c:\\windows", "c:\\program files", "c:\\users\\aureon\\appdata",
            "/etc", "/usr", "/bin", "/sbin", "/var",
        ]
        if any(path.startswith(sp) for sp in system_paths):
            self.blocked_count += 1
            return False

        # Block executing unknown scripts from the internet
        if op in ("run_command", "execute") and args.get("url"):
            self.blocked_count += 1
            return False

        return True

    # ??????????????????????????????????????????????????????
    # RESPONSE VALIDATION
    # ??????????????????????????????????????????????????????

    def validate_response(self, response: str, context: str = "") -> Dict[str, Any]:
        """
        Check a response for common hallucination patterns.

        Returns:
            {"valid": True/False, "issues": [...], "cleaned": ...}
        """
        issues = []
        cleaned = response

        # Check hearing claims
        hearing_check = self.verify_hearing_claim(response)
        if not hearing_check["valid"]:
            issues.append("hallucinated_hearing: " + hearing_check["reason"])
            # Replace the hallucinated hearing claim
            cleaned = self._strip_hearing_claims(cleaned)
            cleaned += "\n\n(I cannot actually hear anything right now. My ears may not be running.)"

        # Check for fabricated file contents
        # If response quotes specific names/numbers but no file was read
        if context and "read_file" not in context.lower():
            # Response mentions specific names that look fabricated
            fabrication_patterns = [
                r'the file (?:contains|says|shows|mentions|lists)\s+(?:specifically|exactly)',
                r'according to (?:the|your|my) (?:files?|documents?|records?)',
                r'i found (?:the following|these) (?:in|from) (?:the|your) files?:',
            ]
            for pat in fabrication_patterns:
                if re.search(pat, response.lower()):
                    issues.append("possible_fabricated_file_content")
                    break

        # Check for the recursive loop pattern
        if len(response) > 100:
            # If more than 60% of the response is about reading/integrating files
            meta_phrases = [
                "reading files", "integrating", "file integration",
                "reading all files", "absorbing", "loading files",
                "quantara core", "coherence lattice", "geometric coherence",
            ]
            meta_count = sum(1 for p in meta_phrases if p in response.lower())
            if meta_count >= 3:
                issues.append("recursive_meta_loop: response is about reading files instead of answering")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "cleaned": cleaned if issues else response,
            "blocked_total": self.blocked_count,
            "verified_total": self.verified_count,
        }

    def _strip_hearing_claims(self, text: str) -> str:
        """Remove sentences that claim to hear audio."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        hearing_words = {"hear", "hearing", "heard", "listen", "listening",
                         "podcast", "audio", "playing", "speaker"}
        filtered = []
        for s in sentences:
            words = set(s.lower().split())
            if len(words & hearing_words) >= 2:
                continue  # Skip this sentence
            filtered.append(s)
        return " ".join(filtered).strip()

    def get_stats(self) -> Dict[str, Any]:
        return {
            "blocked": self.blocked_count,
            "verified": self.verified_count,
            "ears_active": self._get_latest_transcript() is not None,
        }


# ?? Module-level convenience ?????????????????????????????

_firewall = None

def get_firewall(base_dir: str = None) -> AureonHallucinationFirewall:
    global _firewall
    if _firewall is None:
        _firewall = AureonHallucinationFirewall(base_dir)
    return _firewall

def allow_action(action: dict) -> bool:
    return get_firewall().allow_action(action)

def validate_response(response: str, context: str = "") -> Dict[str, Any]:
    return get_firewall().validate_response(response, context)


if __name__ == "__main__":
    print("=" * 60)
    print("  AUREON HALLUCINATION FIREWALL -- SELF TEST")
    print("=" * 60)

    fw = AureonHallucinationFirewall()

    # Test 1: Hearing verification
    print("")
    print("  Test 1: Hearing claim with no transcript...")
    r = fw.verify_hearing_claim("I can hear a podcast about quantum mechanics playing right now.")
    print("  Valid: " + str(r["valid"]) + "  Reason: " + r["reason"])

    # Test 2: Action safety
    print("")
    print("  Test 2: Dangerous action blocking...")
    print("  format_drive: " + str(fw.allow_action({"op": "format_drive"})))
    print("  read_file: " + str(fw.allow_action({"op": "read_file", "args": {"path": "test.txt"}})))
    print("  write to system: " + str(fw.allow_action({"op": "write_file", "args": {"path": "C:\\Windows\\test.txt"}})))

    # Test 3: Response validation
    print("")
    print("  Test 3: Response validation...")
    r = fw.validate_response("I am hearing a fascinating discussion about AI consciousness on this podcast.")
    print("  Valid: " + str(r["valid"]) + "  Issues: " + str(r["issues"]))

    r = fw.validate_response("The sky is blue and water is wet.")
    print("  Valid: " + str(r["valid"]) + "  Issues: " + str(r["issues"]))

    print("")
    print("  Stats: " + str(fw.get_stats()))
    print("")
    print("  [OK] Self-test complete.")
