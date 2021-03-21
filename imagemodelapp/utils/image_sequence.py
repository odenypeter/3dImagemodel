import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

from os.path import join
from django.conf import settings
import cv2


class ImageSequence:
    '''
    Class to hold the necessary information about the image sequence
    '''

    def __init__(self, json_data):
        self.load_features(json_data)

    @property
    def feat_2d(self):
        return self._feat_2d

    @feat_2d.setter
    def feat_2d(self, value):
        self._feat_2d = value

    @property
    def length(self):
        return self._length

    @property
    def number_of_features(self):
        return self._number_of_features

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def load_features(self, json_data):
        '''
        Method that loads a txt file containing 2D coordinates of image features. The format of each line should be:
        [x y feature_number image_number image_filename]
        '''
        features_df = pd.DataFrame(json_data)
        # get length of sequence and number of features
        self._length = int(features_df['image_id'].max())
        self._number_of_features = int(features_df['feature_id'].max())

        self.feat_2d = np.zeros(shape=[self._length, 4, self._number_of_features])
        for i in range(1, self._length + 1):
            self.feat_2d[i - 1, :, :] = np.transpose(features_df.loc[features_df['image_id'] == i].values)[0:4]

        # keep the image filenames
        self._image_filenames = features_df.image_filename.unique()

        image = Image.open(self._image_filenames[0])
        self._width = image.width
        self._height = image.height

    def get_normalized_coordinates(self):
        '''
        Method to normalize the coordinates to the range [-1,1]
        '''
        mm = (self._width + self._height) / 2

        rows = (self.feat_2d[:, 0] - np.ones(self.number_of_features) * self._width) / mm
        cols = (self.feat_2d[:, 1] - np.ones(self.number_of_features) * self._height) / mm
        return np.dstack((rows, cols)).swapaxes(1, 2)

    def show(self):
        '''
        Method to display the sequence, with the 2D features superimposed
        '''
        font = ImageFont.truetype('/Library/fonts/arial.ttf', 30)
        for i in range(0, self.length):
            filename = self._image_filenames[i]
            image = Image.open(filename)
            draw = ImageDraw.Draw(image)
            for j in range(0, self.number_of_features):
                x = self.feat_2d[i, :, j][0]
                y = image.height - self.feat_2d[i, :, j][1]
                draw.text((x, y), "+" + str(j), font=font, fill=(0, 255, 0))

            image.show()

    # Feature extractor
    def extract_features(self, image_path, vector_size=16):
        image = cv2.imread(image_path)
        try:
            # Using KAZE, cause SIFT, ORB and other was moved to additional module
            # which is adding addtional pain during install
            alg = cv2.KAZE_create()
            # Dinding image keypoints
            kps = alg.detect(image)
            # Getting first 32 of them.
            # Number of keypoints is varies depend on image size and color pallet
            # Sorting them based on keypoint response value(bigger is better)
            kps = sorted(kps, key=lambda x: -x.response)[:vector_size]

            # computing descriptors vector
            kps, dsc = alg.compute(image, kps)
            all_points = []
            for kp in kps:
                all_points.append([kp.pt[0], kp.pt[1]])
            # # Flatten all of them in one big vector - our feature vector
            # dsc = dsc.flatten()
            # # Making descriptor of same size
            # # Descriptor vector size is 64
            # needed_size = (vector_size * 64)
            # if dsc.size < needed_size:
            #     # if we have less the 32 descriptors then just adding zeros at the
            #     # end of our feature vector
            #     dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
        except cv2.error as e:
            print('Error: ', e)
            return None

        return all_points
