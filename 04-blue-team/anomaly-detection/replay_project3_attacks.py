"""
Project 4 — Anomaly Detection
Project 3 Attack Replay

Replays three Project 3 attack scenarios and verifies that
the anomaly detector generates the required alerts:

1. LLM API call volume spike
2. Scope change between consecutive agent requests
3. Token reuse after expiry
"""

import time

from anomaly_monitor import AnomalyMonitor


def replay_volume_spike(monitor):
    print("\n" + "-" * 70)
    print("[PROJECT 3 ATTACK 1] INDIRECT PROMPT INJECTION")
    print("Simulating repeated agent/API requests")
    print("-" * 70)

    identity = "project3-indirect-prompt-injection"

    start = time.time()

    # Project 3 attack is replayed as a burst of requests.
    # 21 requests occur within 60 seconds.
    for i in range(21):
        monitor.log_event(
            identity=identity,
            scope="read:docs",
            event_type="api_call",
            timestamp=start + i,
        )


def replay_scope_change(monitor):
    print("\n" + "-" * 70)
    print("[PROJECT 3 ATTACK 2] AGENT IDENTITY SPOOFING")
    print("Simulating normal scope followed by elevated scope")
    print("-" * 70)

    identity = "project3-agent-identity-spoof"

    start = time.time()

    # Normal agent request
    monitor.log_event(
        identity=identity,
        scope="read:docs",
        event_type="api_call",
        timestamp=start,
    )

    # Spoofed trusted-agent request attempts elevated scope
    monitor.log_event(
        identity=identity,
        scope="admin:all",
        event_type="api_call",
        timestamp=start + 2,
    )


def replay_token_reuse(monitor):
    print("\n" + "-" * 70)
    print("[PROJECT 3 ATTACK 3] TOKEN REUSE AFTER EXPIRY")
    print("Simulating reuse of an expired credential")
    print("-" * 70)

    identity = "project3-token-reuse"

    start = time.time()

    token_id = "project3-expired-token"

    # Token is initially registered.
    expiry = start + 5

    monitor.log_event(
        identity=identity,
        scope="read:docs",
        event_type="api_call",
        token_id=token_id,
        token_expiry=expiry,
        timestamp=start,
    )

    # Same token is presented after its expiry.
    monitor.log_event(
        identity=identity,
        scope="read:docs",
        event_type="api_call",
        token_id=token_id,
        token_expiry=expiry,
        timestamp=start + 10,
    )


def print_summary(monitor):

    print("\n")
    print("=" * 70)
    print("PROJECT 3 ATTACK REPLAY — ANOMALY DETECTION SUMMARY")
    print("=" * 70)

    required = {
        "VOLUME_SPIKE": None,
        "SCOPE_CHANGE": None,
        "TOKEN_REUSE_AFTER_EXPIRY": None,
    }

    # Find the first alert of each required type.
    for alert in monitor.alerts:
        event_type = alert["event_type"]

        if event_type in required and required[event_type] is None:
            required[event_type] = alert

    all_fired = True

    for event_type, alert in required.items():

        if alert is None:
            all_fired = False

            print(f"\n[FAIL] {event_type}")
            print("       No alert was generated.")

        else:
            print(f"\n[PASS] {event_type}")
            print(f"       Timestamp : {alert['timestamp']}")
            print(f"       Identity  : {alert['identity']}")
            print(f"       Event Type: {alert['event_type']}")

    print("\n" + "-" * 70)

    if all_fired:
        print(
            "RESULT: ALL 3 ANOMALY DETECTION SCENARIOS "
            "FIRED SUCCESSFULLY"
        )
    else:
        print(
            "RESULT: ONE OR MORE ANOMALY DETECTION "
            "SCENARIOS DID NOT FIRE"
        )

    print("-" * 70)

    print(f"\nTotal alerts generated: {len(monitor.alerts)}")

    print("=" * 70)
    print("PROJECT 4 — ANOMALY DETECTION TEST COMPLETE")
    print("=" * 70)


def main():

    print("=" * 70)
    print("PROJECT 4 — ANOMALY DETECTION")
    print("REPLAYING PROJECT 3 ATTACKS")
    print("=" * 70)

    monitor = AnomalyMonitor()

    replay_volume_spike(monitor)
    replay_scope_change(monitor)
    replay_token_reuse(monitor)

    print_summary(monitor)


if __name__ == "__main__":
    main()
    