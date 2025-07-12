CLARITY_LLM_JUDGE_PROMPT = """
In this task, you will be presented with a query and an answer. Your objective is to evaluate the clarity 
of the answer in addressing the query. A clear response is one that is precise, coherent, and directly 
addresses the query without introducing unnecessary complexity or ambiguity. An unclear response is one 
that is vague, disorganized, or difficult to understand, even if it may be factually correct.

Your response should be a single word: either "clear" or "unclear," and it should not include any other 
text or characters. "clear" indicates that the answer is well-structured, easy to understand, and 
appropriately addresses the query. "unclear" indicates that the answer is ambiguous, poorly organized, or 
not effectively communicated. Please carefully consider the query and answer before determining your 
response.

After analyzing the query and the answer, you must write a detailed explanation of your reasoning to 
justify why you chose either "clear" or "unclear." Avoid stating the final label at the beginning of your 
explanation. Your reasoning should include specific points about how the answer does or does not meet the 
criteria for clarity.

[BEGIN DATA]
Query: {query}
Answer: {response}
[END DATA]
Please analyze the data carefully and provide an explanation followed by your response.

EXPLANATION: Provide your reasoning step by step, evaluating the clarity of the answer based on the query.
LABEL: "clear" or "unclear"
"""

ENTITY_CORRECTNESS_LLM_JUDGE_PROMPT = """
In this task, you will be presented with a query and an answer. Your objective is to determine whether all 
the entities mentioned in the answer are correctly identified and accurately match those in the query. An 
entity refers to any specific person, place, organization, date, or other proper noun. Your evaluation 
should focus on whether the entities in the answer are correctly named and appropriately associated with 
the context in the query.

Your response should be a single word: either "correct" or "incorrect," and it should not include any 
other text or characters. "correct" indicates that all entities mentioned in the answer match those in the 
query and are properly identified. "incorrect" indicates that the answer contains errors or mismatches in 
the entities referenced compared to the query.

After analyzing the query and the answer, you must write a detailed explanation of your reasoning to 
justify why you chose either "correct" or "incorrect." Avoid stating the final label at the beginning of 
your explanation. Your reasoning should include specific points about how the entities in the answer do or 
do not match the entities in the query.

[BEGIN DATA]
Query: {query}
Answer: {response}
[END DATA]
Please analyze the data carefully and provide an explanation followed by your response.

EXPLANATION: Provide your reasoning step by step, evaluating whether the entities in the answer are 
correct and consistent with the query.
LABEL: "correct" or "incorrect"
"""

