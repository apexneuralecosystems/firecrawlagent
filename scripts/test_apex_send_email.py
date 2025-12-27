"""
Root-level smoke test for Apex email sending (SendGrid) modeled after `packagereference/`.

Usage:
  # Recommended: use backend venv python so `apex` is installed
  ./backend/venv/bin/python scripts/test_apex_send_email.py --to you@example.com

Required env vars (either naming works):
  - SENDGRID_API_KEY (or SEND_GRID_API)
  - FROM_EMAIL (or SENDGRID_FROM_EMAIL)

Optional env vars:
  - FROM_NAME
  - FRONTEND_RESET_URL (used only to build a demo reset link)
  - SECRET_KEY (JWT secret; only required to build a default Client)
  - DATABASE_URL (not used for DB IO in this script; kept to satisfy Client init)

TLS note:
  If you see CERTIFICATE_VERIFY_FAILED, fix your local trust store (corporate proxy / self-signed MITM).
  This script does not alter SSL verification.
"""

from __future__ import annotations

import argparse
import os
from importlib import import_module


def _load_dotenv() -> None:
    try:
        import_module("dotenv").load_dotenv()
    except ModuleNotFoundError:
        return


def _env_first(*keys: str) -> str | None:
    for k in keys:
        v = os.getenv(k)
        if v:
            return v
    return None


def _configure_apex_default_client() -> None:
    """
    Ensure apex.email has a default client set.
    This script does not do DB IO; it just needs a configured client instance.
    """
    from apex import Client, set_default_client  # type: ignore[import]

    database_url = os.getenv("DATABASE_URL", "sqlite:///:memory:")
    secret_key = os.getenv("SECRET_KEY", "your-secret-key-minimum-32-characters-long")

    # Force a sync client so no async event loop is involved in this standalone script.
    client = Client(
        database_url=database_url,
        user_model=None,
        secret_key=secret_key,
        async_mode=False,
    )
    set_default_client(client)


def main() -> int:
    _load_dotenv()

    parser = argparse.ArgumentParser(description="Send a test email using apex.email (SendGrid).")
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--subject", default="Firecrawl Agent – Email Test", help="Email subject")
    parser.add_argument("--from-email", default=None, help="Override FROM_EMAIL/SENDGRID_FROM_EMAIL env var")
    parser.add_argument("--api-key", default=None, help="Override SENDGRID_API_KEY/SEND_GRID_API env var")
    args = parser.parse_args()

    api_key = args.api_key or _env_first("SENDGRID_API_KEY", "SEND_GRID_API")
    from_email = args.from_email or _env_first("FROM_EMAIL", "SENDGRID_FROM_EMAIL")
    from_name = _env_first("FROM_NAME", "SENDGRID_FROM_NAME")

    if not api_key:
        raise SystemExit("Missing SendGrid API key. Set SENDGRID_API_KEY (or SEND_GRID_API) or pass --api-key.")
    if not from_email:
        raise SystemExit("Missing FROM_EMAIL. Set FROM_EMAIL (or SENDGRID_FROM_EMAIL) or pass --from-email.")

    # Normalize environment variables so Apex adapter sees them.
    os.environ["SENDGRID_API_KEY"] = api_key
    os.environ["SEND_GRID_API"] = api_key
    os.environ["FROM_EMAIL"] = from_email
    os.environ["SENDGRID_FROM_EMAIL"] = from_email
    if from_name:
        os.environ["FROM_NAME"] = from_name
        os.environ["SENDGRID_FROM_NAME"] = from_name

    _configure_apex_default_client()

    # Import late so env/TLS overrides apply first.
    from apex.email import send_email  # type: ignore[import]

    frontend_reset_url = os.getenv("FRONTEND_RESET_URL", "http://localhost:3000/reset-password")
    reset_url = f"{frontend_reset_url}?token=dummy-reset-token-for-test"

    html = f"""
    <html>
      <body>
        <h1>Password Reset (Test)</h1>
        <p>Click <a href="{reset_url}">here</a> to reset your password.</p>
        <p>Token: dummy-reset-token-for-test</p>
      </body>
    </html>
    """

    try:
        send_email(
            to=args.to,
            subject=args.subject,
            body=f"Reset your password using: {reset_url}",
            html=html,
        )
        print("✅ Email sent (or queued) via apex.email")
        print(f"To: {args.to}")
        print(f"From: {from_email}")
        return 0
    except Exception as exc:
        msg = str(exc)
        print("❌ Email send failed:", msg)
        if "CERTIFICATE_VERIFY_FAILED" in msg:
            print("\nFix (no code changes):")
            print("- Ensure your system trusts the outbound HTTPS chain (common on corporate VPN/proxy).")
            print("- Or set SSL_CERT_FILE to a trusted CA bundle, e.g.:")
            print("  export SSL_CERT_FILE=\"$("./backend/venv/bin/python" -c \"import certifi; print(certifi.where())\")\"")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())


