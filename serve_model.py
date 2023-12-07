# serve_model.py

from flask import Flask, request, jsonify
import tensorflow as tf

app = Flask(__name__)

# Load the model
model = tf.keras.models.load_model('model.h5')
dicom_path='/dicom_path'
@app.route('/predict', methods=['POST'])
def predict():
    message = request.get_json(force=True)
    try:
        # Read the dicom file and extract the slices 
        slices = [pydicom.read_file(os.path.join(dicom_path + '/' + s)) for s in os.listdir(dicom_path) if not s.endswith((".nii.gz",'ipynb_checkpoints'))]
        if ('COR_TSE' in pydicom.dcmread(dicom_path + '/' + s).SeriesDescription):

            slices.sort(key = lambda x: int(x.ImagePositionPatient[2]))
            slices = [cv2.resize(np.array(each_slice.pixel_array),(IMG_PX_SIZE,IMG_PX_SIZE)) for each_slice in slices]
            norm_slices = [cv2.normalize(np.array(each_slice), None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX,
                           dtype=cv2.CV_32F)for each_slice in slices]
           
            if len(slices)>=60:
                new_slices= norm_slices[5:60]
                croped=[]
                for slic in new_slices:
                    crop = slic[20:100, 20:100]
                    croped.append(crop)
                scan_test.append(croped)

    except FileNotFoundError:
        print("Wrong file or file path")

        processed_scan= np.array(scan_test,dtype=object)

        prediction = model.predict(processed_scan)
        output = {'prediction': prediction.tolist()}

        return jsonify({'response': output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
