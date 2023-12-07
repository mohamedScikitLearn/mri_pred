from flask import Flask, jsonify, request
import pydicom
import cv2
import numpy as np
import os
import tensorflow as tf

app = Flask(__name__)

IMG_PX_SIZE = 120
model = tf.keras.models.load_model('oa_def_cor_tse.h5')

print('model loaded')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    # Check if the path is provided
    if not data or 'dicom_path' not in data:
        return jsonify({'error': 'No DICOM path provided'}), 400

    dicom_path = data['dicom_path']
    print('start')

    try:
        # Read the dicom files and extract the slices
        slices = [
            pydicom.read_file(os.path.join(dicom_path, s)) for s in os.listdir(dicom_path)
            if not s.endswith((".nii.gz", 'ipynb_checkpoints'))
        ]
        # Assuming there's at least one DICOM file in the directory
        if 'COR_TSE' in slices[0].SeriesDescription:
            slices.sort(key=lambda x: int(x.ImagePositionPatient[2]))
            slices = [
                cv2.resize(np.array(each_slice.pixel_array), (IMG_PX_SIZE, IMG_PX_SIZE))
                for each_slice in slices
            ]
            norm_slices = [
                cv2.normalize(np.array(each_slice), None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
                for each_slice in slices
            ]

            if len(slices) >= 60:
                new_slices = norm_slices[5:60]
                cropped = [slic[20:100, 20:100] for slic in new_slices]

                scan_test = [cropped]
                processed_scan = np.array(scan_test, dtype=object)
                prediction = model.predict(processed_scan)
                output = {'prediction': prediction.tolist()}
                return jsonify({'response': output})

    except FileNotFoundError:
        print("Wrong file or file path")
        return jsonify({'error': 'File not found'}), 404

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred during prediction'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
