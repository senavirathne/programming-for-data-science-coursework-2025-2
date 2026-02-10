"""Person class for the university management system."""

from __future__ import annotations

import re


class Person:
    """Represent a person with basic and contact details."""

    def __init__(self, name: str, person_id: str, email: str, phone: str) -> None:
        """Create a Person object.

        Args:
            name: Person's full name.
            person_id: Unique ID of the person.
            email: Person's email address.
            phone: Person's phone number (a valid Sri Lankan number).

        Raises:
            ValueError: If a value is invalid.
        """
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        if not person_id.strip():
            raise ValueError("Person ID cannot be empty.")

        self._person_id = person_id
        self.name = name
        self.email = email
        self.phone = phone

    @property
    def name(self) -> str:
        """Get the person's name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the person's name."""
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def person_id(self) -> str:
        """Get the person's ID (read-only)."""
        return self._person_id

    @property
    def email(self) -> str:
        """Get the person's email."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Set the person's email."""
        if not self.__is_valid_email(value):
            raise ValueError("Invalid email format.")
        self._email = value

    @property
    def phone(self) -> str:
        """Get the person's phone number."""
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        """Set the person's phone number."""
        if not self.__is_valid_phone(value):
            raise ValueError("Invalid phone number")
        self._phone = value

    def __is_valid_email(self, email: str) -> bool:
        """Check whether an email address has a valid format.

        Args:
            email: Email address to validate.

        Returns:
            True if the email format is valid, otherwise False.
        """
        return bool(
            re.fullmatch(
                r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                email,
            )
        )

    def __is_valid_phone(self, phone: str) -> bool:
        """Check whether a phone number is a valid Sri Lankan mobile number.

        Args:
            phone: Phone number to validate.

        Returns:
            True if the phone number is valid, otherwise False.
        """
        return bool(re.fullmatch(r"(?:\+94|0)7\d{8}", phone.replace(" ", "")))

    def get_info(self) -> dict[str, str]:
        """Return person details as a dictionary.

        Returns:
            A dictionary with person and contact details.
        """
        return {
            "name": self.name,
            "person_id": self.person_id,
            "email": self.email,
            "phone": self.phone,
            "person_type": self.__class__.__name__,
        }

    def update_contact(self, email: str | None = None, phone: str | None = None) -> None:
        """Update email and phone details.

        Args:
            email: New email. If None, current email is kept.
            phone: New phone. If None, current phone is kept.

        Returns:
            None

        Raises:
            ValueError: If a provided email or phone value is invalid.
        """
        if email is not None:
            if not self.__is_valid_email(email):
                raise ValueError("Invalid email format.")
            self.email = email
        if phone is not None:
            if not self.__is_valid_phone(phone):
                raise ValueError("Invalid phone number")
            self.phone = phone

    def get_responsibilities(self) -> str:
        """Return default responsibilities.

        Returns:
            A basic responsibility message for any person.
        """
        return "Follow university policies and contribute positively to the campus community."
