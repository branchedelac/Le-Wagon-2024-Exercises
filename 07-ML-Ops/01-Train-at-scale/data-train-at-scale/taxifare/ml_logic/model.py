import numpy as np
import time

from colorama import Fore, Style
from typing import Tuple

# Timing the TF import
print(Fore.BLUE + "\nLoading TensorFlow..." + Style.RESET_ALL)
start = time.perf_counter()

from tensorflow import keras
from keras import Model, Sequential, layers, regularizers, optimizers
from keras.callbacks import EarlyStopping

end = time.perf_counter()
print(f"\n✅ TensorFlow loaded ({round(end - start, 2)}s)")


def initialize_model(input_shape: tuple) -> Model:
    """
    Initialize the Neural Network with random weights
    """
    reg = regularizers.l1_l2(l1=0.005)

    model = Sequential()
    model.add(layers.Input(shape=input_shape))
    model.add(layers.Dense(100, activation="relu", kernel_regularizer=reg))
    model.add(layers.BatchNormalization(momentum=0.9))
    model.add(layers.Dropout(rate=0.1))
    model.add(layers.Dense(50, activation="relu"))
    model.add(
        layers.BatchNormalization(momentum=0.9)
    )  # use momentum=0 to only use statistic of the last seen minibatch in inference mode ("short memory"). Use 1 to average statistics of all seen batch during training histories.
    model.add(layers.Dropout(rate=0.1))
    model.add(layers.Dense(1, activation="linear"))

    print("✅ model initialized")

    return model


def compile_model(model: Model, learning_rate=0.0005) -> Model:
    """
    Compile the Neural Network
    """
    learning_rate = 0.0005

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(loss="mean_squared_error", optimizer=optimizer, metrics=["mae"])

    return model


def train_model(
    model: Model,
    X: np.ndarray,
    y: np.ndarray,
    batch_size=256,
    patience=2,
    validation_data=None,  # overrides validation_split
    validation_split=0.3,
) -> Tuple[Model, dict]:
    """
    Fit the model and return a tuple (fitted_model, history)
    """
    es = EarlyStopping(
        monitor="val_loss", patience=patience, restore_best_weights=True, verbose=0
    )

    history = model.fit(
        X,
        y,
        validation_split=validation_split,
        validation_data=validation_data,
        epochs=100,
        batch_size=batch_size,
        callbacks=[es],
        verbose=1,
    )

    print(
        f"✅ Model trained on {len(X)} rows with min val MAE: {round(np.min(history.history['val_mae']), 2)}"
    )

    return model, history
