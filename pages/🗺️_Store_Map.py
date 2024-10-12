import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

st.set_page_config(
        page_title="Store Map",
        page_icon="🗺️",
)

image_path = "assets/topview_1.jpeg"

st.image("assets/mini2.png", use_column_width=True)

st.title('🗺️ Visualize the map for your store')

st.write("Depending on camera positions you will get a heatmap of your store that outlines the most dangerous areas for theft.")
st.write("You can also get reccomendations on how to improve the security of your store.")
st.write("**Note that this is an example that we ran on our working area, simulating a store.**")

st.divider()

st.subheader('Step 1: Upload a top view picture of your store')

st.write("Note that this will be used as a coordinate plane for the heatmap.")
st.image(image_path, use_column_width=True)

st.divider()
st.subheader('Step 2: Measure the dimensions of the store (in)')
st.write("For our space the dimensions where: ")
st.write("- Width: 9.7 in")
st.write("- Height: 12.25 in")

st.divider()
st.subheader('Step 3: Divide the image into a coordinate plane')
img = mpimg.imread(image_path)

fig, ax = plt.subplots()
ax.imshow(img)

store_width_in = 9.7
store_height_in = 12.25

num_grid_lines_x = 10
num_grid_lines_y = 10

height, width, _ = img.shape

spacing_x = width / store_width_in
spacing_y = height / store_height_in

for x in range(0, width, int(spacing_x)):
    ax.axvline(x, color='white', linestyle='--', linewidth=1)

for y in range(0, height, int(spacing_y)):
    ax.axhline(y, color='white', linestyle='--', linewidth=1)

ax.set_xlabel('X Coordinate (in)')
ax.set_ylabel('Y Coordinate (in)')
st.pyplot(fig)

st.divider()
st.subheader('Step 4: Add pinpoint locations of cameras')
st.write("Add the locations of the cameras in the store to get the heatmap.")
st.write("For our store we had 4 cameras placed at each corner.")

# Plot camera locations near each corner
camera_locations = [
    (0.5, 0.5),  # Top-left corner
    (store_width_in - 0.5, 0.5),  # Top-right corner
    (0.5, store_height_in - 0.5),  # Bottom-left corner
    (store_width_in - 0.5, store_height_in - 0.5)  # Bottom-right corner
]

# Convert camera locations to pixel coordinates
camera_locations_px = [
    (x * spacing_x, y * spacing_y) for x, y in camera_locations
]

# Plot the camera locations
for (x, y) in camera_locations_px:
    ax.plot(x, y, 'k-')  # 'ro' means red color, circle marker

st.pyplot(fig)
