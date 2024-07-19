class FaceExpressionData:
    def __init__(self, left_eye_open, right_eye_open, mouth_open_x, mouth_open_y, left_iris_x, left_iris_y, right_iris_x, right_iris_y, eyebrow_left, eyebrow_right):
        self.left_eye_open = left_eye_open
        self.right_eye_open = right_eye_open
        self.mouth_open_x = mouth_open_x
        self.mouth_open_y = mouth_open_y
        self.left_iris_x = left_iris_x
        self.left_iris_y = left_iris_y
        self.right_iris_x = right_iris_x
        self.right_iris_y = right_iris_y
        self.eyebrow_left = eyebrow_left
        self.eyebrow_right = eyebrow_right

    #def __repr__(self):
        #return (f"BodyExpressionData(left_eye_open={self.left_eye_open}, "
                #f"right_eye_open={self.right_eye_open}, mouth_open={self.mouth_open}, "
                #f"torso_data={self.torso_data})")