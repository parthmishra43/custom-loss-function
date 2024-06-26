import tensorflow as tf
from tensorflow import keras

# Use fetch_california_housing() function to load the data.
# This dataset contains only numerical features (there is no ocean_proximity feature)
# And there is no missing value.
# After loading the data, we split it into a training set, a validation set, and a test set
# And we scale all the features


from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# fetch the data
housing = fetch_california_housing()

# split it into a training set, a validation set, and a test set
X_train_full, X_test, y_train_full, y_test = train_test_split(
    housing.data, housing.target.reshape(-1, 1), random_state=42)
X_train, X_valid, y_train, y_valid = train_test_split(
    X_train_full, y_train_full, random_state=42)

# Scale all the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_valid_scaled = scaler.transform(X_valid)
X_test_scaled = scaler.transform(X_test)

"""Custom Loss Function - Huber Loss

![hl.png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASYAAAA8BAMAAAA50AqgAAAAMFBMVEX///+enp4WFhbMzMwwMDCKiopAQEAMDAzm5uZ0dHS2trZQUFAEBAQiIiJiYmIAAAAwCtEKAAAAAXRSTlMAQObYZgAAAAlwSFlzAAAOxAAADsQBlSsOGwAABylJREFUaAW9WW2IVFUYfub7zuzuzCDRjxRZkrIPqrEWw8J2bAMxql2KMpFwohClwA1MmgK9KeUPrblFSJtU94etQeUMSOlSrYuWaEFsRCAJcUGDto91zcz1c3vPOffcz9mZO7vOHth5P87zvufZe88959z3AkFb7FhQ5Mzhuo2ZGyvgSG2nAwJnEHaqZwYHCzZU5J9guJlEtZzlo7XlzEH3nNRncviqYyXOMHfsK5OTYqSOVMUFdO43cVIGDHPDMuPcbjU5pcbQ2JxPf6E5E3aZhpRW3+z5hqXXUzJjHCE5QVf4hasXZvW/H89bOimSi5RAyOD9RijrxNXUvZwQr9TEeztvdzskFykRuzHHEcNuXE3Lx2lHTbivs+j2SC5SJjeoArDMjatpeTmFDKUm3ttZm1P6FdUMKOveyMltJ6dPRv/Eni3vTQ729/QfXIt7+/Zj1oUdBdZL1yc1OFox59W2jVbE8l5LrasITqFTdG1j7ZHzkYmJsboxTkARqZtwt4qLr/FBidOj6NQEpxb7Ii6+57wzqrZuXicG6syhsWeOBRWR0BAt4DAz2HWKnEEmJzhtlrMKyndYLwBBfh2c7kdoKEiIC1NEOYfkEI4Kbxei7Zgj14TPfjGx8QIedoXVNASnCWq4gpZGnliRtohVxGkc3wqzCxkDX0tO6PhRuDNZrK5Jw9VpX6fIaYQNV18Qg1+n9JjNqTMLWrPkXVt4A0/SCQglSErYnGgBL2W1QEEOUBGtNJ/yNqdSTjmdtDhh280MXIIy5AiqowpOqdEHgRdw4FW9DtzXvRGhl7BbhTheEJdEtmX8OpsT0hWKadPjPYr9FPIsJ0SuKkuP4PQmPlWx8IOWAd+YdRz9l55B/+ga7Dq3hiPpuVtrfGmuBXasMvAblINk/33puOmN9QglqpoOWwhOZdAsvBpNziMpnTmTZKSsZarD7IrknRium/cOpZyvayoOyUVKZ44YGWlxNCKNJotoS6RiyVK7UJ+zPNNSJBcu77yeNTafeFtAv229poF2qVwjFUuWC1xNCmG5p6q4OHmS9JCdKZhOe8CMBwYcyHLXXKi+rqk49ppBUnpzlBkx1tqYwjZ9hAUD7uU/ymUuUr8v0m1nE7UPVTN5WBebPhDVyBXnt/k23hk+xEUnbS0z0h6So7SqctNvqUifKZ/PeRxNNr+h/CpOzgObRWLTTxfcY4aPue1mWxFanhQtoqnIqDA3fS+nRKHZLNz5k3RAS6uYB9CLkrnpxw3COOfT0pm9d9EhoAPKUiChw9z0oz1u3ggf8Tiaa7bmkXoR126mo4QmN31i524RsRa4nU2z4ndseHbTkNJLU4itmWLTT/iGW6f7XNUcP1VzTtEXy9MUUnpl9EqpWHJV3lKRzkHWHqQ0O1eKZQyoctqx4wNqoUJYBZ6WaP+/WxJ8Z883gMftM6vct2Qg50SgqCo9HrnrZ4+DmXP0Kk5g8A9yv2F2pQo+jDirgJUYIvk6nAjEMP62BWArj6/t1n0uyxEyhBq1PJZichomR1Svw4mBlliRDuUj0osOO5D6mEC96webnJZRT5j+5D2TUgbwe8dA/tMOOT+nv4Y5ydR+aXIq6wCrqEguUsoAzomB/KcdIMleEKpxWpCT8Q1JkxMrMbBZSlwcNQg7E+fEQN7TDitgPHF5tYriipMqQgODrJyxdtO8dRdjEye6tdDIqIHZOw07UwBNcOIlhlsITpzsGoQdPvdfDeAgftqxO0QBg12n9bloAU+xkhqVMzr1dDveole/DoQqsWE0drLmnESJgW0zrhqEPTTTBMhz2hEFDM4J6V5680yNsXJGuBIbh0HljVmA0dqDsjtVHYtzivMSwxhBnTWIyF2sqTKBAHlOFmVewGCcNhKn1JW+vjwrZ6R7079CI06Jw0RopO8dmSSQ5JxEiWGcApw1iI4HWDPIm6ESx5gAeTiJAobkFKOjCNhreuRC8u1Qjjgp+y7phGmscU6ixMDmcRfcNQhHMgGKGw4XWKGHChhn6Zrw68Tr2MQJtz5Zuo8OJNrHeL29nHWF1Dc4J1FieJnQXfTy6apB2BkEyHPaaeUFjKM0dxgnfE/Th5cz/jLaBhinFcBQawVpO00AjXNiJQaALYn+GgTPwb54CBCddrZqdl5RwDieygpOc3IRjZczShq7jwljOZR86BAWuYLs8Ooa58RKDHLNrFaD4F88BCgBbG93pGIFDCweRP+5yr7/9MgjfaKc0aZiGKnuH1aM7FTRMaJhu+MfcYRXVTkn0bOVBK1PvEkpLHrA5RcPdtppIL2Ib/DXwSmenYyT44sHO+30NDhGo3AHJ2V4Uk6g5Zm3VIEedOLe1JZgq5LZ5k7OSX7xYKedmMQ3S8bP25ljOew1LSlN0/riUeW0Y8dfLS3Yi0uDXzymS25dgBnb8BePaZIKX5hmgmaEdwe4UM0Yt1bO2E21eq9m3/8fFtsu4e8xDQAAAABJRU5ErkJggg==)
"""

# Define a custom loss function
# Define Huber loss function

def huber_fn(y_true, y_pred):
    error = y_true - y_pred
    is_small_error = tf.abs(error) < 1
    squared_loss = tf.square(error) / 2
    linear_loss  = tf.abs(error) - 0.5
    return tf.where(is_small_error, squared_loss, linear_loss)

# Build the network.
# Output layer just contains 1 neuron since we have to predict only one value

model = keras.models.Sequential([
    keras.layers.Dense(30, activation="selu", kernel_initializer="lecun_normal",
                       input_shape=X_train.shape[1:]),
    keras.layers.Dense(1),
])

# Specify the loss function and the optimizer to use.
# Here we are using custom loss function
# Measure MAE during training and evaluation

model.compile(loss=huber_fn, optimizer="nadam", metrics=["mae"])

# Specify the loss function and the optimizer to use.
# Here we are using custom loss function
# Measure MAE during training and evaluation

model.compile(loss=huber_fn, optimizer="nadam", metrics=["mae"])

"""Saving/Loading Models with Custom Objects"""

# Save the model

model.save("my_model_with_a_custom_loss.h5")

# Load the model
# Specify the custom loss function while loading the model

loaded_model = keras.models.load_model("my_model_with_a_custom_loss.h5", custom_objects={"huber_fn": huber_fn})
loaded_model

model.fit(X_train_scaled, y_train, epochs=2,
          validation_data=(X_valid_scaled, y_valid))

"""When you save the model, the threshold will not be saved. This means that you will have to specify the threshold value when loading the model. You can solve this by creating a subclass of the keras.losses.Loss class, and then implementing its get_config() method"""

class HuberLoss(keras.losses.Loss):
    def __init__(self, threshold=1.0, **kwargs):
        self.threshold = threshold
        super().__init__(**kwargs)
    def call(self, y_true, y_pred):
        error = y_true - y_pred
        is_small_error = tf.abs(error) < self.threshold
        squared_loss = tf.square(error) / 2
        linear_loss  = self.threshold * tf.abs(error) - self.threshold**2 / 2
        return tf.where(is_small_error, squared_loss, linear_loss)
    def get_config(self):
        base_config = super().get_config()
        return {**base_config, "threshold": self.threshold}

input_shape = X_train.shape[1:]
model = keras.models.Sequential([
    keras.layers.Dense(30, activation="selu", kernel_initializer="lecun_normal",
                       input_shape=input_shape),
    keras.layers.Dense(1),
])

model.compile(loss=HuberLoss(2.), optimizer="nadam", metrics=["mae"])

model.fit(X_train_scaled, y_train, epochs=2,
          validation_data=(X_valid_scaled, y_valid))
