from reflexion import run_reflexion
from intermediate_agents import DescriptionGenerationAgent, FunctionMocksAgent
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if __name__ == "__main__":
    
    cur_func_impl = """
    def train_house_price_prediction_model2(data:pd.DataFrame):
        # Split the data into training and testing sets
        X = data.drop('price', axis=1)
        y = data['price']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a linear regression model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Test the model and print the results
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = round(mse**(1/2), 2)
        r2 = r2_score(y_test, y_pred)
        output = {'RMSE': rmse, 'R2': round(r2, 2)}
        return output
    """
    # Description generation agent 
    dg_agent = DescriptionGenerationAgent(OPENAI_API_KEY=OPENAI_API_KEY)
    description_result = dg_agent.generate(cur_func_impl)
    prepared_description_result = dg_agent.create_function_with_comments(
        description_result['description'],
        description_result['method_signature'],
        description_result['programming_language'],
    )

    # Mock methods generation agent
    fm_agent = FunctionMocksAgent(OPENAI_API_KEY=OPENAI_API_KEY)
    fm_result = fm_agent.generate(cur_func_impl)


    #Preparing Dataset to call reflexion
    dataset = [{
        "cur_func_impl": fm_result +"\n" + cur_func_impl,
        "prompt":prepared_description_result
    }]

    results = run_reflexion(
        dataset = dataset,
        model = "gpt-3.5-turbo",
        language= "py",
        max_iters= 3,
        pass_at_k =1,
        log_path="root",
        verbose= True
    )

    is_solved = results[0]["is_solved"]
    unit_tests = results[0]["unit_tests"]
    reflections = results[0]["reflections"]
    solution = results[0]["solution"]

    # Parsing results 
    for key,val in results[0].items():
        print(key)
        print(val)
        print("--------------")

    