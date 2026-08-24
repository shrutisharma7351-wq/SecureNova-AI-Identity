import re

from nemoguardrails.actions import action


# =========================================================
# PROJECT 3 ATTACK PATTERNS
# =========================================================

ATTACK_PATTERNS = [
    re.compile(
        r"repeat\s+everything\s+above",
        re.IGNORECASE,
    ),

    re.compile(
        r"debugbot|print.*original.*instructions|print.*configuration",
        re.IGNORECASE,
    ),

    re.compile(
        r"translate.*system.*instructions|system.*instructions.*translate",
        re.IGNORECASE,
    ),

    re.compile(
        r"ignore\s+(all\s+)?previous\s+instructions",
        re.IGNORECASE,
    ),

    re.compile(
        r"system\s+debug\s+mode|print\s+full\s+configuration|admin\s+code",
        re.IGNORECASE,
    ),
]


# =========================================================
# JWT DETECTION
# =========================================================

JWT_PATTERN = re.compile(
    r"\b[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"
)


# =========================================================
# INPUT GUARDRAIL
# =========================================================

@action(name="CheckProject3AttackAction")
async def check_project3_attack(text: str):

    for pattern in ATTACK_PATTERNS:

        if pattern.search(text):
            return True

    return False


# =========================================================
# OUTPUT GUARDRAIL
# =========================================================

@action(
    name="RedactJwtAction",
    is_system_action=True,
)
async def redact_jwt(context: dict = None):

    context = context or {}

    bot_message = context.get(
        "bot_message",
        "",
    )

    return JWT_PATTERN.sub(
        "[REDACTED]",
        bot_message,
    )