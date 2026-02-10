# University Management System (OOP)

## Overview

This project implements a robust **University Management System** using Python. It adheres to **Object-Oriented Programming (OOP)** principles, The system models core university entities such as Students, Faculty, Staff, Courses, and Departments, handling relationships, academic tracking, and role-specific responsibilities.

Key features include class hierarchy with inheritance, polymorphic behavior, strict encapsulation with validation logic, and a comprehensive test suite.

## 📂 Project Structure

```text
coursework_COMScDS252P-002/
└── question1_university_system/
    ├── main.py                  # Entry point demonstrating system functionality
    ├── person.py                # Base class for all individuals
    ├── student.py               # Student entity with academic logic
    ├── faculty.py               # Faculty entity with teaching logic
    ├── staff.py                 # Staff entity for administrative roles
    ├── course.py                # Course management logic
    ├── department.py            # Departmental organization logic
    ├── README.md                # Project documentation
    └── tests/                   # Unit test suite
        └── test_university_system.py

```

## 🚀 Features Implemented

### 1. Class Hierarchy & Inheritance

The system is built on a solid foundation of inheritance to promote code reuse and logical grouping:

* **`Person` (Base Class):** Manages shared attributes like `name`, `person_id`, `email`, and `phone`. Includes utility methods `get_info()` and `update_contact()`.
* **`Student`:** Extends `Person` with `student_id`, `major`, and `enrollment_date`.
* **`Faculty`:** Extends `Person` with `employee_id`, `department`, and `hire_date`.
* **`Staff`:** Extends `Person` with `employee_id`, `role`, and `department`.
* **Constructor Chaining:** All derived classes utilize `super().__init__()` for proper initialization.

### 2. Student Course Management

Robust academic tracking features for `Student` objects:

* **Enrollment:** `enroll_course(course_code)` allows students to register for classes.
* **Grading:** `add_grade(course_code, grade)` stores academic performance in a dictionary.
* **GPA Calculation:** `calculate_gpa()` dynamically computes the Grade Point Average based on credit hours.
* **Status Tracking:** `get_academic_status()` determines standing (e.g., "Good Standing", "Probation").

### 3. Encapsulation & Validation

Data integrity is enforced through strict encapsulation rules:

* **Read-Only Properties:** The `gpa` attribute is exposed via `@property` without a setter to prevent manual manipulation.
* **Grade Validation:** Grades must be within the `0.0` to `4.0` range; otherwise, a `ValueError` is raised.
* **Enrollment Limits:** Students are restricted to a maximum of **6 courses** per semester.
* **Error Handling:** Invalid operations (like over-enrollment) raise exceptions, which are gracefully handled in `main.py`.

### 4. Polymorphism

The system leverages polymorphism to handle different roles uniformly:

* The `get_responsibilities()` method is abstract in concept and overridden in `Student`, `Faculty`, and `Staff`.
* `main.py` demonstrates iterating through a mixed list of people, invoking the correct version of `get_responsibilities()` for each object type at runtime.

### 5. Course & Department Management

* **`Course`:** Manages metadata (`course_code`, `credits`, `instructor`) and logistics (`enrolled_students`, `max_capacity`). Includes logic to prevent over-enrollment (`is_full()`).
* **`Department`:** Organizes the university structure, holding lists of faculty and courses. Methods include `add_faculty()` and `add_course()` to build the organizational tree.

## 🛠️ Usage

### Prerequisites

* Python 3.8 or higher

### Running the Demonstration

Execute the main script to see a simulation of the system in action, including object creation, enrollment, grading, and polymorphic behavior.

```bash
cd coursework_COMScDS252P-002/question1_university_system
python main.py

```

### Running Tests

The project includes a `unittest` suite to verify logic, validation, and edge cases.

```bash
cd coursework_COMScDS252P-002/question1_university_system
python -m unittest discover -s tests -p "test_*.py"

```

## 📝 Code Quality

* **PEP 8 Compliance:** The codebase follows standard Python style guidelines.
* **Documentation:** All classes and significant methods include docstrings that clearly describe purpose, inputs, and outputs in plain language.

---

*Created for Object-Oriented Programming Coursework.*

---
