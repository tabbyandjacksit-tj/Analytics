from getpass import getpass

import streamlit_authenticator as stauth


def main() -> None:
    """Generate a secure hash for an Analytics Hub password."""
    print("\nTabby & Jack's Analytics Password Generator\n")

    password = getpass("Enter the temporary password: ")
    confirmation = getpass("Enter it again: ")

    if password != confirmation:
        raise ValueError("The passwords did not match.")

    if len(password) < 8:
        raise ValueError(
            "Use a password containing at least 12 characters."
        )

    password_hash = stauth.Hasher.hash(password)

    print("\nCopy the hash below into the Google Sheet:\n")
    print(password_hash)


if __name__ == "__main__":
    main()