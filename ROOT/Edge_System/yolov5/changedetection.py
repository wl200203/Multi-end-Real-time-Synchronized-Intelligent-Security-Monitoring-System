import os
import cv2
import pathlib
import requests
from datetime import datetime


class ChangeDetection:
    # Class variables
    result_prev = []  # Stores the detection results from the previous frame
    HOST = 'http://127.0.0.1:8000/api_root'  # Django API server URL
    username = 'wangxudong020306'  # Replace with your username
    password = 'QQyxy0207'  # Replace with your password
    token = 'fe3abce52b877b6eb00422f27c5756003ab3af1d' # Variable to store the authentication token
    title = ''  # Title for the detection result
    text = ''  # Description of the detection result

    # Constructor: Initializes detection results and retrieves the authentication token
    def __init__(self, names):
        self.result_prev = [0 for _ in range(len(names))]  # Initialize the detection state for each object
        # Send a POST request to the server to authenticate and retrieve the token
        res = requests.post(self.HOST + '/api-token-auth/', {
            'username': self.username,
            'password': self.password,
        })
        res.raise_for_status()  # Raise an error if the request fails
        self.token = res.json()['token']  # Store the token
        print(self.token)  # Print the token for debugging purposes

    # Method to add new detection results and check for state changes
    def add(self, names, detected_current, save_dir, image):
        self.title = ""  # Reset the title for the new detection result
        self.text = ""  # Reset the description
        change_flag = 0  # Flag to indicate if there is a state change
        i = 0
        while i < len(self.result_prev):  # Iterate through the detection results
            if self.result_prev[i] == 0 and detected_current[i] == 1:  # Detect a new object
                change_flag = 1
                self.title = names[i]  # Update the title with the detected object name
                self.text += names[i] + ","  # Append the object name to the description
            i += 1

        self.result_prev = detected_current[:]  # Update the previous detection state

        if change_flag == 1:  # If there is a state change, send the result to the server
            self.send(save_dir, image)

    # Method to send detection results to the server
    def send(self, save_dir, image):
        now = datetime.now()  # Get the current time
        today = datetime.now()  # Get the current date
        # Build the path to save the detected image
        #save_path = os.getcwd() + save_dir + '/detected/' + str(today.year) + '/' + str(today.month) + '/' + str(today.day)
        save_path = os.path.join(os.getcwd(), save_dir, 'detected', str(today.year), str(today.month), str(today.day))
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist

        # Generate the full path for the image file with a timestamp
        full_path = save_path + '/{0}-{1}-{2}-{3}.jpg'.format(
            today.hour, today.minute, today.second, today.microsecond
        )

        # Resize the image and save it to the full path
        dst = cv2.resize(image, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        cv2.imwrite(full_path, dst)

        # Set the request headers for authentication
        #headers = {
            #'Authorization': 'JWT ' + self.token,
            #'Accept': 'application/json',
        #}
        headers = {'Authorization': f'Token {self.token}'}

        # Build the POST request data
        data = {
            'title': self.title,  # Detected object name
            'text': self.text,  # Detected object details
            'created_date': now.isoformat(),  # Current timestamp
            'published_date': now.isoformat(),  # Current timestamp
        }

        # Open the detected image file and send it to the server
        file = {'image': open(full_path, 'rb')}
        res = requests.post(self.HOST + '/api-root/Post/', data=data, files=file, headers=headers)
        print(res)  # Print the server response for debugging purposes
