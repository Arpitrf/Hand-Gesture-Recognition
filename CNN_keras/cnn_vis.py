from keras.models import load_model
from keras.utils import plot_model

model = load_model('my_model.h5')
print (model.summary())

#plot_model(model, to_file='model.png')