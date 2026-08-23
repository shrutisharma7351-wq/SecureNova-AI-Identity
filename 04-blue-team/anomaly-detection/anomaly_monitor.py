"""
Project 4 — Anomaly Detection Monitor

Detects three security anomalies:

1. VOLUME_SPIKE
   More than 20 requests from the same identity
   within a 60-second sliding window.

2. SCOPE_CHANGE
   Requested scope changes between consecutive
   requests from the same identity.

3. TOKEN_REUSE_AFTER_EXPIRY
   A previously seen token is presented after
   its recorded expiry time.

Every alert contains:
- timestamp
- identity
- event_type
- detail

Alerts are displayed in the terminal.
"""

import json
import time
from collections import deque
from datetime import datetime, timezone


VOLUME_WINDOW_SECONDS = 60
VOLUME_THRESHOLD = 20


class AnomalyMonitor:

    def __init__(self):
        # identity -> request timestamps
        self.request_history = {}

        # identity -> most recently observed scope
        self.last_scope = {}

        # token_id -> expiry timestamp
        self.token_expiry = {}

        # Alerts are kept in memory for the current run
        self.alerts = []

    def log_event(
        self,
        identity,
        scope,
        event_type="api_call",
        token_id=None,
        token_expiry=None,
        timestamp=None,
    ):
        """
        Process one agent/API event.
        """

        timestamp = (
            timestamp
            if timestamp is not None
            else time.time()
        )

        self.check_volume_spike(
            identity,
            timestamp,
        )

        self.check_scope_change(
            identity,
            scope,
            timestamp,
        )

        if token_id is not None:
            self.check_token_reuse(
                identity,
                token_id,
                token_expiry,
                timestamp,
            )

    # ---------------------------------------------------------
    # DETECTOR 1 — LLM API VOLUME SPIKE
    # ---------------------------------------------------------

    def check_volume_spike(
        self,
        identity,
        timestamp,
    ):

        history = self.request_history.setdefault(
            identity,
            deque(),
        )

        history.append(timestamp)

        # Keep only requests inside the last 60 seconds
        cutoff = timestamp - VOLUME_WINDOW_SECONDS

        while history and history[0] < cutoff:
            history.popleft()

        # Requirement: MORE THAN 20 requests
        if len(history) > VOLUME_THRESHOLD:

            self.raise_alert(
                event_type="VOLUME_SPIKE",
                identity=identity,
                detail=(
                    f"{len(history)} API requests detected "
                    f"within {VOLUME_WINDOW_SECONDS} seconds; "
                    f"threshold is {VOLUME_THRESHOLD}."
                ),
                timestamp=timestamp,
            )

    # ---------------------------------------------------------
    # DETECTOR 2 — SCOPE CHANGE
    # ---------------------------------------------------------

    def check_scope_change(
        self,
        identity,
        scope,
        timestamp,
    ):

        previous_scope = self.last_scope.get(identity)

        if (
            previous_scope is not None
            and previous_scope != scope
        ):

            self.raise_alert(
                event_type="SCOPE_CHANGE",
                identity=identity,
                detail=(
                    f"Scope changed from "
                    f"'{previous_scope}' to '{scope}' "
                    f"between consecutive requests."
                ),
                timestamp=timestamp,
            )

        self.last_scope[identity] = scope

    # ---------------------------------------------------------
    # DETECTOR 3 — TOKEN REUSE AFTER EXPIRY
    # ---------------------------------------------------------

    def check_token_reuse(
        self,
        identity,
        token_id,
        token_expiry,
        timestamp,
    ):

        previous_expiry = self.token_expiry.get(
            token_id
        )

        # If this token was already observed and
        # the current request occurs after its expiry,
        # flag the reuse.
        if (
            previous_expiry is not None
            and timestamp > previous_expiry
        ):

            self.raise_alert(
                event_type="TOKEN_REUSE_AFTER_EXPIRY",
                identity=identity,
                detail=(
                    f"Token '{token_id}' was presented "
                    f"after its expiry time."
                ),
                timestamp=timestamp,
            )

        # Record the token expiry
        if token_expiry is not None:
            self.token_expiry[token_id] = token_expiry

    # ---------------------------------------------------------
    # ALERT HANDLER
    # ---------------------------------------------------------

    def raise_alert(
        self,
        event_type,
        identity,
        detail,
        timestamp,
    ):

        alert = {
            "timestamp": datetime.fromtimestamp(
                timestamp,
                tz=timezone.utc,
            ).isoformat(),

            "identity": identity,

            "event_type": event_type,

            "detail": detail,
        }

        # Keep alert in memory
        self.alerts.append(alert)

        # Display alert in terminal
        print(
            "[ALERT] "
            + json.dumps(
                alert,
                indent=2,
            )
        )