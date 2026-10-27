# views/station_dashboard_view.py
import streamlit as st
from controllers.station_controller import StationController

def station_dashboard_view():
    st.set_page_config(page_title="Station Dashboard", page_icon="📊", layout="wide")

    # ---- Authentication Check ----
    if not st.session_state.get("logged_in"):
        st.error("Please login.")
        if st.button("Go to Login"):
            st.session_state["page"] = "login"
            st.rerun()
        return

    # ---- Load Dashboard Data ----
    data = StationController.get_dashboard_data()

    # ---- SIDEBAR ----
    
    st.sidebar.markdown(f"### 👤 {st.session_state.get('name')}")
    st.sidebar.markdown(f"**🏢 Station:** {data['station_name']}")
    st.sidebar.markdown("---")

    if st.sidebar.button("🏠 Dashboard"):
        st.session_state["page"] = "station_dashboard"
        st.rerun()

    if st.sidebar.button("📝 Request Funds"):
        st.session_state["page"] = "station_request_funds"
        st.rerun()

    if st.sidebar.button("💰 Update Usage"):
        st.session_state["page"] = "station_update_usage"
        st.rerun()

    if st.sidebar.button("📜 View History"):
        st.session_state["page"] = "station_history"
        st.rerun()

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        from utils.session_manager import end_session
        end_session()
        st.session_state["page"] = "login"
        st.rerun()

    # -------------------------------------------------------------------------
    #                               MAIN UI
    # -------------------------------------------------------------------------

    st.markdown(f"## 📊 Station Dashboard — {data['station_name']}")
    st.markdown("### Overview of Funds")

    # ===== METRIC CARDS =====
    card_style = """
        <style>
            .metric-card {
                background: #ffffff;
                border-radius: 14px;
                padding: 22px;
                box-shadow: 0 4px 18px rgba(0,0,0,0.08);
                text-align: center;
            }
            .metric-value {
                font-size: 26px;
                font-weight: bold;
                color: #0b3d91;
            }
            .metric-label {
                font-size: 16px;
                color: #666;
            }
        </style>
    """
    st.markdown(card_style, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"<div class='metric-card'><div class='metric-label'>Total Assigned</div>"
            f"<div class='metric-value'>₹ {data['assigned']:.2f}</div></div>",
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"<div class='metric-card'><div class='metric-label'>Total Used</div>"
            f"<div class='metric-value'>₹ {data['used']:.2f}</div></div>",
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"<div class='metric-card'><div class='metric-label'>Remaining</div>"
            f"<div class='metric-value'>₹ {data['residual']:.2f}</div></div>",
            unsafe_allow_html=True
        )

    st.markdown("")

    # ===== BODY SECTIONS =====
    col_left, col_right = st.columns([1.7, 1.3])

    # =====================================================================
    #                     UPDATED: REQUEST TABLE (WITH RHQ COMMENT)
    # =====================================================================
    with col_left:
        st.markdown("### 📝 Fund Requests (Recent)")

        pending = data["pending_requests"] or []
        if not pending:
            st.info("No requests found.")
        else:
            table = []
            for r in pending:

                # prettier status
                status = r["status"]
                if status == "Approved":
                    status_html = f"🟢 <b>{status}</b>"
                elif status == "Rejected":
                    status_html = f"🔴 <b>{status}</b>"
                else:
                    status_html = f"🟡 <b>{status}</b>"

                table.append({
                    "Request ID": r["request_id"],
                    "Amount": f"₹ {float(r['amount']):.2f}",
                    "Priority": r["priority"],
                    "Status": status_html,
                    "RHQ Comment": r.get("rhq_comment") or "-",
                    "Approved By": r.get("approved_by_name") or "-",
                    "Created At": r["created_at"]
                })

            st.write(
                "<style>td, th {padding: 6px;} .stDataFrame {font-size: 15px;}</style>",
                unsafe_allow_html=True
            )

            st.dataframe(table, use_container_width=True)

    # ---- Recent Activity ----
    with col_right:
        st.markdown("### 🕒 Recent Activity")

        acts = data["recent_activities"] or []
        if not acts:
            st.info("No recent activity.")
        else:
            for a in acts[:8]:
                who = a.get("user_name") or "System"
                station = a.get("station_name") or ""
                st.markdown(
                    f"""
                    <div style='margin-bottom:10px;
                                padding:10px;
                                background:#f7f9fc;
                                border-radius:10px;
                                border-left: 4px solid #0b3d91;'>
                        <b>{a['created_at']}</b><br>
                        {who} • {station}<br>
                        <span style='color:#444;'>{a['action_text']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

