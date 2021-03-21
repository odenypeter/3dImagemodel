import numpy as np
import pandas as pd
from PIL import Image


class ImageSequence:
    """
    Class to hold the necessary information about the image sequence
    """

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
        """
        Method that loads a txt file containing 2D coordinates of image features. The format of each line should be:
        [x y feature_number image_number image_filename]
        """
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
        """
        Method to normalize the coordinates to the range [-1,1]
        """
        mm = (self._width + self._height) / 2

        rows = (self.feat_2d[:, 0] - np.ones(self.number_of_features) * self._width) / mm
        cols = (self.feat_2d[:, 1] - np.ones(self.number_of_features) * self._height) / mm
        return np.dstack((rows, cols)).swapaxes(1, 2)
