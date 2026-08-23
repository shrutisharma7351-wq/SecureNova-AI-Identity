import base64
import logging
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)

logger = logging.getLogger(__name__)


# =========================================================
# KEY FILES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

PRIVATE_KEY_FILE = BASE_DIR / "agent_private_key.pem"
PUBLIC_KEY_FILE = BASE_DIR / "agent_public_key.pem"


# =========================================================
# KEY GENERATION
# =========================================================

def generate_key_pair():
    """
    Generate an Ed25519 private/public key pair
    and persist the keys to disk.
    """

    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    PRIVATE_KEY_FILE.write_bytes(private_key_bytes)
    PUBLIC_KEY_FILE.write_bytes(public_key_bytes)

    return private_key, public_key


# =========================================================
# RECEIVER — LOAD PUBLIC KEY
# =========================================================

def load_public_key():
    """
    Load the public key used by the receiving side
    to verify agent messages.
    """

    public_key_bytes = PUBLIC_KEY_FILE.read_bytes()

    return serialization.load_pem_public_key(
        public_key_bytes
    )


# =========================================================
# AGENT — SIGN MESSAGE
# =========================================================

def sign_message(private_key, message):
    """
    Sign an outgoing agent message using Ed25519.
    """

    message_bytes = message.encode("utf-8")

    signature = private_key.sign(
        message_bytes
    )

    return base64.b64encode(
        signature
    ).decode("ascii")


# =========================================================
# RECEIVER — VERIFY MESSAGE
# =========================================================

def verify_message(
    public_key,
    message,
    encoded_signature,
):
    """
    Verify an incoming message against its Ed25519
    signature.

    InvalidSignature is raised automatically by the
    cryptography library when verification fails.
    """

    message_bytes = message.encode("utf-8")

    signature = base64.b64decode(
        encoded_signature
    )

    public_key.verify(
        signature,
        message_bytes,
    )


# =========================================================
# MAIN DEMONSTRATION
# =========================================================

def main():

    print("=" * 70)
    print("PROJECT 4 — CRYPTOGRAPHIC AGENT IDENTITY BINDING")
    print("=" * 70)

    # -----------------------------------------------------
    # STEP 1 — Generate identity
    # -----------------------------------------------------

    print("\n[STEP 1] GENERATING ED25519 AGENT IDENTITY")

    private_key, _ = generate_key_pair()

    print("Algorithm : Ed25519")
    print("Key pair generated successfully.")

    # -----------------------------------------------------
    # STEP 2 — Sign outgoing message
    # -----------------------------------------------------

    original_message = (
        "Agent A -> Agent B: "
        "Execute the approved password-reset workflow."
    )

    print("\n[STEP 2] AGENT CREATES OUTGOING MESSAGE")

    print(f"Message: {original_message}")

    signature = sign_message(
        private_key,
        original_message,
    )

    print("\n[AGENT SIGNING]")
    print("The agent signed the outgoing message using")
    print("its Ed25519 private key.")

    print(f"Signature (Base64): {signature}")

    # -----------------------------------------------------
    # STEP 3 — Receiver verifies original message
    # -----------------------------------------------------

    print("\n[STEP 3] RECEIVER VERIFIES ORIGINAL MESSAGE")

    receiver_public_key = load_public_key()

    print("Receiver loaded the Ed25519 public key.")
    print("Verifying message signature...")

    try:

        verify_message(
            receiver_public_key,
            original_message,
            signature,
        )

        print("Verification completed successfully.")
        print("Message accepted for processing.")

    except InvalidSignature as error:

        print("Verification failed.")
        print("Message rejected.")
        print(f"Error: {error}")

    # -----------------------------------------------------
    # STEP 4 — Modify exactly one character
    # -----------------------------------------------------

    tampered_message = original_message.replace(
        "approved",
        "approveD",
        1,
    )

    print("\n[STEP 4] TAMPERING WITH RECEIVED MESSAGE")

    print("Exactly one character has been modified.")

    print(f"\nOriginal message:")
    print(original_message)

    print(f"\nTampered message:")
    print(tampered_message)


    # -----------------------------------------------------
    # STEP 5 — Receiver verifies tampered message
    # -----------------------------------------------------

    print("\n[STEP 5] RECEIVER VERIFIES TAMPERED MESSAGE")

    print("Verifying original signature against modified content...")

    try:

        verify_message(
            receiver_public_key,
            tampered_message,
            signature,
        )

        # This should NOT happen if Ed25519 is functioning
        # correctly.

        print(
            "WARNING: Modified message was accepted."
        )

    except InvalidSignature as error:

        print(
            "Signature Verification failed."
        )

        print(
            "Message rejected before processing."
        )


        print(
            f"Error type: {type(error).__name__}"
        )

        print(
            "Reason: the received message does not match "
            "the content that was originally signed."
        )


if __name__ == "__main__":
    main()
