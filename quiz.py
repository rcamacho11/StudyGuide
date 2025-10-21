import streamlit as st
import random

# -------------------------------
# Define your quiz questions
# -------------------------------
questions = [
    # --- FILTERS ---
    {"question": "What does a Gaussian filter do in image processing?", "options": ["Enhances edges", "Blurs image", "Detects corners", "Sharpens details"], "answer": "Blurs image"},
    {"question": "What is the main reason to apply a Gaussian filter before computing image gradients?", "options": ["To sharpen details", "To remove color", "To reduce noise", "To convert to grayscale"], "answer": "To reduce noise"},
    {"question": "What type of filter highlights edges in an image?", "options": ["Low-pass", "High-pass", "Band-pass", "Median"], "answer": "High-pass"},

    # --- HARRIS CORNER ---
    {"question": "What does the Harris Corner Detector detect?", "options": ["Edges", "Textures", "Uniform regions", "Corners"], "answer": "Corners"},
    {"question": "What kind of region gives a large response in Harris corner detection?", "options": ["Flat region", "Edge", "Corner", "Uniform background"], "answer": "Corner"},

    # --- IMAGE WARPING / STITCHING ---
    {"question": "What is image warping?", "options": ["Rotating pixels", "Transforming coordinates of an image", "Blurring edges", "Enhancing contrast"], "answer": "Transforming coordinates of an image"},
    {"question": "What does homography represent in image stitching?", "options": ["Brightness difference", "Motion blur", "Perspective transformation", "Depth map"], "answer": "Perspective transformation"},

    # --- FITTING / TRANSFORMATIONS ---
    {"question": "Which transformation preserves straight lines and parallelism but not angles?", "options": ["Euclidean", "Affine", "Projective", "Rigid"], "answer": "Affine"},
    {"question": "What do you need to compute a homography?", "options": ["At least 2 points", "At least 4 point correspondences", "One image", "Gradient map"], "answer": "At least 4 point correspondences"},

    # --- LEAST SQUARES / RANSAC ---
    {"question": "What is the goal of least squares fitting?", "options": ["Maximize accuracy", "Minimize sum of squared errors", "Remove outliers", "Detect corners"], "answer": "Minimize sum of squared errors"},
    {"question": "What is RANSAC used for?", "options": ["Detecting texture", "Smoothing image", "Robust model fitting", "Edge detection"], "answer": "Robust model fitting"},
    {"question": "How many points do you need to estimate a homography with RANSAC?", "options": ["2", "3", "4", "8"], "answer": "4"},

    # --- HOUGH TRANSFORM ---
    {"question": "What shape does a single point in image space map to in Hough space?", "options": ["Line", "Circle", "Sinusoid", "Edge"], "answer": "Sinusoid"},
    {"question": "What is the purpose of Hough Transform?", "options": ["Edge smoothing", "Corner detection", "Line detection", "Color matching"], "answer": "Line detection"},

    # --- STEREO ---
    {"question": "What is disparity in stereo vision?", "options": ["Color difference", "Noise level", "Difference in position between left and right views", "Gradient direction"], "answer": "Difference in position between left and right views"},
    {"question": "What does a small disparity value mean in stereo?", "options": ["Object is close", "Object is far", "No object", "Edge detected"], "answer": "Object is far"},

    # --- EXTRA QUESTIONS TO REACH 40 ---
    {"question": "What kind of filter is the Sobel operator?", "options": ["Smoothing filter", "Edge detection filter", "Color filter", "Noise filter"], "answer": "Edge detection filter"},
    {"question": "In Harris detector, what matrix is analyzed for eigenvalues?", "options": ["Gradient matrix", "Structure tensor", "Hessian matrix", "Homography matrix"], "answer": "Structure tensor"},
    {"question": "In image alignment, what does SSD stand for?", "options": ["Single Scale Decomposition", "Sum of Squared Differences", "Structured Spatial Data", "Semi-Stitched Display"], "answer": "Sum of Squared Differences"},
    {"question": "What is a benefit of using RANSAC over least squares?", "options": ["Faster", "Works without data", "Robust to outliers", "Easier math"], "answer": "Robust to outliers"},
    {"question": "In frequency domain filtering, what does the center of the Fourier image represent?", "options": ["High frequencies", "Low frequencies", "Edges", "Textures"], "answer": "Low frequencies"},
    {"question": "Which step in Canny edge detector thins edges?", "options": ["Smoothing", "Gradient calculation", "Non-maximum suppression", "Thresholding"], "answer": "Non-maximum suppression"},
    {"question": "In homography, what does it mean if the determinant is 0?", "options": ["Translation only", "No transformation", "Not invertible", "Pure rotation"], "answer": "Not invertible"},
    {"question": "Which filter removes salt-and-pepper noise?", "options": ["Gaussian", "Median", "Sobel", "Laplacian"], "answer": "Median"},
    {"question": "What does bilinear interpolation use?", "options": ["2 nearest neighbors", "4 surrounding pixels", "1 pixel", "All pixels in row"], "answer": "4 surrounding pixels"},
    {"question": "What does the gradient direction represent in an image?", "options": ["Color change", "Texture", "Direction of steepest intensity change", "Brightness"], "answer": "Direction of steepest intensity change"},
    {"question": "In stereo vision, what are epipolar lines used for?", "options": ["Compute brightness", "Reduce search space", "Enhance corners", "Normalize filters"], "answer": "Reduce search space"},
    {"question": "Which method is best for finding straight lines in edge images?", "options": ["Corner detection", "RANSAC", "Hough transform", "Optical flow"], "answer": "Hough transform"},
    {"question": "What transformation preserves angles and lengths?", "options": ["Affine", "Rigid", "Projective", "Perspective"], "answer": "Rigid"},
    {"question": "Which frequency component captures edges in an image?", "options": ["Low-frequency", "High-frequency", "Band-pass", "DC component"], "answer": "High-frequency"},
    {"question": "What is the role of the structure tensor in corner detection?", "options": ["Smooth image", "Store gradients", "Measure intensity change in all directions", "Apply Gaussian filter"], "answer": "Measure intensity change in all directions"},
    {"question": "What does a high determinant and trace in Harris corner detection indicate?", "options": ["Edge", "Flat", "Corner", "Noise"], "answer": "Corner"},
    {"question": "Which step in Canny helps link weak edges to strong ones?", "options": ["Gradient calculation", "Thresholding", "Hysteresis", "Non-max suppression"], "answer": "Hysteresis"},
    {"question": "What is required to compute depth in stereo vision?", "options": ["One image", "Disparity and baseline", "Two unrelated images", "Edge map only"], "answer": "Disparity and baseline"},
    {"question": "Which transform generalizes affine to include perspective?", "options": ["Rigid", "Similarity", "Projective", "Hough"], "answer": "Projective"},
    {"question": "What does DFT stand for?", "options": ["Direct Filter Transform", "Discrete Fourier Transform", "Dual Frame Transformation", "Directional Fourier Test"], "answer": "Discrete Fourier Transform"}
,
{
"question": "What effect does applying a Gaussian filter in the spatial domain have on an image in the frequency domain?",
"options": [
"High-frequency components are enhanced",
"Low-frequency components are suppressed",
"High-frequency components are suppressed",
"Image is binarized"
],
"answer": "High-frequency components are suppressed"
},
{
"question": "Which of the following is true about the Laplacian filter?",
"options": [
"It smooths the image by averaging pixel values",
"It sharpens the image by emphasizing edges",
"It performs a color histogram equalization",
"It reduces noise by median filtering"
],
"answer": "It sharpens the image by emphasizing edges"
},


# 2. Harris Corner Detection
{
"question": "What does the Harris corner detector look for in an image?",
"options": [
"High-frequency gradients",
"Strong changes in intensity in all directions",
"Large flat regions",
"Edges only in the x-direction"
],
"answer": "Strong changes in intensity in all directions"
},
{
"question": "Which matrix is used in Harris corner detection to analyze local image structure?",
"options": [
"Hessian matrix",
"Structure tensor (second moment matrix)",
"Laplacian of Gaussian",
"Fourier transform matrix"
],
"answer": "Structure tensor (second moment matrix)"
},


# 3. Image Warping & Stitching
{
"question": "In homography estimation, why must point correspondences be non-collinear?",
"options": [
"To avoid Gaussian noise",
"To ensure invertibility of the system",
"To reduce image blur",
"To improve filter responses"
],
"answer": "To ensure invertibility of the system"
},
{
"question": "If you want to stitch two images that share a planar surface (e.g., a poster), which transformation is appropriate?",
"options": ["Translation", "Affine", "Similarity", "Homography"],
"answer": "Homography"
},



]

# Shuffle once
if "shuffled_questions" not in st.session_state:
    random.shuffle(questions)
    st.session_state.shuffled_questions = questions
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.submitted = False
    st.session_state.selected = None

# Get current question
q_index = st.session_state.current_q
current_q = st.session_state.shuffled_questions[q_index]

# UI
st.set_page_config(page_title="🧪 CSE 185 Quiz", layout="centered")
st.title("🧪 CSE 185 Midterm Practice Quiz")
st.write(f"**Question {q_index + 1} of {len(questions)}**")

# Show options
selected = st.radio(
    current_q["question"],
    current_q["options"],
    key=f"radio_{q_index}"
)

# Submit logic
if st.button("Submit Answer") and not st.session_state.submitted:
    st.session_state.selected = selected
    st.session_state.submitted = True
    if selected == current_q["answer"]:
        st.success("✅ Correct!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Incorrect. The correct answer is: **{current_q['answer']}**")

# Next Question
if st.session_state.submitted:
    if st.button("Next Question"):
        if q_index < len(questions) - 1:
            st.session_state.current_q += 1
            st.session_state.submitted = False
            st.session_state.selected = None
            st.rerun()
        else:
            st.balloons()
            st.success(f"🎉 Quiz complete! Your final score: **{st.session_state.score} / {len(questions)}**")