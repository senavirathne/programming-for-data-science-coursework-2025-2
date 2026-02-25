"""Staff class for the university management system."""

from __future__ import annotations

from person import Person


class Staff(Person):
    """Represent a staff member and their service role."""

    def __init__(
        self,
        name: str,
        person_id: str,
        email: str,
        phone: str,
        employee_id: str,
        role: str,
        department: str,
    ) -> None:
        """Initialize a staff member record.

        Args:
            name: Staff member full name.
            person_id: Unique person identifier.
            email: Staff email address.
            phone: Staff phone number.
            employee_id: Unique employee identifier.
            role: Job role for the staff member.
            department: Department name.

        Returns:
            None
        """
        super().__init__(name, person_id, email, phone)

        if not employee_id.strip():
            raise ValueError("Employee ID cannot be empty.")

        self._employee_id = employee_id
        self.role = role
        self.department = department

    @property
    def employee_id(self) -> str:
        """Get employee ID (read-only)."""
        return self._employee_id

    @property
    def role(self) -> str:
        """Get staff role."""
        return self._role

    @role.setter
    def role(self, value: str) -> None:
        """Set staff role."""
        if not value.strip():
            raise ValueError("Role cannot be empty.")
        self._role = value.strip()

    @property
    def department(self) -> str:
        """Get department name."""
        return self._department

    @department.setter
    def department(self, value: str) -> None:
        """Set department name."""
        if not value.strip():
            raise ValueError("Department cannot be empty.")
        self._department = value.strip()

    def get_info(self) -> dict[str, str]:
        """Return staff details as a dictionary.

        Returns:
            Staff profile data including base person fields.
        """
        info = super().get_info()
        info.update(
            {
                "employee_id": self.employee_id,
                "role": self.role,
                "department": self.department,
            }
        )
        return info

    def get_responsibilities(self) -> str:
        """Return staff responsibilities.

        Returns:
            A short description of staff responsibilities.
        """
        return (
            f"Perform {self.role.lower()} duties, support university operations, "
            "and provide administrative/service excellence."
        )
