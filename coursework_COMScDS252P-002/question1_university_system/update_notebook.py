import json

with open("university_system_interactive.ipynb", "r") as f:
    nb = json.load(f)

# The cell we want to modify is at index 2 (UI Components)
# Let's find the cell with "# --- UI Components ---"
ui_cell_idx = -1
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code" and len(cell["source"]) > 0 and "# --- UI Components ---" in cell["source"][0]:
        ui_cell_idx = i
        break

if ui_cell_idx != -1:
    source = nb["cells"][ui_cell_idx]["source"]
    
    # We will inject our new tabs right before the "# Main Layout\n" line
    insert_idx = -1
    for i, line in enumerate(source):
        if "# Main Layout" in line:
            insert_idx = i
            break
            
    if insert_idx != -1:
        new_ui_lines = [
            "# 5. Student Profile Tab\n",
            "profile_student_dropdown = widgets.Dropdown(description=\"Student:\")\n",
            "app.refresh_student_dropdown(profile_student_dropdown)\n",
            "profile_out = widgets.Output()\n",
            "def show_student_profile(change):\n",
            "    profile_out.clear_output()\n",
            "    student = profile_student_dropdown.value\n",
            "    if student:\n",
            "        with profile_out:\n",
            "            info = student.get_info()\n",
            "            print(f\"Name: {info['name']}\")\n",
            "            print(f\"ID: {info.get('student_id', 'N/A')}\")\n",
            "            print(f\"Email: {info['email']}\")\n",
            "            print(f\"Major: {info.get('major', 'N/A')}\")\n",
            "            print(f\"GPA: {student.gpa:.2f} ({student.get_academic_status()})\")\n",
            "            print(\"Enrolled Courses:\")\n",
            "            for c in student.enrolled_courses:\n",
            "                print(f\"  - {c}\")\n",
            "            print(\"Grades:\")\n",
            "            for c, g in student.grades.items():\n",
            "                print(f\"  - {c}: {g}\")\n",
            "profile_student_dropdown.observe(show_student_profile, names='value')\n",
            "show_student_profile(None)\n",
            "profile_box = widgets.VBox([widgets.HTML(\"<h3>Student Profile</h3>\"), profile_student_dropdown, profile_out])\n",
            "\n",
            "# 6. Course Details Tab\n",
            "details_course_dropdown = widgets.Dropdown(description=\"Course:\")\n",
            "app.refresh_course_dropdown(details_course_dropdown)\n",
            "course_out = widgets.Output()\n",
            "def show_course_details(change):\n",
            "    course_out.clear_output()\n",
            "    course = details_course_dropdown.value\n",
            "    if course:\n",
            "        with course_out:\n",
            "            print(f\"Course: {course.course_code} - {course.course_name}\")\n",
            "            print(f\"Credits: {course._credits if hasattr(course, '_credits') else 'N/A'}\")\n",
            "            instructor_name = getattr(course, '_instructor').name if getattr(course, '_instructor', None) else 'None'\n",
            "            print(f\"Instructor: {instructor_name}\")\n",
            "            enrolled = getattr(course, '_enrolled_students', [])\n",
            "            print(f\"Capacity: {len(enrolled)} / {course.max_capacity}\")\n",
            "            print(\"Enrolled Students:\")\n",
            "            for s in enrolled:\n",
            "                print(f\"  - {s.name} ({s.student_id})\")\n",
            "details_course_dropdown.observe(show_course_details, names='value')\n",
            "show_course_details(None)\n",
            "course_box = widgets.VBox([widgets.HTML(\"<h3>Course Details</h3>\"), details_course_dropdown, course_out])\n",
            "\n",
            "# 7. Dashboard Tab\n",
            "dash_out = widgets.Output()\n",
            "dash_refresh_btn = widgets.Button(description=\"Refresh Stats\", icon='refresh')\n",
            "def refresh_dashboard(b=None):\n",
            "    dash_out.clear_output()\n",
            "    with dash_out:\n",
            "        total_students = len(db.students)\n",
            "        total_faculty = len(getattr(db, 'faculty_members', getattr(db, 'academic_staff_members', [])))\n",
            "        total_staff = len(getattr(db, 'staff_members', getattr(db, 'non_academic_staff_members', [])))\n",
            "        avg_gpa = sum(s.gpa for s in db.students) / total_students if total_students > 0 else 0.0\n",
            "        print(f\"Total Students: {total_students}\")\n",
            "        print(f\"Total Faculty/Academic Staff: {total_faculty}\")\n",
            "        print(f\"Total Staff: {total_staff}\")\n",
            "        print(f\"Average Student GPA: {avg_gpa:.2f}\")\n",
            "        \n",
            "        highest_enrollment = max(db.courses.values(), key=lambda c: len(getattr(c, '_enrolled_students', [])), default=None)\n",
            "        if highest_enrollment:\n",
            "            print(f\"Most Popular Course: {highest_enrollment.course_code} ({len(getattr(highest_enrollment, '_enrolled_students', []))} students)\")\n",
            "dash_refresh_btn.on_click(refresh_dashboard)\n",
            "refresh_dashboard()\n",
            "dash_box = widgets.VBox([widgets.HTML(\"<h3>System Statistics</h3>\"), dash_refresh_btn, dash_out])\n",
            "\n"
        ]
        
        # Replace the Main Layout section to include new tabs
        for i in range(len(source)):
            if "tabs = widgets.Tab(" in source[i]:
                source[i] = "tabs = widgets.Tab([dash_box, enroll_box, profile_box, course_box, dept_box, add_student_box, demo_box])\n"
            elif "tabs.set_title(" in source[i]:
                pass # We will replace all titles
        
        # Remove old set_title lines
        source = [line for line in source if "tabs.set_title(" not in line]
        
        # Insert set_title lines
        new_titles = [
            "tabs.set_title(0, 'Dashboard')\n",
            "tabs.set_title(1, 'Enrollment')\n",
            "tabs.set_title(2, 'Student Profile')\n",
            "tabs.set_title(3, 'Course Details')\n",
            "tabs.set_title(4, 'Departments')\n",
            "tabs.set_title(5, 'Add Student')\n",
            "tabs.set_title(6, 'Console Demos')\n"
        ]
        
        # re-find Main layout position after removals
        insert_idx2 = -1
        for i, line in enumerate(source):
            if "tabs = widgets.Tab(" in line:
                insert_idx2 = i
                break
        
        if insert_idx2 != -1:
            source = source[:insert_idx2+1] + new_titles + source[insert_idx2+1:]
        
        # Re-find new tabs insert point
        insert_idx3 = -1
        for i, line in enumerate(source):
            if "# Main Layout" in line:
                insert_idx3 = i
                break
        
        source = source[:insert_idx3] + new_ui_lines + source[insert_idx3:]
        
        
        # We should also update on_add_student to refresh the profile dropdown
        for i, line in enumerate(source):
            if "app.refresh_student_dropdown(student_dropdown)" in line:
                source.insert(i+1, "        app.refresh_student_dropdown(profile_student_dropdown)\n")
                break
                
        # Update on_enroll_click to refresh profile & course
        for i, line in enumerate(source):
            if "app.log(f\"Enrolled {student.name} in {course.course_code}\", \"success\")" in line:
                source.insert(i+1, "            show_student_profile(None)\n            show_course_details(None)\n            refresh_dashboard()\n")
                break
                
        # Update on_grade_click to refresh profile
        for i, line in enumerate(source):
            if "app.assign_grade(student, course.course_code, grade_input.value)" in line:
                source.insert(i+1, "        show_student_profile(None)\n        refresh_dashboard()\n")
                break

        nb["cells"][ui_cell_idx]["source"] = source

with open("university_system_interactive.ipynb", "w") as f:
    json.dump(nb, f, indent=4)

print("Notebook modified successfully.")
