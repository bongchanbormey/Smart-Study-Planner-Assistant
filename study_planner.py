import streamlit as st
from streamlit_calendar import calendar
from datetime import date
import pandas as pd

# Initialize task storage
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Time Format Helper Function
def format_estimated_time(total_hours):
    """
    Formats total estimated time (in hours) to 'xh ymin' format.
    """
    hours = int(total_hours)
    minutes = int((total_hours - hours) * 60)
    if hours > 0 and minutes > 0:
        return f"{hours}h {minutes}min"
    elif hours > 0:
        return f"{hours}h"
    elif minutes > 0:
        return f"{minutes}min"
    else:
        return "0min"

# Function to Display Tasks on Calendar
def show_calendar(tasks):
    """
    Displays tasks on a calendar using streamlit-calendar.
    """
    if not tasks:
        st.info("No tasks to display on the calendar.")
        return

    # Convert dates to string format for JSON serialization
    events = [
        {"date": task["Due Date"].strftime("%Y-%m-%d"), "title": task["Task Name"]}
        for task in tasks
    ]

    # Render the interactive calendar
    st.write("### Task Calendar")
    calendar(events)

# Study Planner UI
def study_planner_ui():
    # Form to add a new task
    with st.form("add_task_form"):
        st.subheader("➕ Add a New Task")
        task_name = st.text_input("Task Name", placeholder="Enter the task title")
        task_description = st.text_area(
            "Task Description",
            placeholder="Enter a brief description of the task (optional)",
            height=68,
        )
        category = st.selectbox("Category", ["Reading", "Coding", "Assignments", "Other"])
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        due_date = st.date_input("Due Date", min_value=date.today())
        
        # Separate hour and minute inputs for estimated time
        col1, col2 = st.columns(2)
        with col1:
            hours = st.number_input("Hours", min_value=0, max_value=23, step=1, key="hours_input")
        with col2:
            minutes = st.number_input("Minutes", min_value=0, max_value=59, step=1, key="minutes_input")
        
        submit_task = st.form_submit_button("Add Task")
        if submit_task:
            if task_name:
                # Calculate total estimated time in hours
                total_estimated_time = hours + (minutes / 60)
                
                # Add task to session state
                new_task = {
                    "Task Name": task_name,
                    "Description": task_description,
                    "Category": category,
                    "Priority": priority,
                    "Due Date": due_date,  # This will be converted to string in show_calendar
                    "Estimated Time (hours)": round(total_estimated_time, 2),
                    "Status": "Pending",
                }
                st.session_state.tasks.append(new_task)
                st.success("Task added successfully!")
            else:
                st.error("Task Name cannot be empty.")

    # Display tasks if available
    if st.session_state.tasks:
        # Convert task list to DataFrame for display
        tasks_df = pd.DataFrame(st.session_state.tasks)

        # Task filters
        filter_status = st.selectbox("Filter by Status", ["All", "Pending", "In Progress", "Completed"])
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
        
        filtered_df = tasks_df.copy()
        if filter_status != "All":
            filtered_df = filtered_df[filtered_df["Status"] == filter_status]
        if filter_priority != "All":
            filtered_df = filtered_df[filtered_df["Priority"] == filter_priority]

        st.dataframe(filtered_df, use_container_width=True)
        
        # Format the "Estimated Time (hours)" column
        tasks_df["Estimated Time"] = tasks_df["Estimated Time (hours)"].apply(format_estimated_time)
        
        # Drop the original unformatted column (optional)
        tasks_df = tasks_df.drop(columns=["Estimated Time (hours)"])
        
        # Highlight Priority levels with colors
        def highlight_priority(priority):
            colors = {"High": "background-color: #f28b82",  # Red
                      "Medium": "background-color: #fbbc04",  # Yellow
                      "Low": "background-color: #34a853"}  # Green
            return colors.get(priority, "")
        
        # Apply formatting to the Priority column
        styled_table = tasks_df.style.applymap(
            lambda x: highlight_priority(x) if x in ["High", "Medium", "Low"] else "", subset=["Priority"]
        )

        # Display all tasks
        st.write("### Task List")
        st.dataframe(tasks_df)

        # Calendar view
        show_calendar(st.session_state.tasks)

        # Progress Tracker
        st.write("### Progress Tracker")
        total_tasks = len(st.session_state.tasks)
        completed_tasks = sum(task["Status"] == "Completed" for task in st.session_state.tasks)
        progress_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        st.progress(progress_percentage / 100)
        st.write(f"Completed {completed_tasks} of {total_tasks} tasks ({round(progress_percentage, 2)}%).")

        # Mark tasks as completed
        st.write("### Update Task Status")
        task_to_update = st.selectbox("Select a task to update", [t["Task Name"] for t in st.session_state.tasks])
        new_status = st.selectbox("New Status", ["Pending", "In Progress", "Completed"])
        update_task = st.button("Update Status")
        if update_task:
            for task in st.session_state.tasks:
                if task["Task Name"] == task_to_update:
                    task["Status"] = new_status
                    st.success(f"Task '{task_to_update}' updated to '{new_status}'!")
                    break
                

        # Export tasks
        st.write("### Export Tasks")
        export_csv = st.button("Download Task List as CSV")
        if export_csv:
            tasks_csv = pd.DataFrame(st.session_state.tasks).to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=tasks_csv,
                file_name="study_tasks.csv",
                mime="text/csv"
            )
    else:
        st.info("No tasks added yet. Use the form above to add tasks.")
