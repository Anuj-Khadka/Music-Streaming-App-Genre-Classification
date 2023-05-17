from tensorflow import keras
from keras.models import load_model
import numpy as np

def predict_genre(X_to_predict):
    genre_dict = {0:"hiphop",1:"country",2:"jazz",3:"classical",4:"metal",5:"pop",6:"rock",7:"blues",8:"reggae",9:"disco"}
    # load the model
    model = load_model('model\Music_Genre_10_CNN_02.h5')
    prediction = model.predict(X_to_predict)
    print(prediction)
    # get index with max value
    predicted_index = np.argmax(prediction, axis=1)

    return(genre_dict[int(predicted_index)])
    