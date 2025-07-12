from experiment import start_main_span


agent_questions = [
    "What was the most popular product SKU?",
    "What was the total revenue across all stores?",
    "Which store had the highest sales volume?",
    "Create a bar chart showing total sales by store",
    "What percentage of items were sold on promotion?",
    "What was the average transaction value?"
]

def testing_agent():

    for quest in agent_questions:
        try:
            ret = start_main_span([{'role': 'user', 'content': quest}])
        except Exception as ex:
            print(f'Error processing question: {ex} ')
            print(ex)
            continue
