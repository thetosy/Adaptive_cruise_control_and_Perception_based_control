# code reuse partial of https://github.com/harshilpatel312/KITTI-distance-estimation
"""This file contains the NN-based distance predictor.

Here, you will design the NN module for distance prediction
"""
from mp1_distance_predictor.inference_distance import infer_dist
from mp1_distance_predictor.detect import detect_cars

from pathlib import Path
from keras.models import load_model
from keras.models import model_from_json


# NOTE: Very important that the class name remains the same
class Predictor:
    def __init__(self):
        self.detect_model = None
        self.distance_model = None
        # Keep track of previous distance
        self.prev_distance = None

    def initialize(self):
        # Load YOLOv3 car detection model
        self.detect_model = load_model('mp1_distance_predictor/model.h5')
        # Load distance prediction model
        self.distance_model = self.load_inference_model()

    def load_inference_model(self):
        MODEL = 'distance_model'
        WEIGHTS = 'distance_model'

        # Load JSON and create distance prediction model
        json_file = open('mp1_distance_predictor/distance_model_weights/{}.json'.format(MODEL), 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)

        # Load weights into the distance prediction model
        loaded_model.load_weights("mp1_distance_predictor/distance_model_weights/{}.h5".format(WEIGHTS))
        print("Loaded model from disk")

        # Compile the loaded model
        loaded_model.compile(loss='mean_squared_error', optimizer='adam')
        return loaded_model

    def predict(self, obs) -> float:
        """This is the main predict step of the NN.

        Here, the provided observation is an Image. Your goal is to train a NN that can
        use this image to predict distance to the lead car.

        """
        data = obs
        image_name = 'camera_images/vision_input.png'
        # Load a trained YOLOv3 model to detect car bounding box
        car_bounding_box = detect_cars(self.detect_model, image_name)
        # Different dist_test will have effect on the prediction
        # You can play with the number of dist_test
        dist_test = data.distance_to_lead

        if car_bounding_box is not None:
            # If car is detected, use the distance prediction model
            dist = infer_dist(self.distance_model, car_bounding_box, [[dist_test]])
            # Update previous distance
            self.prev_distance = dist
        else:
            print("No car detected")
            # If no car detected what would you do for the distance prediction
            # Do your magic...
            if self.prev_distance is not None:
                # If no car detected, maintain the previous known distance
                dist = self.prev_distance
                print("Maintaining previous distance: ", dist)
            else:
                # If no previous distance is available, set a default distance
                dist = 20
                print("Setting default distance: ", dist)

        print("estimated distance: ", dist)
        return dist
