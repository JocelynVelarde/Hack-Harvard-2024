import streamlit as st

st.set_page_config(
        page_title="theft-alert",
        page_icon="🚨",
)

st.title('📷 Welcome to Theft Alert!')

st.divider()

st.subheader("TheftWatch: Enhancing Retail Security")
st.write("**TheftWatch** uses computer vision and machine learning to monitor in-store activity, helping small business owners feel secure and in control of their shops.")

st.write("Here are some of the features we offer:")
st.write("✨ Real-time **customer monitoring** using computer vision to classify behavior.")
st.write("✨ **WhatsApp notifications** for suspicious activities detected in-store.")
st.write("✨ **Heatmap visualizations** to identify hotspots for theft.")
st.write("✨ Detailed **incident reports** generated for each alert.")
st.write("✨ Insights into **customer behavior** to help reduce shoplifting.")

st.divider()

# Create a grid of 4 rows and 2 columns
rows = 4
columns = 2

for row in range(rows):
    cols = st.columns(columns)
    for col_index, col in enumerate(cols):
        with col:
            container = st.container(border=True)
            with container:
                if row == 0 and col_index == 0:
                    st.write("🛒 **Real-time Monitoring**")
                    st.write("1. Uses computer vision to classify customers as safe, suspicious, or dangerous.")
                    st.write("2. Sends alerts when suspicious behavior is detected.")
                    st.write("3. Provides immediate insights into in-store activities.")
                    st.write("4. Helps store owners take proactive measures against theft.")
                    
                elif row == 0 and col_index == 1:
                    st.write("📱 **WhatsApp Notifications**")
                    st.write("1. Receive real-time alerts for detected suspicious activities.")
                    st.write("2. Notifications include details about the incident and identified individuals.")
                    st.write("3. Easy setup with Twilio API for seamless communication.")
                   
                elif row == 1 and col_index == 0:
                    st.write("🗺️ **Heatmap Visualizations**")
                    st.write("1. View hotspots for theft to identify areas of concern.")
                    st.write("2. Historical data analysis to spot trends in shoplifting.")
                    st.write("3. Visualize the performance of theft prevention measures.")
                    
                elif row == 1 and col_index == 1:
                    st.write("📊 **Detailed Reports**")
                    st.write("1. Generate reports detailing incidents of theft and suspicious activities.")
                    st.write("2. Gain insights into customer behavior patterns over time.")
                    st.write("3. Help in developing strategies for reducing theft.")
                    
                elif row == 2 and col_index == 0:
                    st.write("🔍 **AI-Powered Insights**")
                    st.write("1. Analyze customer behavior to improve security measures.")
                    st.write("2. Learn from patterns to better understand theft risks.")
                    st.write("3. Leverage data to enhance the shopping experience for genuine customers.")
                    
                elif row == 2 and col_index == 1:
                    st.write("🚀 **Future Enhancements**")
                    st.write("1. Refine classification models to improve accuracy and reduce false positives.")
                    st.write("2. Expand notification systems to include SMS or email alerts.")
                    st.write("3. Integrate predictive analytics to forecast potential theft risks.")
