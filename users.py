"""
Who can sign in.

Two shared logins only: one for the Kenja team, one for anybody from the Times of
India. Passwords are stored as a SHA256 hash so they are not sitting in plain text
in the repository, but this is a prototype sign in, not real authentication, and
nobody should treat it as such. Before a client uses this for real work, move the
accounts into a database and put a proper identity provider in front of it.

To change a password, run
    python -c "import hashlib;print(hashlib.sha256('newpassword'.encode()).hexdigest())"
and paste the hash below, or set it in Streamlit Secrets so no commit is needed.
"""

import hashlib


def _h(p):
    return hashlib.sha256(p.encode()).hexdigest()


# username: (password hash, display name, side)
ACCOUNTS = {
    "kenja": (_h("Kenja2026.demo"), "Kenja team", "Kenja"),
    "toi":   (_h("Times2026.guest"), "Times of India", "Guest"),
}
