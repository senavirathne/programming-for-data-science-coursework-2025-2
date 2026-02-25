import json

with open('university_system_interactive.ipynb', 'r') as f:
    nb = json.load(f)

# Cell 3: UniversityApp with ALL backend methods
app_code = """class UniversityApp:
    def __init__(self, db):
        self.db = db
        self.out = widgets.Output()

        # UI Elements Storage -- Custom Log UI
        self.log_html = widgets.HTML(value="<i>System ready...</i>")
        self.log_container = widgets.VBox(
            [self.log_html],
            layout=widgets.Layout(height='200px', overflow_y='auto', border='1px solid #ccc', padding='8px')
        )

    def log(self, message, level='info'):
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        color = "black"
        icon = "ℹ️"
        bg_color = "white"
        if level == 'success':
            color = "green"
            icon = "✅"
        elif level == 'error':
            color = "red"
            icon = "⚠️"
        elif level == 'demo':
            color = "#003366"
            icon = "🖥️"
            bg_color = "#f0f8ff"

        formatted_msg = str(message).replace('\\n', '<br>')
        new_entry = f"<div style='color:{color}; background-color:{bg_color}; border-bottom: 1px solid #eee; padding: 2px;'>"\\
                    f"<span style='color:#777; font-size:0.8em;'>[{timestamp}]</span> "\\
                    f"{icon} {formatted_msg}</div>"
        
        self.log_html.value = new_entry + self.log_html.value

    def demo_printer(self, message):
        self.log(message, level='demo')

    # --- Student Backend ---
    def create_student(self, name, s_id, email, phone, major, date):
        from student import Student
        if any(s.student_id == f"S{s_id}" for s in self.db.students):
            self.log(f"Error: Student with ID S{s_id} already exists.", "error")
            return False
        try:
            new_student = Student(name, f"S{s_id}", email, phone, s_id, major, date)
            self.db.students.append(new_student)
            self.log(f"Created Student: {name} (S{s_id})", "success")
            return True
        except Exception as e:
            self.log(f"Error creating student: {e}", "error")
            return False

    def update_student(self, s_id, new_name, new_email, new_phone, new_major):
        student = next((s for s in self.db.students if s.student_id == s_id), None)
        if student:
            try:
                if new_name: student.name = new_name
                if new_major: student.major = new_major
                student.update_contact(email=new_email if new_email else None, phone=new_phone if new_phone else None)
                self.log(f"Updated Student: {student.name} ({s_id})", "success")
                return True
            except Exception as e:
                self.log(f"Error updating student: {e}", "error")
        return False

    def delete_student(self, s_id):
        student = next((s for s in self.db.students if s.student_id == s_id), None)
        if student:
            for course_code in list(student.enrolled_courses):
                course = self.db.courses.get(course_code)
                if course:
                    try: course.remove_student(student)
                    except: pass
            self.db.students.remove(student)
            self.log(f"Deleted Student: {student.name} ({s_id})", "success")
            return True
        return False

    # --- Faculty Backend ---
    def create_faculty(self, name, id_val, email, phone, emp_id, dept, date):
        from faculty import Faculty
        if any(getattr(f, 'employee_id', '') == emp_id for f in getattr(self.db, 'faculty_members', [])):
            self.log(f"Error: Faculty with Emp ID {emp_id} already exists.", "error")
            return False
        try:
            new_f = Faculty(name, f"P{id_val}", email, phone, emp_id, dept, date)
            self.db.faculty_members.append(new_f)
            if dept in self.db.departments:
                 self.db.departments[dept].add_faculty(new_f)
            self.log(f"Created Faculty: {name} ({emp_id})", "success")
            return True
        except Exception as e:
            self.log(f"Error creating faculty: {e}", "error")
            return False

    def update_faculty(self, emp_id, new_name, new_email, new_phone, new_dept):
        f = next((x for x in getattr(self.db, 'faculty_members', []) if getattr(x, 'employee_id', '') == emp_id), None)
        if f:
            try:
                if new_name: f.name = new_name
                if new_dept: f.department = new_dept
                f.update_contact(email=new_email if new_email else None, phone=new_phone if new_phone else None)
                self.log(f"Updated Faculty: {f.name} ({emp_id})", "success")
                return True
            except Exception as e:
                self.log(f"Error updating faculty: {e}", "error")
        return False

    def delete_faculty(self, emp_id):
        f = next((x for x in getattr(self.db, 'faculty_members', []) if getattr(x, 'employee_id', '') == emp_id), None)
        if f:
            self.db.faculty_members.remove(f)
            self.log(f"Deleted Faculty: {f.name} ({emp_id})", "success")
            return True
        return False

    # --- Staff Backend ---
    def create_staff(self, name, id_val, email, phone, emp_id, role, dept):
        from staff import Staff
        if any(getattr(s, 'employee_id', '') == emp_id for s in getattr(self.db, 'staff_members', [])):
            self.log(f"Error: Staff with Emp ID {emp_id} already exists.", "error")
            return False
        try:
            new_s = Staff(name, f"P{id_val}", email, phone, emp_id, role, dept)
            self.db.staff_members.append(new_s)
            self.log(f"Created Staff: {name} ({emp_id})", "success")
            return True
        except Exception as e:
            self.log(f"Error creating staff: {e}", "error")
            return False

    def update_staff(self, emp_id, new_name, new_email, new_phone, new_role, new_dept):
        s = next((x for x in getattr(self.db, 'staff_members', []) if getattr(x, 'employee_id', '') == emp_id), None)
        if s:
            try:
                if new_name: s.name = new_name
                if new_role: s.role = new_role
                if new_dept: s.department = new_dept
                s.update_contact(email=new_email if new_email else None, phone=new_phone if new_phone else None)
                self.log(f"Updated Staff: {s.name} ({emp_id})", "success")
                return True
            except Exception as e:
                self.log(f"Error updating staff: {e}", "error")
        return False

    def delete_staff(self, emp_id):
        s = next((x for x in getattr(self.db, 'staff_members', []) if getattr(x, 'employee_id', '') == emp_id), None)
        if s:
            self.db.staff_members.remove(s)
            self.log(f"Deleted Staff: {s.name} ({emp_id})", "success")
            return True
        return False

    # --- Enrollment Backend ---
    def enroll_student(self, student, course_code):
        try:
            course = self.db.courses.get(course_code)
            if not course:
                self.log(f"Error: Course {course_code} not found.", "error")
                return
            
            # course.add_student handles capacity checks and calls student.enroll_course
            course.add_student(student)
            self.log(f"Enrolled {student.name} in {course_code}.", "success")
        except Exception as e:
            msg = str(e)
            self.log(f"Enroll Note: {msg}", "info" if "already" in msg.lower() else "error")

    def assign_grade(self, student, course_code, grade):
        try:
            student.add_grade(course_code, float(grade))
            self.log(f"Assigned Grade {grade} to {student.name} for {course_code}.", "success")
        except Exception as e:
            self.log(f"Error: {e}", "error")

    # --- Refreshers ---
    def refresh_student_dropdown(self, dropdown):
        if dropdown: dropdown.options = [(f"{s.name} ({s.student_id})", s) for s in self.db.students]

    def refresh_faculty_dropdown(self, dropdown):
        if dropdown: dropdown.options = [(f"{getattr(f, 'name', 'Unknown')} ({getattr(f, 'employee_id', '')})", f) for f in getattr(self.db, 'faculty_members', [])]

    def refresh_staff_dropdown(self, dropdown):
        if dropdown: dropdown.options = [(f"{getattr(s, 'name', 'Unknown')} ({getattr(s, 'employee_id', '')})", s) for s in getattr(self.db, 'staff_members', [])]

    def refresh_course_dropdown(self, dropdown):
        if dropdown: dropdown.options = [(f"{c.course_code} - {c.course_name}", c) for c in self.db.courses.values()]

app = UniversityApp(db)
"""

# Cell 4: UI Component Factories and Assembly
ui_code = """# --- UI Components Factories ---
import ipywidgets as widgets
from IPython.display import display, clear_output

# Global dropdowns so we can refresh them from anywhere
shared_dropdowns = {
    'student_manage': widgets.Dropdown(description="Select:"),
    'faculty_manage': widgets.Dropdown(description="Select:"),
    'staff_manage': widgets.Dropdown(description="Select:"),
    'student_enroll': widgets.Dropdown(description="Student:"),
    'course_enroll': widgets.Dropdown(description="Course:"),
    'student_view': widgets.Dropdown(description="Student:"),
    'course_view': widgets.Dropdown(description="Course:")
}

def global_refresh():
    app.refresh_student_dropdown(shared_dropdowns['student_manage'])
    app.refresh_student_dropdown(shared_dropdowns['student_enroll'])
    app.refresh_student_dropdown(shared_dropdowns['student_view'])
    app.refresh_faculty_dropdown(shared_dropdowns['faculty_manage'])
    app.refresh_staff_dropdown(shared_dropdowns['staff_manage'])
    app.refresh_course_dropdown(shared_dropdowns['course_enroll'])
    app.refresh_course_dropdown(shared_dropdowns['course_view'])

def create_dashboard_ui():
    out = widgets.HTML()
    btn = widgets.Button(description="Refresh Stats", icon='refresh', button_style='info')
    
    def render(b=None):
        total_s = len(db.students)
        total_f = len(getattr(db, 'faculty_members', []))
        total_st = len(getattr(db, 'staff_members', []))
        avg_gpa = sum(s.gpa for s in db.students) / total_s if total_s > 0 else 0.0
        
        highest = max(db.courses.values(), key=lambda c: len(getattr(c, '_enrolled_students', [])), default=None)
        pop_str = f"{highest.course_code} ({len(getattr(highest, '_enrolled_students', []))} stds)" if highest else "N/A"

        out.value = f'''
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; 
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 15px; 
                    box-shadow: 0 10px 20px rgba(0,0,0,0.1); display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;">
            <div style="background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); flex: 1; min-width: 200px; text-align: center; border-bottom: 4px solid #3498db;">
                <h3 style="margin: 0; color: #7f8c8d; font-size: 1.1em; text-transform: uppercase; letter-spacing: 1px;">👨‍🎓 Total Students</h3>
                <p style="font-size: 2.5em; font-weight: bold; color: #2c3e50; margin: 10px 0 0 0;">{total_s}</p>
            </div>
            <div style="background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); flex: 1; min-width: 200px; text-align: center; border-bottom: 4px solid #9b59b6;">
                <h3 style="margin: 0; color: #7f8c8d; font-size: 1.1em; text-transform: uppercase; letter-spacing: 1px;">👨‍🏫 Faculty / Staff</h3>
                <p style="font-size: 2.5em; font-weight: bold; color: #2c3e50; margin: 10px 0 0 0;">{total_f} / {total_st}</p>
            </div>
            <div style="background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); flex: 1; min-width: 200px; text-align: center; border-bottom: 4px solid #f1c40f;">
                <h3 style="margin: 0; color: #7f8c8d; font-size: 1.1em; text-transform: uppercase; letter-spacing: 1px;">🏆 Average GPA</h3>
                <p style="font-size: 2.5em; font-weight: bold; color: #2c3e50; margin: 10px 0 0 0;">{avg_gpa:.2f}</p>
            </div>
            <div style="background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); flex: 1; min-width: 200px; text-align: center; border-bottom: 4px solid #e74c3c;">
                <h3 style="margin: 0; color: #7f8c8d; font-size: 1.1em; text-transform: uppercase; letter-spacing: 1px;">🔥 Popular Course</h3>
                <p style="font-size: 1.5em; font-weight: bold; color: #2c3e50; margin: 15px 0 0 0;">{pop_str}</p>
            </div>
        </div>
        '''
    
    btn.on_click(render)
    render()
    return widgets.VBox([btn, out]), render

def create_student_management_ui(refresh_cb):
    drop = shared_dropdowns['student_manage']
    name = widgets.Text(description="Name:")
    pid = widgets.Text(description="Person ID:")
    sid = widgets.Text(description="Student ID:")
    email = widgets.Text(description="Email:")
    phone = widgets.Text(description="Phone:")
    major = widgets.Text(description="Major:")
    date = widgets.Text(description="Date:", value="2024-01-01")
    
    btn_add = widgets.Button(description="Add New", button_style='success', icon='plus')
    btn_upd = widgets.Button(description="Update", button_style='warning', icon='edit')
    btn_del = widgets.Button(description="Delete", button_style='danger', icon='trash')
    
    def on_drop(change):
        s = drop.value
        btn_del.description = "Delete"
        btn_del.button_style = "danger"
        if s:
            name.value = s.name
            pid.value = getattr(s, '_person_id', '')
            sid.value = s.student_id
            email.value = s.email
            phone.value = s.phone
            major.value = getattr(s, 'major', '')
            date.value = getattr(s, 'enrollment_date', '')
    drop.observe(on_drop, names='value')
    
    def on_add(b): 
        if app.create_student(name.value, pid.value, email.value, phone.value, major.value, date.value):
            global_refresh()
            refresh_cb()
    def on_upd(b): 
        if drop.value and app.update_student(drop.value.student_id, name.value, email.value, phone.value, major.value):
            global_refresh()
            refresh_cb()
    def on_del(b): 
        if btn_del.description == "Delete":
            btn_del.description = "Confirm Delete?"
            btn_del.button_style = "warning"
        else:
            if drop.value and app.delete_student(drop.value.student_id):
                global_refresh()
                refresh_cb()
            btn_del.description = "Delete"
            btn_del.button_style = "danger"
            
    btn_add.on_click(on_add)
    btn_upd.on_click(on_upd)
    btn_del.on_click(on_del)
    
    return widgets.VBox([
        widgets.HTML("<h4>Manage Students</h4>"), drop, widgets.HTML("<hr>"),
        name, pid, sid, email, phone, major, date,
        widgets.HBox([btn_add, btn_upd, btn_del])
    ])

def create_faculty_management_ui(refresh_cb):
    drop = shared_dropdowns['faculty_manage']
    name = widgets.Text(description="Name:")
    pid = widgets.Text(description="Person ID:")
    eid = widgets.Text(description="Emp ID:")
    email = widgets.Text(description="Email:")
    phone = widgets.Text(description="Phone:")
    dept = widgets.Text(description="Dept:")
    date = widgets.Text(description="Date:", value="2020-01-01")
    
    btn_add = widgets.Button(description="Add New", button_style='success', icon='plus')
    btn_upd = widgets.Button(description="Update", button_style='warning', icon='edit')
    btn_del = widgets.Button(description="Delete", button_style='danger', icon='trash')
    
    def on_drop(change):
        f = drop.value
        btn_del.description = "Delete"
        btn_del.button_style = "danger"
        if f:
            name.value = f.name
            pid.value = getattr(f, '_person_id', '')
            eid.value = getattr(f, 'employee_id', '')
            email.value = f.email
            phone.value = f.phone
            dept.value = getattr(f, 'department', '')
            date.value = getattr(f, 'hire_date', '')
    drop.observe(on_drop, names='value')
    
    def on_add(b):
        if app.create_faculty(name.value, pid.value, email.value, phone.value, eid.value, dept.value, date.value):
            global_refresh()
            refresh_cb()
    def on_upd(b):
        if drop.value and app.update_faculty(getattr(drop.value, 'employee_id', ''), name.value, email.value, phone.value, dept.value):
            global_refresh()
            refresh_cb()
    def on_del(b):
        if btn_del.description == "Delete":
            btn_del.description = "Confirm Delete?"
            btn_del.button_style = "warning"
        else:
            if drop.value and app.delete_faculty(getattr(drop.value, 'employee_id', '')):
                global_refresh()
                refresh_cb()
            btn_del.description = "Delete"
            btn_del.button_style = "danger"
            
    btn_add.on_click(on_add)
    btn_upd.on_click(on_upd)
    btn_del.on_click(on_del)
    
    return widgets.VBox([
        widgets.HTML("<h4>Manage Faculty</h4>"), drop, widgets.HTML("<hr>"),
        name, pid, eid, email, phone, dept, date,
        widgets.HBox([btn_add, btn_upd, btn_del])
    ])

def create_staff_management_ui(refresh_cb):
    drop = shared_dropdowns['staff_manage']
    name = widgets.Text(description="Name:")
    pid = widgets.Text(description="Person ID:")
    eid = widgets.Text(description="Emp ID:")
    email = widgets.Text(description="Email:")
    phone = widgets.Text(description="Phone:")
    role = widgets.Text(description="Role:")
    dept = widgets.Text(description="Dept:")
    
    btn_add = widgets.Button(description="Add New", button_style='success', icon='plus')
    btn_upd = widgets.Button(description="Update", button_style='warning', icon='edit')
    btn_del = widgets.Button(description="Delete", button_style='danger', icon='trash')
    
    def on_drop(change):
        s = drop.value
        btn_del.description = "Delete"
        btn_del.button_style = "danger"
        if s:
            name.value = s.name
            pid.value = getattr(s, '_person_id', '')
            eid.value = getattr(s, 'employee_id', '')
            email.value = s.email
            phone.value = s.phone
            role.value = getattr(s, 'role', '')
            dept.value = getattr(s, 'department', '')
    drop.observe(on_drop, names='value')
    
    def on_add(b):
        if app.create_staff(name.value, pid.value, email.value, phone.value, eid.value, role.value, dept.value):
            global_refresh()
            refresh_cb()
    def on_upd(b):
        if drop.value and app.update_staff(getattr(drop.value, 'employee_id', ''), name.value, email.value, phone.value, role.value, dept.value):
            global_refresh()
            refresh_cb()
    def on_del(b):
        if btn_del.description == "Delete":
            btn_del.description = "Confirm Delete?"
            btn_del.button_style = "warning"
        else:
            if drop.value and app.delete_staff(getattr(drop.value, 'employee_id', '')):
                global_refresh()
                refresh_cb()
            btn_del.description = "Delete"
            btn_del.button_style = "danger"
            
    btn_add.on_click(on_add)
    btn_upd.on_click(on_upd)
    btn_del.on_click(on_del)
    
    return widgets.VBox([
        widgets.HTML("<h4>Manage Staff</h4>"), drop, widgets.HTML("<hr>"),
        name, pid, eid, email, phone, role, dept,
        widgets.HBox([btn_add, btn_upd, btn_del])
    ])

def create_enrollment_ui(refresh_cb):
    drop_s, drop_c = shared_dropdowns['student_enroll'], shared_dropdowns['course_enroll']
    btn_enr = widgets.Button(description="Enroll", button_style='success', icon='check')
    inp_grad = widgets.BoundedFloatText(value=0.0, min=0.0, max=4.0, step=0.1, description="Grade:")
    btn_grad = widgets.Button(description="Assign Grade", button_style='warning', icon='graduation-cap')
    
    def on_enr(b):
        if drop_s.value and drop_c.value:
            app.enroll_student(drop_s.value, drop_c.value.course_code)
            refresh_cb()
            if shared_dropdowns['student_view'].value == drop_s.value:
                # Retrigger observer hack
                shared_dropdowns['student_view'].value = drop_s.value
    btn_enr.on_click(on_enr)
    
    def on_grad(b):
        if drop_s.value and drop_c.value:
            app.assign_grade(drop_s.value, drop_c.value.course_code, inp_grad.value)
            refresh_cb() # Refresh dashboards
            if shared_dropdowns['student_view'].value == drop_s.value:
                shared_dropdowns['student_view'].value = drop_s.value # Retrigger profile recalculation
    btn_grad.on_click(on_grad)
    
    return widgets.VBox([
        widgets.HTML("<h3>Enrollment & Grades</h3>"), drop_s, drop_c, btn_enr,
        widgets.HTML("<hr>"), inp_grad, btn_grad
    ])

def create_views_ui():
    drop_s, drop_c = shared_dropdowns['student_view'], shared_dropdowns['course_view']
    out_s, out_c = widgets.HTML(), widgets.HTML()
    
    def on_s_view(change):
        s = drop_s.value
        if s:
            info = s.get_info()
            enrolled_str = ', '.join(s.enrolled_courses) if s.enrolled_courses else "None"
            grades_html = "".join([f"<li style='padding: 5px 0; border-bottom: 1px solid #eee;'><span style='font-weight: 500; color: #34495e;'>{c}</span><span style='float: right; color: #2c3e50; font-weight: 600;'>{g}</span></li>" for c, g in s.grades.items()])
            out_s.value = f'''
            <div style="font-family: 'Segoe UI', Tahoma, Verdana, sans-serif; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); border-left: 5px solid #3498db; max-width: 500px; margin-top: 15px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                    <h2 style="margin: 0; color: #2c3e50; font-size: 1.8em;">{info.get('name', 'N/A')}</h2>
                    <span style="background: #e8f4fd; color: #3498db; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9em;">🧑‍🎓 ID: {s.student_id}</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
                    <div><p style="margin:0; color:#7f8c8d; font-size:0.9em;">Email</p><p style="margin:0; font-weight:500;">{info.get('email', '-')}</p></div>
                    <div><p style="margin:0; color:#7f8c8d; font-size:0.9em;">Major</p><p style="margin:0; font-weight:500;">{info.get('major', '-')}</p></div>
                    <div><p style="margin:0; color:#7f8c8d; font-size:0.9em;">GPA</p><p style="margin:0; font-weight:bold; color: {'#27ae60' if s.gpa >= 3.0 else '#e67e22'}; font-size: 1.2em;">{s.gpa:.2f}</p></div>
                    <div><p style="margin:0; color:#7f8c8d; font-size:0.9em;">Status</p><p style="margin:0; font-weight:bold; color: #8e44ad;">{s.get_academic_status()}</p></div>
                </div>
                <div><p style="margin:0 0 5px 0; color:#7f8c8d; font-size:0.9em;">Enrolled Courses</p><p style="margin:0; background: #f8f9fa; padding: 10px; border-radius: 6px; font-family: monospace;">{enrolled_str}</p></div>
                <div style="margin-top: 15px;">
                    <p style="margin:0 0 10px 0; color:#7f8c8d; font-size:0.9em; border-bottom: 2px solid #eee; padding-bottom: 5px;">Grades</p>
                    <ul style="list-style-type: none; padding: 0; margin: 0;">{"<li style='padding: 5px 0; color: #95a5a6; font-style: italic;'>No grades yet</li>" if not grades_html else grades_html}</ul>
                </div>
            </div>
            '''
        else:
            out_s.value = ""
    drop_s.observe(on_s_view, names='value')
    
    def on_c_view(change):
        c = drop_c.value
        if c:
            inst = getattr(c, '_instructor', None)
            enrolled = getattr(c, '_enrolled_students', [])
            enrollment_perc = (len(enrolled) / c.max_capacity * 100) if c.max_capacity > 0 else 0
            student_list_html = "".join([f"<li style='padding: 4px 0; border-bottom: 1px dotted #e0e0e0;'><span style='color:#34495e; font-weight: 500;'>{st.name}</span> <span style='float:right; color:#7f8c8d; font-size: 0.9em;'>{st.student_id}</span></li>" for st in enrolled])
            
            out_c.value = f'''
            <div style="font-family: 'Segoe UI', Tahoma, Verdana, sans-serif; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); border-left: 5px solid #e67e22; max-width: 500px; margin-top: 15px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                    <h2 style="margin: 0; color: #2c3e50; font-size: 1.6em;">{c.course_name}</h2>
                    <span style="background: #fdf2e9; color: #e67e22; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9em;">📚 {c.course_code}</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
                    <div><p style="margin:0; color:#7f8c8d; font-size:0.9em;">Credits</p><p style="margin:0; font-weight:bold; font-size: 1.2em; color: #2980b9;">{getattr(c, '_credits', 'N/A')}</p></div>
                    <div><p style="margin:0; color:#7f8c8d; font-size:0.9em;">Instructor</p><p style="margin:0; font-weight:500;">{getattr(inst, 'name', 'None')}</p></div>
                </div>
                <div style="margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="color:#7f8c8d; font-size:0.9em;">Enrollment: {len(enrolled)} / {c.max_capacity}</span>
                        <span style="font-weight: 500; font-size: 0.9em; color:{'#e74c3c' if enrollment_perc >= 100 else '#2ecc71'}">{int(enrollment_perc)}% Filled</span>
                    </div>
                    <div style="background: #ecf0f1; border-radius: 10px; height: 10px; overflow: hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="background: {'#e74c3c' if enrollment_perc >= 100 else '#2ecc71'}; height: 100%; width: {min(100, enrollment_perc)}%; border-radius: 10px;"></div>
                    </div>
                </div>
                <div style="margin-top: 15px; max-height: 200px; overflow-y: auto;">
                    <p style="margin:0 0 10px 0; color:#7f8c8d; font-size:0.9em; border-bottom: 2px solid #eee; padding-bottom: 5px;">Enrolled Students</p>
                    <ul style="list-style-type: none; padding: 0; margin: 0;">{"<li style='padding: 5px 0; color: #bdc3c7; font-style: italic;'>No students enrolled</li>" if not student_list_html else student_list_html}</ul>
                </div>
            </div>
            '''
        else:
            out_c.value = ""
    drop_c.observe(on_c_view, names='value')
    
    acc = widgets.Accordion(children=[widgets.VBox([drop_s, out_s]), widgets.VBox([drop_c, out_c])])
    acc.set_title(0, 'Student Profiles')
    acc.set_title(1, 'Course Details')
    return acc

# --- Main Assembly ---
dash_ui, refresh_dash_cb = create_dashboard_ui()
global_refresh()

acc_manage = widgets.Accordion(children=[
    create_student_management_ui(refresh_dash_cb),
    create_faculty_management_ui(refresh_dash_cb),
    create_staff_management_ui(refresh_dash_cb)
])
acc_manage.set_title(0, 'Students')
acc_manage.set_title(1, 'Faculty')
acc_manage.set_title(2, 'Staff')

main_tabs = widgets.Tab([
    dash_ui, acc_manage, create_enrollment_ui(refresh_dash_cb), create_views_ui()
])
main_tabs.set_title(0, 'Dashboard')
main_tabs.set_title(1, 'Manage Data')
main_tabs.set_title(2, 'Enrollment')
main_tabs.set_title(3, 'Views')

# Trigger initial UI render
for drop in shared_dropdowns.values():
    if drop.value: drop.value = drop.value

main_ui = widgets.VBox([main_tabs, widgets.HTML("<hr><h3>Activity Log</h3>"), app.log_container])
display(main_ui)
"""

nb['cells'][3]['source'] = [line + '\\n' for line in app_code.split('\\n')][:-1] + [app_code.split('\\n')[-1]]
nb['cells'][4]['source'] = [line + '\\n' for line in ui_code.split('\\n')][:-1] + [ui_code.split('\\n')[-1]]

with open('university_system_interactive.ipynb', 'w') as f:
    json.dump(nb, f, indent=4)

print("Notebook successfully refactored and saved.")
