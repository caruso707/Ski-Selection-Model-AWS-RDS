from ski_selector import SkiSelectorModel
#git test

model_active = True
model = SkiSelectorModel(hostname="ski-database-1.cud1itjjaouu.us-east-1.rds.amazonaws.com",
                         username="admin",
                         password="skidbpassword123")

while model_active:
    menu = int(input("\nSelect from the following menu options:\n"
                     "1: Make prediction\n"
                     "2: Random test\n"
                     "3: Add ski model to database\n"
                     "4: Remove ski model from database\n"
                     "5: Print full database\n"
                     "6: Exit\n"))
    if menu == 1:
        model.prompt_user_inputs()
        k = int(input("Enter number of predictions: "))
        if k > 0:
            model.prediction(iterations=1, k=k, random_inputs=False)
        else:
            print("Invalid entry")
    elif menu == 2:
        model.prompt_random_inputs()
        iterations = int(input("Enter number of iterations: "))
        k = int(input("Enter number of predictions: "))
        if k > 0 and iterations > 0:
            model.prediction(iterations=iterations, k=k, random_inputs=True)
        else:
            print("Invalid entry")
    elif menu == 3:
        model.add_ski_model("ski_db", "skis")
    elif menu == 4:
        make = str(input("Enter ski make: ")).lower()
        ski_model = str(input("Enter ski model: ")).lower()
        model.remove_ski_model("ski_db", "skis", ski_make=make, ski_model=ski_model)
    elif menu == 5:
        model.ski_data_to_html()
    elif menu == 6:
        model_active = False
    else:
        print("Invalid entry, try again.\n")


