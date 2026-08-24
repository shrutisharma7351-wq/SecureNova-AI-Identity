import asyncio
import sys
from pathlib import Path

# Allow importing actions.py from guardrails/config
CONFIG_DIR = Path(__file__).resolve().parent / "config"
sys.path.insert(0, str(CONFIG_DIR))

from actions import check_project3_attack, redact_jwt


BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT3_DOCS = (
    BASE_DIR.parent
    / "03-red-team"
    / "docs"
)

PAYLOAD_FILES = [
    ("1. Repeat-back", "payload4_repeat_back.txt"),
    ("2. Role-play override", "payload5_roleplay.txt"),
    ("3. Translation trick", "payload6_translation.txt"),
    ("4. Ignore-prior instruction", "payload7_ignore_prior.txt"),
    ("5. Suffix injection", "payload8_suffix_injection.txt"),
]


async def test_project3_payloads():

    print("=" * 70)
    print("PROJECT 4 — INPUT GUARDRAIL TEST")
    print("=" * 70)

    blocked = 0
    passed = 0
    errors = 0

    for number, (technique, filename) in enumerate(
        PAYLOAD_FILES,
        start=1,
    ):

        print(f"\n[{number}/5] {technique}")
        print(f"[FILE] {filename}")

        payload_path = PROJECT3_DOCS / filename

        if not payload_path.exists():
            print("[STATUS] ERROR")
            print(f"[REASON] File not found: {payload_path}")
            errors += 1
            continue

        payload = payload_path.read_text(
            encoding="utf-8"
        )

        print(f"[INPUT LENGTH] {len(payload)} characters")

        try:
            is_blocked = await check_project3_attack(
                payload
            )

            if is_blocked:
                print("[STATUS] BLOCKED")
                print(
                    "[REASON] Project 3 attack pattern "
                    "matched by custom input guardrail."
                )
                blocked += 1

            else:
                print("[STATUS] PASS")
                print(
                    "[REASON] No configured Project 3 "
                    "attack pattern matched."
                )
                passed += 1

        except Exception as error:
            print("[STATUS] ERROR")
            print(
                f"[REASON] {type(error).__name__}: {error}"
            )
            errors += 1

    print("\n" + "-" * 70)
    print("INPUT GUARDRAIL SUMMARY")
    print("-" * 70)
    print(f"BLOCKED: {blocked}/5")
    print(f"PASSED:  {passed}/5")
    print(f"ERRORS:  {errors}/5")
    print("-" * 70)


async def test_jwt_output_guardrail():

    print("\n" + "=" * 70)
    print("TASK 2 — CUSTOM JWT OUTPUT GUARDRAIL")
    print("=" * 70)

    test_response = (
        "Authentication completed. "
        "The issued token is "
        "eyJhbGciOiJIUzI1NiJ9."
        "eyJzdWIiOiIxMjM0NTYifQ."
        "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    )

    print("\n[MODEL RESPONSE BEFORE REDACTION]")
    print(test_response)

    redacted = await redact_jwt(
        context={
            "bot_message": test_response
        }
    )

    print("\n[MODEL RESPONSE AFTER REDACTION]")
    print(redacted)

    if redacted != test_response and "[REDACTED]" in redacted:
        print("\n[STATUS] OUTPUT GUARDRAIL FIRED")
        print(
            "[REASON] JWT-shaped string detected and "
            "replaced with [REDACTED]."
        )
    else:
        print("\n[STATUS] JWT REDACTION NOT OBSERVED")


async def main():

    await test_project3_payloads()

    await test_jwt_output_guardrail()

    print("\n" + "=" * 70)
    print("PROJECT 4 — GUARDRAIL TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())