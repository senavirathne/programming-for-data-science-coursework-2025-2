"""Person class for the university management system."""

from __future__ import annotations


class Person:
    """Represent a person with basic and contact details."""

    def __init__(self, name: str, person_id: str, email: str, phone: str) -> None:
        """Create a Person object.

        Args:
            name: Person's full name.
            person_id: Unique ID of the person.
            email: Person's email address.
            phone: Person's phone number.

        Raises:
            ValueError: If a value is invalid.
            TypeError: If a value is of the wrong type.
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not isinstance(person_id, str):
            raise TypeError("Person ID must be a string.")
        if not isinstance(email, str):
            raise TypeError("Email must be a string.")
        if not isinstance(phone, str):
            raise TypeError("Phone must be a string.")

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
        """Set the person's name.
        
        Args:
            value: New name.

        Raises:
            ValueError: If the name is empty.
            TypeError: If the name is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
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
        """Set the person's email.
        
        Args:
            value: New email address.
            
        Raises:
            TypeError: If the email is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("Email must be a string.")
        self._email = value

    @property
    def phone(self) -> str:
        """Get the person's phone number."""
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        """Set the person's phone number.
        
        Args:
            value: New phone number.
            
        Raises:
            TypeError: If the phone is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("Phone must be a string.")
        self._phone = value

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
        """
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone

    def get_responsibilities(self) -> str:
        """Return default responsibilities.

        Returns:
            A basic responsibility message for any person (student or staff).
        """
        return "Follow university policies and contribute positively to the campus community."
