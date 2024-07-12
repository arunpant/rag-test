import pandas as pd
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load the CSV data
data = pd.read_csv('./data/org-data-leaders.csv')
print(data)
# Initialize the OpenAI model
llm = OpenAI(api_key='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')

# Create a prompt template
template = """
You are a professional astrologer with deep knowledge in astrology and corporate leadership.

Given the sun sign {sun_sign}, provide information about the corresponding leader from the CSV data and answer the user's question.

CSV Data:
{csv_data}

Sun Sign: {sun_sign}

Additionally, the user has a question: {question}

Please provide a professional and respectful response to their question. Ensure not to answer any demeaning or inappropriate questions. Also, include a fun fact about the sun sign and note that they share their sun sign with the leader {leader_name}.
"""

prompt = PromptTemplate(
    input_variables=["sun_sign", "csv_data", "question", "leader_name"],
    template=template
)

# Define a list of keywords that signify demeaning or inappropriate questions
demeaning_keywords = ["stupid", "idiot", "dumb", "useless", "hate", "ugly", "worthless"]


# Define a function to get the matching leader and answer the question
def get_matching_leader_and_answer_question(sun_sign, question):
    # Filter the data based on the sun sign
    filtered_data = [data['SunSign'].str.lower() == sun_sign.lower()]
    print('Filtered data',filtered_data)
    if len(filtered_data)<1:
        return "No matching leader found for the provided sun sign."

    csv_data = filtered_data
    leader_name = filtered_data.iloc[0]['LeaderName']
    fun_fact = filtered_data.iloc[0]['FunFacts']

    # Check for demeaning or inappropriate questions
    if any(keyword in question.lower() for keyword in demeaning_keywords):
        return "I'm sorry, but I cannot answer demeaning or inappropriate questions. Please ask a respectful question."

    # Create an LLM chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Generate the result
    result = chain.run({
        "sun_sign": sun_sign,
        "csv_data": csv_data,
        "question": question,
        "leader_name": leader_name
    })

    # Append the fun fact and the note
    result += f"\n\nFun Fact: {fun_fact}"
    result += f"\n\nDo you know you share your sun sign with the leader {leader_name}?"

    return result


# Example usage
user_sun_sign = "Aries"
user_question = "Can you tell me more about the leadership style of an Aries?"
result = get_matching_leader_and_answer_question(user_sun_sign, user_question)
print(result)
