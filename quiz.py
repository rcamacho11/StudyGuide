import streamlit as st
import random

questions = [
    # --- FILTERS ---
    {"question": "What does a Gaussian filter do in image processing?",
     "options": ["Enhances edges", "Blurs image", "Detects corners", "Sharpens details"],
     "answer": "Blurs image",
     "why": "A Gaussian filter smooths the image by averaging pixel values, reducing noise and small detail variations."},

    {"question": "What is the main reason to apply a Gaussian filter before computing image gradients?",
     "options": ["To sharpen details", "To remove color", "To reduce noise", "To convert to grayscale"],
     "answer": "To reduce noise",
     "why": "Gradients amplify noise; smoothing with a Gaussian filter ensures more stable edge responses."},

    {"question": "What type of filter highlights edges in an image?",
     "options": ["Low-pass", "High-pass", "Band-pass", "Median"],
     "answer": "High-pass",
     "why": "High-pass filters preserve sharp intensity transitions, emphasizing edges and fine details."},

    # --- HARRIS CORNER ---
    {"question": "What does the Harris Corner Detector detect?",
     "options": ["Edges", "Textures", "Uniform regions", "Corners"],
     "answer": "Corners",
     "why": "It identifies points where intensity changes in both directions, which are corners."},

    {"question": "What kind of region gives a large response in Harris corner detection?",
     "options": ["Flat region", "Edge", "Corner", "Uniform background"],
     "answer": "Corner",
     "why": "Corners cause strong gradient changes in all directions, producing high eigenvalues in the structure tensor."},

    # --- IMAGE WARPING / STITCHING ---
    {"question": "What is image warping?",
     "options": ["Rotating pixels", "Transforming coordinates of an image", "Blurring edges", "Enhancing contrast"],
     "answer": "Transforming coordinates of an image",
     "why": "Warping changes how pixels map to new coordinates, enabling scaling, rotation, or perspective correction."},

    {"question": "What does homography represent in image stitching?",
     "options": ["Brightness difference", "Motion blur", "Perspective transformation", "Depth map"],
     "answer": "Perspective transformation",
     "why": "A homography is a 3×3 matrix that relates two planar views of the same scene under perspective projection."},

    # --- FITTING / TRANSFORMATIONS ---
    {"question": "Which transformation preserves straight lines and parallelism but not angles?",
     "options": ["Euclidean", "Affine", "Projective", "Rigid"],
     "answer": "Affine",
     "why": "Affine transformations maintain lines and parallelism but allow non-uniform scaling and shearing."},

    {"question": "What do you need to compute a homography?",
     "options": ["At least 2 points", "At least 4 point correspondences", "One image", "Gradient map"],
     "answer": "At least 4 point correspondences",
     "why": "Four point pairs are required to solve the eight unknowns in a 3×3 homography matrix."},

    # --- LEAST SQUARES / RANSAC ---
    {"question": "What is the goal of least squares fitting?",
     "options": ["Maximize accuracy", "Minimize sum of squared errors", "Remove outliers", "Detect corners"],
     "answer": "Minimize sum of squared errors",
     "why": "It minimizes the total squared distance between observed and predicted values for best fit."},

    {"question": "What is RANSAC used for?",
     "options": ["Detecting texture", "Smoothing image", "Robust model fitting", "Edge detection"],
     "answer": "Robust model fitting",
     "why": "RANSAC fits models while ignoring outliers, making it ideal for noisy feature matching."},

    {"question": "How many points do you need to estimate a homography with RANSAC?",
     "options": ["2", "3", "4", "8"],
     "answer": "4",
     "why": "Four pairs of matching points give enough equations to compute the 8 degrees of freedom in a homography."},

    # --- HOUGH TRANSFORM ---
    {"question": "What shape does a single point in image space map to in Hough space?",
     "options": ["Line", "Circle", "Sinusoid", "Edge"],
     "answer": "Sinusoid",
     "why": "Each image-space point corresponds to a sinusoidal curve in parameter space representing all possible lines through it."},

    {"question": "What is the purpose of Hough Transform?",
     "options": ["Edge smoothing", "Corner detection", "Line detection", "Color matching"],
     "answer": "Line detection",
     "why": "The Hough transform accumulates votes in parameter space to detect lines even in noisy or broken edge maps."},

    # --- STEREO ---
    {"question": "What is disparity in stereo vision?",
     "options": ["Color difference", "Noise level", "Difference in position between left and right views", "Gradient direction"],
     "answer": "Difference in position between left and right views",
     "why": "Disparity measures how far a point shifts between left and right camera images."},

    {"question": "What does a small disparity value mean in stereo?",
     "options": ["Object is close", "Object is far", "No object", "Edge detected"],
     "answer": "Object is far",
     "why": "Objects farther away appear almost aligned in both cameras, producing small disparity values."},

    # --- EXTRA QUESTIONS ---
    {"question": "What kind of filter is the Sobel operator?",
     "options": ["Smoothing filter", "Edge detection filter", "Color filter", "Noise filter"],
     "answer": "Edge detection filter",
     "why": "Sobel filters compute gradients to highlight regions of rapid intensity change (edges)."},

    {"question": "In Harris detector, what matrix is analyzed for eigenvalues?",
     "options": ["Gradient matrix", "Structure tensor", "Hessian matrix", "Homography matrix"],
     "answer": "Structure tensor",
     "why": "The structure tensor captures local gradient information used to assess corner strength via eigenvalues."},

    {"question": "In image alignment, what does SSD stand for?",
     "options": ["Single Scale Decomposition", "Sum of Squared Differences", "Structured Spatial Data", "Semi-Stitched Display"],
     "answer": "Sum of Squared Differences",
     "why": "SSD measures how similar two image patches are by summing squared intensity differences pixel-wise."},

    {"question": "What is a benefit of using RANSAC over least squares?",
     "options": ["Faster", "Works without data", "Robust to outliers", "Easier math"],
     "answer": "Robust to outliers",
     "why": "RANSAC ignores incorrect matches, while least squares is highly affected by outliers."},

    {"question": "In frequency domain filtering, what does the center of the Fourier image represent?",
     "options": ["High frequencies", "Low frequencies", "Edges", "Textures"],
     "answer": "Low frequencies",
     "why": "The DC component and nearby values at the center represent smooth variations and overall brightness."},

    {"question": "Which step in Canny edge detector thins edges?",
     "options": ["Smoothing", "Gradient calculation", "Non-maximum suppression", "Thresholding"],
     "answer": "Non-maximum suppression",
     "why": "This step keeps only the strongest pixel in the gradient direction, making edges one pixel thick."},

    {"question": "In homography, what does it mean if the determinant is 0?",
     "options": ["Translation only", "No transformation", "Not invertible", "Pure rotation"],
     "answer": "Not invertible",
     "why": "A zero determinant means the transformation collapses to a lower dimension, losing information."},

    {"question": "Which filter removes salt-and-pepper noise?",
     "options": ["Gaussian", "Median", "Sobel", "Laplacian"],
     "answer": "Median",
     "why": "The median filter replaces each pixel with the neighborhood median, removing isolated outlier pixels."},

    {"question": "What does bilinear interpolation use?",
     "options": ["2 nearest neighbors", "4 surrounding pixels", "1 pixel", "All pixels in row"],
     "answer": "4 surrounding pixels",
     "why": "It averages four neighboring pixels weighted by their distances to produce smoother resizing results."},

    {"question": "What does the gradient direction represent in an image?",
     "options": ["Color change", "Texture", "Direction of steepest intensity change", "Brightness"],
     "answer": "Direction of steepest intensity change",
     "why": "Gradient direction indicates where the image intensity increases most rapidly, perpendicular to edges."},

    {"question": "In stereo vision, what are epipolar lines used for?",
     "options": ["Compute brightness", "Reduce search space", "Enhance corners", "Normalize filters"],
     "answer": "Reduce search space",
     "why": "Matching points must lie on corresponding epipolar lines, reducing correspondence search from 2D to 1D."},

    {"question": "Which method is best for finding straight lines in edge images?",
     "options": ["Corner detection", "RANSAC", "Hough transform", "Optical flow"],
     "answer": "Hough transform",
     "why": "The Hough transform identifies dominant line patterns by accumulating votes in parameter space."},

    {"question": "What transformation preserves angles and lengths?",
     "options": ["Affine", "Rigid", "Projective", "Perspective"],
     "answer": "Rigid",
     "why": "Rigid transformations include only rotation and translation, keeping distances and angles unchanged."},

    {"question": "Which frequency component captures edges in an image?",
     "options": ["Low-frequency", "High-frequency", "Band-pass", "DC component"],
     "answer": "High-frequency",
     "why": "Edges are sharp intensity transitions, corresponding to high‑frequency components in the spectrum."},

    {"question": "What is the role of the structure tensor in corner detection?",
     "options": ["Smooth image", "Store gradients", "Measure intensity change in all directions", "Apply Gaussian filter"],
     "answer": "Measure intensity change in all directions",
     "why": "It summarizes local gradients to quantify how much intensity varies along different directions."},

    {"question": "What does a high determinant and trace in Harris corner detection indicate?",
     "options": ["Edge", "Flat", "Corner", "Noise"],
     "answer": "Corner",
     "why": "Both eigenvalues are large, meaning strong intensity change in x and y — a corner region."},

    {"question": "Which step in Canny helps link weak edges to strong ones?",
     "options": ["Gradient calculation", "Thresholding", "Hysteresis", "Non-max suppression"],
     "answer": "Hysteresis",
     "why": "Hysteresis connects weak edge pixels to nearby strong ones, ensuring continuous edge curves."},

    {"question": "What is required to compute depth in stereo vision?",
     "options": ["One image", "Disparity and baseline", "Two unrelated images", "Edge map only"],
     "answer": "Disparity and baseline",
     "why": "Depth is obtained via triangulation using disparity and the distance (baseline) between the cameras."},

    {"question": "Which transform generalizes affine to include perspective?",
     "options": ["Rigid", "Similarity", "Projective", "Hough"],
     "answer": "Projective",
     "why": "Projective transformations include perspective distortions like foreshortening and vanishing points."},

    {"question": "What does DFT stand for?",
     "options": ["Direct Filter Transform", "Discrete Fourier Transform", "Dual Frame Transformation", "Directional Fourier Test"],
     "answer": "Discrete Fourier Transform",
     "why": "The DFT converts an image from spatial to frequency representation for analysis or filtering."},

    {"question": "What effect does applying a Gaussian filter in the spatial domain have on an image in the frequency domain?",
     "options": ["High-frequency components are enhanced", "Low-frequency components are suppressed", "High-frequency components are suppressed", "Image is binarized"],
     "answer": "High-frequency components are suppressed",
     "why": "Gaussian smoothing removes high‑frequency noise, equivalent to low‑pass filtering in frequency space."},

    {"question": "Which of the following is true about the Laplacian filter?",
     "options": ["It smooths the image by averaging pixel values", "It sharpens the image by emphasizing edges", "It performs a color histogram equalization", "It reduces noise by median filtering"],
     "answer": "It sharpens the image by emphasizing edges",
     "why": "The Laplacian is a second‑derivative operator that highlights rapid intensity changes, sharpening edges."},

    {"question": "What does the Harris corner detector look for in an image?",
     "options": ["High-frequency gradients", "Strong changes in intensity in all directions", "Large flat regions", "Edges only in the x-direction"],
     "answer": "Strong changes in intensity in all directions",
     "why": "Corners show large gradient magnitudes in both x and y, giving high corner response values."},

    {"question": "Which matrix is used in Harris corner detection to analyze local image structure?",
     "options": ["Hessian matrix", "Structure tensor (second moment matrix)", "Laplacian of Gaussian", "Fourier transform matrix"],
     "answer": "Structure tensor (second moment matrix)",
     "why": "This matrix encodes local gradient variations used to compute corner strength via eigenvalue analysis."},

    {"question": "In homography estimation, why must point correspondences be non-collinear?",
     "options": ["To avoid Gaussian noise", "To ensure invertibility of the system", "To reduce image blur", "To improve filter responses"],
     "answer": "To ensure invertibility of the system",
     "why": "Collinear points don't provide enough independent constraints; the matrix becomes singular."},

    {"question": "If you want to stitch two images that share a planar surface (e.g., a poster), which transformation is appropriate?",
     "options": ["Translation", "Affine", "Similarity", "Homography"],
     "answer": "Homography",
     "why": "Planar scenes are related by a projective transformation (homography) that accounts for perspective shifts."},

    {"question": "In the frequency domain, convolution corresponds to multiplication.",
     "options": ["True", "False"],
     "answer": "True",
     "why": "According to the convolution theorem, convolution in one domain equals multiplication in the other."},

    {"question": "A small standard deviation in a Gaussian filter will blur the image more than a large standard deviation.",
     "options": ["True", "False"],
     "answer": "False",
     "why": "A small sigma gives a narrow kernel and less blur; a large sigma spreads the blur more."},

    {"question": "Harris corner detection is based on computing image gradients in both x and y directions.",
     "options": ["True", "False"],
     "answer": "True",
     "why": "It uses partial derivatives Ix and Iy to evaluate local intensity changes in both directions."},

    {"question": "The determinant and trace of the Harris matrix are used to classify pixels as edges, corners, or flat regions.",
     "options": ["True", "False"],
     "answer": "True",
     "why": "These values describe eigenvalue behavior that differentiates flat, edge, and corner areas."},

    {"question": "Image warping is only possible if the input and output images are the same size.",
     "options": ["True", "False"],
     "answer": "False",
     "why": "Warping remaps coordinates; input and output can have any dimensions."},

    {"question": "RANSAC is robust to outliers in feature matching.",
     "options": ["True", "False"],
     "answer": "True",
     "why": "RANSAC discards inconsistent matches while computing a model that fits inliers well."},

    {"question": "Hough transform maps every point in the image space to a point in parameter space.",
     "options": ["True", "False"],
     "answer": "False",
     "why": "Each image-space point maps to a curve (sinusoid) representing all possible line parameters."},

    {"question": "Stereo disparity is higher for objects that are farther away.",
     "options": ["True", "False"],
     "answer": "False",
     "why": "Closer objects appear more shifted between views, giving larger disparity values."},

    {"question": "Non-maximum suppression in Canny edge detection is used to thin out edges.",
     "options": ["True", "False"],
     "answer": "True",
     "why": "It removes weak neighboring pixels along the gradient direction, leaving thin edges."},

    {"question": "The least squares solution finds the best line through data by minimizing the sum of squared perpendicular distances.",
     "options": ["True", "False"],
     "answer": "False",
     "why": "Standard least squares minimizes vertical residuals, not perpendicular distances."}
]

# -------------------------------
# Streamlit App
# -------------------------------
st.set_page_config(page_title="🧪 CSE 185 Quiz", layout="centered")
st.title("🧪 CSE 185 Midterm Practice Quiz")

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
st.write(f"**Question {q_index + 1} of {len(questions)}**")
selected = st.radio(current_q["question"], current_q["options"], key=f"radio_{q_index}")

# Submit logic
if st.button("Submit Answer") and not st.session_state.submitted:
    st.session_state.selected = selected
    st.session_state.submitted = True
    if selected == current_q["answer"]:
        st.success("✅ Correct!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Incorrect. The correct answer is: **{current_q['answer']}**")
        if "why" in current_q:
            st.info(f"💡 **Explanation:** {current_q['why']}")

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
            st.success(f"🎉 Quiz complete! Final score: **{st.session_state.score} / {len(questions)}**")
