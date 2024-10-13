import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

st.set_page_config(
        page_title="Dashboard",
        page_icon="📊",
)

st.title('View general statistics and insights for your store')

# Load JSON data from a file
json_file_path = 'assets/data.json'  # Replace with your JSON file path
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Flatten the JSON data
records = []
for entry in data:
    frame = entry['frame']
    for prediction in entry['predictions']:
        record = {
            'frame': frame,
            'x': prediction['x'],
            'y': prediction['y'],
            'width': prediction['width'],
            'height': prediction['height'],
            'confidence': prediction['confidence'],
            'class': prediction['class'],
            'level': prediction['level']
        }
        records.append(record)

# Create a DataFrame
df = pd.DataFrame(records)

# Create a new column for 5-frame intervals
df['frame_interval'] = (df['frame'] // 5) * 5

# Group by frame_interval and class, then count occurrences
class_counts = df.groupby(['frame_interval', 'class']).size().unstack(fill_value=0)

# Determine the predominant class for each interval
predominant_class = class_counts.idxmax(axis=1)
predominant_class_counts = class_counts.max(axis=1)

# Create a DataFrame for plotting
plot_data = pd.DataFrame({
    'frame_interval': predominant_class.index,
    'predominant_class': predominant_class.values,
    'count': predominant_class_counts.values
})

# Plot 4: Frame Interval vs Predominant Class Line Chart
fig4, ax4 = plt.subplots()
for class_name in plot_data['predominant_class'].unique():
    class_data = plot_data[plot_data['predominant_class'] == class_name]
    ax4.plot(class_data['frame_interval'], class_data['count'], label=class_name)

ax4.set_title('Predominant Class per 5-Frame Interval')
ax4.set_xlabel('Frame Interval')
ax4.set_ylabel('Number of Predictions')
ax4.legend(title='Class')
st.pyplot(fig4)