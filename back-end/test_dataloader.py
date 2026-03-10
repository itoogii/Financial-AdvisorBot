import app.services.dataloader as dataloader
import numpy as np

history_df = dataloader.data_collector("AAPL")
def test_load_data():
    assert not history_df.empty, "Data collection failed: DataFrame is empty."

def test_preprocess_data():
    processed_numpy = dataloader.data_preprocessing(history_df)
    assert processed_numpy is not None, "Data preprocessing failed: Result is None."
    assert not processed_numpy.size == 0, "Data preprocessing failed: numpy is empty."
    assert not np.isnan(processed_numpy).any(), "Data preprocessing failed: numpy contains NaN values."
    print("Processed numpy shape:", processed_numpy.shape)
    assert processed_numpy.shape == (1, 60, 5), "Data preprocessing failed: numpy has incorrect shape."
