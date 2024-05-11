import tflite_runtime.interpreter as tf
import numpy as np


class AccelerationClassifier(object):
    def __init__(
        self,
        model_path='./models/nn_gesture.tflite',
        num_threads=1,
    ):
        self.interpreter = tf.Interpreter(model_path=model_path, num_threads=num_threads)

        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        print(self.input_details)
        self.output_details = self.interpreter.get_output_details()

    def __call__(
        self,
        averaged_list,
    ):
        input_details_tensor_index = self.input_details[0]['index']
        self.interpreter.set_tensor(
            input_details_tensor_index,
            np.asarray([averaged_list], dtype=np.float32))
        self.interpreter.invoke()

        output_details_tensor_index = self.output_details[0]['index']

        result = self.interpreter.get_tensor(output_details_tensor_index)

        result_index = np.argmax(np.squeeze(result))

        return result_index
