import urllib.parse
import streamlit as st

st.set_page_config(page_title="Meeting Follow-up Tracker", page_icon="📌")

st.title("📌 Meeting & Manager Follow-up")
st.write("Log your meeting points and dispatch them instantly via WhatsApp.")

# Input fields
manager_phone = st.text_input("Manager WhatsApp Phone (e.g., +213555000000)")
meeting_title = st.text_input("Meeting Subject / Title", value="Q3 Performance Review")
schedule_date = st.date_input("Meeting Date")
schedule_time = st.time_input("Meeting Time")

st.markdown("### Discussion / Agenda Points")
if "points" not in st.session_state:
    st.session_state.points = [""]

for i, point in enumerate(st.session_state.points):
    st.session_state.points[i] = st.text_input(f"Point #{i+1}", value=point, key=f"point_{i}")

col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Add Point"):
        st.session_state.points.append("")
        st.rerun()
with col2:
    if len(st.session_state.points) > 1 and st.button("🗑️ Remove"):
        st.session_state.points.pop()
        st.rerun()

st.divider()

# Format message
formatted_points = "\n".join([f"{idx+1}. {p}" for idx, p in enumerate(st.session_state.points) if p.strip()])
message_body = f"""📌 *MEETING FOLLOW-UP REMINDER* 📌

*Topic:* {meeting_title}
*Scheduled For:* {schedule_date} at {schedule_time}

*Discussion Points:*
{formatted_points}"""

encoded_message = urllib.parse.quote(message_body)
whatsapp_url = f"https://wa.me/{manager_phone.strip('+')}?text={encoded_message}"

if manager_phone:
    st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color:#25D366; color:white; padding:12px 20px; border:none; border-radius:5px; font-size:16px; font-weight:bold; cursor:pointer; width:100%;">🚀 Open WhatsApp & Send Reminder</button></a>', unsafe_allow_html=True)
else:
    st.info("Enter your manager's WhatsApp phone number above to enable the send button.")
