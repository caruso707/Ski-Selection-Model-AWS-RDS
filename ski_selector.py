import numpy as np
import pandas as pd

from knn_modeling import KNNRegressionModel
import random
from db_connection import Database

COLUMNS = "(make, " \
          "model, " \
          "gender, " \
          "stiffness, " \
          "stability_at_speed, " \
          "carving, " \
          "turn_length, " \
          "powder, " \
          "playfulness, " \
          "park, " \
          "ability_level)"


class SkiSelectorModel:

    def __init__(self, hostname, username, password):
        self.ski_database = Database(hostname=hostname, username=username, password=password)
        self.input_parameters = ""
        self.new_data_point = np.array([])
        self.knn_model = KNNRegressionModel(pd.DataFrame())
        self.ski_data = pd.DataFrame()
        pd.set_option('display.max_colwidth', None)
        self.ski_make = []
        self.ski_model = []
        self.ski_gender = []
        self.gender = ""
        self.output = ""
        self.database_to_array("ski_db", "skis")

    def database_to_array(self, database, table):
        self.ski_database.select_database(database)
        headers = list(self.ski_database.get_columns(table))
        header_list = []
        for i in range(len(headers)):
            header_list.append(tuple(headers[i])[0])
        result = np.asarray(self.ski_database.get_table(table))
        self.ski_data = pd.DataFrame(result, columns=header_list)
        self.ski_data = self.ski_data.astype({'ID': 'int',
                                              'stiffness': 'int',
                                              'carving': 'int',
                                              'turn_length': 'int',
                                              'powder': 'int',
                                              'playfulness': 'int',
                                              'park': 'int',
                                              'stability_at_speed': 'int',
                                              'ability_level': 'int'})

    def prompt_random_inputs(self):
        """Produces random inputs for all fields for faster simulation of model."""
        if random.randint(0, 1) == 0:
            self.gender = "m"
        else:
            self.gender = "f"
        stiffness = random.randint(1, 10)
        stability = random.randint(1, 10)
        carving = random.randint(1, 10)
        turn_len = random.randint(1, 10)
        powder = random.randint(1, 10)
        playfulness = random.randint(1, 10)
        park = random.randint(1, 10)
        ability_level = random.randint(1, 10)

        self.input_parameters = (str(f"gender: {self.gender} "
                                     f"stiffness: {stiffness} "
                                     f"stability: {stability} "
                                     f"carving: {carving} "
                                     f"turn length: {turn_len} "
                                     f"powder: {powder} "
                                     f"playfulness: {playfulness} "
                                     f"park: {park} "
                                     f"ability level: {ability_level}"))

        self.new_data_point = np.array([
            stiffness,
            stability,
            carving,
            turn_len,
            powder,
            playfulness,
            park,
            ability_level
        ])

    def prompt_user_inputs(self):
        """Prompt using user prompts"""
        self.gender = str(input("Select gender ('m' or 'f'): ")).lower()
        stiffness = int(input("Select stiffness (1-10): "))
        stability = int(input("Select stability (1-10): "))
        carving = int(input("Select carving performance (1-10): "))
        turn_len = int(input("Select turn length (1-10): "))
        powder = int(input("Select powder performance (1-10): "))
        playfulness = int(input("Select playfulness (1-10): "))
        park = int(input("Select park performance (1-10): "))
        ability_level = int(input("Select ability level (1-10): "))

        self.input_parameters = (str(f"gender: {self.gender} "
                                     f"stiffness: {stiffness} "
                                     f"stability: {stability} "
                                     f"carving: {carving} "
                                     f"turn len: {turn_len} "
                                     f"powder: {powder} "
                                     f"playfulness: {playfulness} "
                                     f"park: {park} "
                                     f"ability lvl: {ability_level}"))

        self.new_data_point = np.array([
            stiffness,
            stability,
            carving,
            turn_len,
            powder,
            playfulness,
            park,
            ability_level
        ])

    def prediction(self, iterations: int, k=1, random_inputs=False):
        """Makes ski prediction.
        Use 'iterations' to specify number of iterations.
        Use 'k' to specify number of predictions per iteration.
        Use 'random_inputs' to choose between randomized inputs and user selected inputs"""
        prediction = []
        for _ in range(iterations):
            # Selects random inputs if applicable
            if random_inputs:
                self.prompt_random_inputs()
            # Filter for gender
            self.knn_model.dataset = self.ski_data.query(f'gender in ["{self.gender.upper()}", "U"]')
            # Drop all string fields
            self.knn_model.dataset = self.knn_model.dataset.drop("make", axis=1)
            self.knn_model.dataset = self.knn_model.dataset.drop("model", axis=1)
            self.knn_model.dataset = self.knn_model.dataset.drop("gender", axis=1)
            # Reset index positions
            self.knn_model.dataset.reset_index(drop=True, inplace=True)

            # Make predictions and produce results
            prediction = list(self.knn_model.get_nearest_neighbor_indices(self.new_data_point, "ID", k))
            ids = []
            for i in range(len(prediction)):
                ids.append(self.knn_model.dataset["ID"][prediction[i]])
            result = self.ski_data.query(f"ID == {ids[0]}")
            result.reset_index(drop=True, inplace=True)
            self.output = f"{result['make'][0]} {result['model'][0]}"
            for i in range(1, len(prediction)):
                result = self.ski_data.query(f"ID == {ids[i]}")
                result.reset_index(drop=True, inplace=True)
                string = f"{result['make'][0]} {result['model'][0]}"
                self.output = self.output + ", " + string
            print(self.output + " | " + self.input_parameters)
        return self.output, self.input_parameters, prediction

    def add_ski_model(self, database, table):
        """Adds ski model to database"""
        self.ski_database.select_database(database)
        make = str(input("Enter ski make: "))
        model = str(input("Enter ski model: "))
        gender = str(input("Enter ski gender ('M', 'W' or 'U'): ")).upper()
        stiffness = str(input("Enter stiffness (0-10): "))
        sas = str(input("Enter stability at speed (0-10): "))
        carve = str(input("Enter carving performance (0-10): "))
        turn_len = str(input("Enter turn length (0-10): "))
        powder = str(input("Enter powder performance (0-10): "))
        play = str(input("Enter playfulness (0-10): "))
        park = str(input("Enter park performance (0-10): "))
        ability_level = str(input("Enter ability level (0-10): "))
        row = f"('{make}','{model}','{gender}',{stiffness},{sas}," \
              f"{carve},{turn_len},{powder},{play},{park},{ability_level})"
        self.ski_database.add_row(table, COLUMNS, row)
        self.database_to_array(database, table)

    def remove_ski_model(self, database, table, ski_make, ski_model):
        """Removes ski model from database"""
        self.ski_database.select_database(database)
        condition = f"make='{ski_make}' AND model='{ski_model}'"
        self.ski_database.delete_row(table, condition)
        self.database_to_array(database, table)

    def ski_data_to_html(self):
        html = self.ski_data.to_html()
        html_file = open("ski_data.html", "w")
        html_file.write(html)
        html_file.close()
