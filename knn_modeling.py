import numpy as np


class KNNRegressionModel:

    def __init__(self, dataset):
        self.dataset = dataset

    def get_correlation(self, header):
        correlation_matrix = self.dataset.corr()
        return correlation_matrix[header]

    def drop_column(self, column, axis=1):
        self.dataset = self.dataset.drop(column, axis=axis)

    def drop_row(self, row_index, axis=0):
        self.dataset = self.dataset.drop(row_index, axis=axis)

    def add_headers(self, header_list):
        self.dataset.columns = header_list

    def predict(self, new_data_point, dependent_variable, k, axis=1):
        ind_var = self.dataset.drop(dependent_variable, axis=axis)
        ind_var = ind_var.values
        dep_var = self.dataset[dependent_variable]
        dep_var = dep_var.values
        distances = np.linalg.norm(ind_var - new_data_point, axis=axis)
        nearest_neighbor_ids = distances.argsort()[:k]
        nearest_neighbor_values = dep_var[nearest_neighbor_ids]
        prediction = nearest_neighbor_values.mean()
        return prediction

    def get_nearest_neighbor_indices(self, new_data_point, dependent_variable, k, axis=1):
        ind_var = self.dataset.drop(dependent_variable, axis=axis)
        ind_var = ind_var.values
        distances = np.linalg.norm(ind_var - new_data_point, axis=axis)
        nearest_neighbor_ids = distances.argsort()[:k]
        return nearest_neighbor_ids

    def get_nearest_neighbor_values(self, new_data_point, dependent_variable, k, axis=1):
        ind_var = self.dataset.drop(dependent_variable, axis=axis)
        ind_var = ind_var.values
        dep_var = self.dataset[dependent_variable]
        dep_var = dep_var.values
        distances = np.linalg.norm(ind_var - new_data_point, axis=axis)
        nearest_neighbor_ids = distances.argsort()[:k]
        nearest_neighbor_values = dep_var[nearest_neighbor_ids]
        return nearest_neighbor_values
