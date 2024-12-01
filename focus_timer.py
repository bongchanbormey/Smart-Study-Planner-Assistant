import streamlit as st
import time

# Function to handle the focus timer and progress logging
def focus_timer():
    st.title("⏳ Focus Timer")
    st.write("Boost your productivity with automated focus sessions and breaks!")

    # Timer Settings
    work_duration = st.number_input("Focus Duration (minutes):", min_value=1, max_value=120, value=25)
    short_break = st.number_input("Short Break (minutes):", min_value=1, max_value=30, value=5)
    long_break = st.number_input("Long Break (minutes):", min_value=1, max_value=60, value=15)
    total_sessions = st.number_input("Number of Sessions:", min_value=1, max_value=10, value=3)

    # Initialize session states
    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
    if "mode" not in st.session_state:
        st.session_state.mode = "Focus"
    if "remaining_time" not in st.session_state:
        st.session_state.remaining_time = work_duration * 60
    if "sessions_completed" not in st.session_state:
        st.session_state.sessions_completed = 0
    if "current_session" not in st.session_state:
        st.session_state.current_session = 1
    if "paused_time" not in st.session_state:
        st.session_state.paused_time = 0

    # Timer Controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if not st.session_state.timer_running and st.button("Start Timer"):
            st.session_state.timer_running = True
            st.session_state.remaining_time = (
                work_duration * 60 if st.session_state.mode == "Focus" else
                short_break * 60 if st.session_state.mode == "Short Break" else
                long_break * 60
            )
            st.session_state.paused_time = 0

    with col2:
        if st.session_state.timer_running and st.button("Stop Timer"):
            st.session_state.timer_running = False
            st.session_state.paused_time = st.session_state.remaining_time

        elif not st.session_state.timer_running and st.session_state.paused_time > 0 and st.button("Resume Timer"):
            st.session_state.timer_running = True

    with col3:
        if st.button("Reset Timer"):
            st.session_state.timer_running = False
            st.session_state.mode = "Focus"
            st.session_state.remaining_time = work_duration * 60
            st.session_state.sessions_completed = 0
            st.session_state.current_session = 1
            st.session_state.paused_time = 0

    # Timer Header
    header_placeholder = st.empty()
    timer_placeholder = st.empty()

    # Timer Logic
    if st.session_state.timer_running:
        while st.session_state.timer_running and st.session_state.remaining_time > 0:
            minutes, seconds = divmod(st.session_state.remaining_time, 60)
            header_placeholder.markdown(
                f"### {'Session ' + str(st.session_state.current_session) if st.session_state.mode == 'Focus' else st.session_state.mode}"
            )
            timer_placeholder.markdown(
                f"<h1 style='text-align: center; font-size: 80px;'>{int(minutes):02}:{int(seconds):02}</h1>",
                unsafe_allow_html=True,
            )
            time.sleep(1)
            st.session_state.remaining_time -= 1

        if st.session_state.remaining_time <= 0:
            # Transition logic
            if st.session_state.mode == "Focus":
                st.session_state.sessions_completed += 1
                if st.session_state.current_session < total_sessions:
                    st.session_state.mode = "Short Break"
                    st.session_state.remaining_time = short_break * 60
                else:
                    st.session_state.mode = "Long Break"
                    st.session_state.remaining_time = long_break * 60
            elif st.session_state.mode == "Short Break":
                st.session_state.mode = "Focus"
                st.session_state.current_session += 1
                st.session_state.remaining_time = work_duration * 60
            elif st.session_state.mode == "Long Break":
                st.session_state.timer_running = False
                st.success("🎉 All Sessions Completed!")
                st.balloons()

    # Display Timer in Paused State
    if not st.session_state.timer_running and st.session_state.paused_time > 0:
        minutes, seconds = divmod(st.session_state.paused_time, 60)
        timer_placeholder.markdown(
            f"<h1 style='text-align: center; font-size: 80px;'>{int(minutes):02}:{int(seconds):02}</h1>",
            unsafe_allow_html=True,
        )

    # Today's Progress Section
    st.markdown("### Today's Progress")
    completed_sessions = st.session_state.sessions_completed
    progress_icon = "🍅" * completed_sessions
    remaining_icon = "🍅" * (total_sessions - completed_sessions)
    st.write(f"{progress_icon}{remaining_icon} ({completed_sessions}/{total_sessions} sessions)")

