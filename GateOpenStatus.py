import cv2
import time
import numpy as np
import sys

# Define the constants
GATE_THRESHOLD_TOLERANCE: float = 0.03
GATE_THRESHOLD_CHANGE_DECREMENT: float = 0.0001
GATE_THRESHOLD_SMOOTHING = 20


def visualize_on_frame(vis_frame, fps_result, gate_res, avr, std, gate_stat) -> np.ndarray:
    """Draws fps on the input image and return it.
            Args:
                vis_frame: The input RGB image.
                fps_result: The fps Value to be visualized.
                gate_res: The result of the gate detection
                avr: The average of the gate detection
                std: The standard deviation of gate detection
                gate_stat: The status of what the result mean
            Returns:
                frame with fps and threshold result.
            """
    # Visualization parameters
    row_size = 50  # pixels
    left_margin = 50  # pixels
    text_color = (255, 255, 255)  # White
    font_size = 1
    font_thickness = 1

    # Show the FPS
    fps_text = f'FPS = {fps_result:.1f}'
    res_threshold_text = f'threshold = {gate_res.min():.4f}'
    threshold_avr_text = f'average  = {avr:.4f}'
    std_dev_text = f'std deviation = {std:.4f}'
    text_location = (left_margin, row_size)
    cv2.putText(vis_frame, fps_text, text_location, cv2.FONT_HERSHEY_DUPLEX,
                font_size, text_color, font_thickness, cv2.LINE_AA)
    # Show threshold from detection
    cv2.putText(vis_frame, res_threshold_text, (left_margin + 300, row_size), cv2.FONT_HERSHEY_DUPLEX,
                font_size, text_color, font_thickness, cv2.LINE_AA)
    # Show gate status
    cv2.putText(vis_frame, gate_stat, (left_margin, row_size * 2), cv2.FONT_HERSHEY_DUPLEX,
                font_size, text_color, font_thickness, cv2.LINE_AA)
    # Show threshold average
    cv2.putText(vis_frame, std_dev_text, (left_margin + 300, row_size * 3), cv2.FONT_HERSHEY_DUPLEX,
                font_size, text_color, font_thickness, cv2.LINE_AA)
    # Show standard derivation
    cv2.putText(vis_frame, threshold_avr_text, (left_margin + 300, row_size * 2), cv2.FONT_HERSHEY_DUPLEX,
                font_size, text_color, font_thickness, cv2.LINE_AA)
    return vis_frame


gate_condition = 'closed'
confirmation_open = 0
confirmation_closed = 0


def detect_change(gate_state):
    # This function should detect the change in the gate state
    # and return the new state as a string ('open' or 'closed')
    global gate_condition, confirmation_closed, confirmation_open
    new_state = gate_state

    if new_state:
        if gate_condition == 'closed':
            confirmation_closed = 0
            confirmation_open += 1
            if confirmation_open >= GATE_THRESHOLD_SMOOTHING:
                gate_condition = 'open'
                confirmation_open = 0
                print(f"Gate opened -> {time.strftime('%H:%M:%S')}")
    else:
        if gate_condition == 'open':
            confirmation_open = 0
            confirmation_closed += 1
            if confirmation_closed >= GATE_THRESHOLD_SMOOTHING:
                gate_condition = 'closed'
                confirmation_closed = 0
                print(f"Gate closed -> {time.strftime('%H:%M:%S')}")


# Load the gate images
gate = cv2.imread("c:/temp/smartsecurity/mask/gate_closed_night.png", cv2.IMREAD_GRAYSCALE)

# Initialize the VideoCapture object
# cap = cv2.VideoCapture("c:/temp/smartsecurity/learn/Gate_day_long.mp4")
cap = cv2.VideoCapture("rtsp://admin:admin6@192.168.xxx.xxx")
video_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
              int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# Create a black image with the size of the video
mask = np.zeros([video_size[1], video_size[0]], dtype=np.uint8)

# Create the zone of interest where the gate is located in the frame
zone_of_intrest = np.array([[960, 489], [1674, 602], [1734, 319], [988, 183]], dtype=np.int32)

# As the Gate we track is not angled we need the get the minimum and maximum x and y values
min_x = np.min(zone_of_intrest[:, 0])
max_x = np.max(zone_of_intrest[:, 0])
min_y = np.min(zone_of_intrest[:, 1])
max_y = np.max(zone_of_intrest[:, 1])

# Draw mask in the black image by fill the area white
cv2.fillPoly(mask, [zone_of_intrest], (255, 255, 255), )

# As smaller pictures get faster processed put mask on and cut out the zone of interest
masked_gate = cv2.bitwise_and(gate, mask)

# masked_gate = masked_gate[193:587, 970:1714]
masked_gate = masked_gate[min_y:max_y, min_x:max_x]

# Make the test windows smaller
cv2.namedWindow('Detected Gate', cv2.WINDOW_NORMAL)

# Initialize the variable to store the gate state
frame_count = 0

# Create the array
std_dev = np.full(200, 0.0001)
threshold_list = np.full(200, 0.88)
threshold_avr = 0.88

#  Initialize the variable to show fps
counter = 0
i = 0
fps = 0
fps_avg_frame_count = 10
start_time = time.time()

while True:
    # Read the frame from the video
    ret, frame = cap.read()

    if not ret:
        # Later write log entry only
        sys.exit(
            f'ERROR: Unable to read from webcam. Please verify your webcam settings.'
        )
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Put the mask on to remove unnecessary effects
    masked_frame = cv2.bitwise_and(gray_frame, mask)
    # reduce the size for better performance
    masked_frame = masked_frame[min_y:max_y, min_x:max_x]
    # Perform template matching
    res = cv2.matchTemplate(masked_frame, masked_gate, cv2.TM_CCOEFF_NORMED)

    # While the Camara is started set the initial values
    if frame_count == 0:
        threshold_list = np.full(200, res)
    # While Gate is closed do the calculation to avoid status changes through minimal changes
    if gate_condition == "closed":
        i = (i + 1) % len(threshold_list)
        threshold_list[i] = res.min()
        threshold_avr = np.average(threshold_list)
        # through the time the situation may change shadow light, sun, clouds, ....
        std_dev[i] = np.std(threshold_list)
    else:
        # If the Gate is open over hours the threshold will be reduced so the status change will happen.
        if np.average(threshold_list) - std_dev.max() - GATE_THRESHOLD_TOLERANCE < threshold_avr:
            threshold_avr -= GATE_THRESHOLD_CHANGE_DECREMENT

    # If the result is changed so much that the gate status should be changed
    detect_change(res <= threshold_avr - std_dev.max() - GATE_THRESHOLD_TOLERANCE)

    frame_count += 1

    # Calculate the FPS
    if counter % fps_avg_frame_count == 0:
        end_time = time.time()
        fps = fps_avg_frame_count / (end_time - start_time)
        start_time = time.time()

    # add results to frame
    current_frame = visualize_on_frame(masked_frame, fps, res, threshold_avr, std_dev[i], gate_condition)

    # Display the resulting frame
    cv2.imshow('Detected Gate', masked_frame)

    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()
