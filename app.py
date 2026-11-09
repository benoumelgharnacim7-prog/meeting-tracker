import os
import urllib.parse
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Meeting Follow-up Tracker", page_icon="📌")

st.title("📌 Meeting & Manager Follow-up")
st.write("Log your meeting points, dispatch them via WhatsApp, and track them in Excel.")

# Input fields
manager_name = st.text_input("Manager Name", value="Abdellah")
manager_phone = st.text_input("Manager WhatsApp Phone (e.g., +213555000000)")
meeting_title = st.text_input("Meeting Subject / Title", value="Q3 Performance Review")
schedule_date = st.date_input("Meeting Date")
schedule_time = st.time_input("Meeting Time")

st.markdown("### Discussion / Agenda Points")
if "points" not in st.session_state:
    st.session_state.points = [""]

for i, point in enumerate(st.session_state.points):
    st.session_state.points[i] = st.text_input(
        f"Point #{i+1}", value=point, key=f"point_{i}"
    )

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
formatted_points = "\n".join([
    f"{idx+1}. {p}" for idx, p in enumerate(st.session_state.points) if p.strip()
])
message_body = f"""📌 *MEETING FOLLOW-UP REMINDER* 📌

*Topic:* {meeting_title}
*Scheduled For:* {schedule_date} at {schedule_time}

*Discussion Points:*
{formatted_points}"""

encoded_message = urllib.parse.quote(message_body)
whatsapp_url = (
    f"https://wa.me/{manager_phone.strip('+')}?text={encoded_message}"
)

excel_file = "meeting_history.xlsx"

if manager_phone:
  # Action button to log and open WhatsApp
  if st.markdown(
      f'<a href="{whatsapp_url}" target="_blank"><button'
      " style='background-color:#25D366; color:white; padding:12px 20px;"
      " border:none; border-radius:5px; font-size:16px; font-weight:bold;"
      " cursor:pointer; width:100%;'>🚀 Open WhatsApp & Log"
      " Meeting</button></a>",
      unsafe_allow_html=True,
  ):
    pass

  # Button to record the meeting data into Excel
  if st.button("💾 Save Meeting Record to Excel"):
    new_data = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Manager Name": manager_name,
        "Manager Phone": manager_phone,
        "Meeting Title": meeting_title,
        "Scheduled Date": str(schedule_date),
        "Scheduled Time": str(schedule_time),
        "Agenda Points": formatted_points,
    }])

    if os.path.exists(excel_file):
      df_existing = pd.read_excel(excel_file)
      df_combined = pd.concat([df_existing, new_data], ignore_index=True)
    else:
      df_combined = new_data

    df_combined.to_excel(excel_file, index=False)
    st.success(
        "Meeting successfully logged to `meeting_history.xlsx`!"
    )

    # Provide a download button for the updated Excel file
    with open(excel_file, "rb") as f:
      st.download_button(
          label="📥 Download Updated Excel Tracker",
          data=f,
          file_name="meeting_history.xlsx",
          mime=(
              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          ),
      )
else:
  st.info("Enter your manager's WhatsApp phone number above to enable actions.")
