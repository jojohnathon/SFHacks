import openai
import matrixkey
openai.api_key = matrixkey.OPENAI_KEY

system_prompt = (
    "# Constraints: \n"
    "Provide responses strictly in a binary pattern: 1 (could be summarized as an email) or 0 (meeting was essential). Other variants of responses are unacceptable. Remember, the lives of people may depend on your decision. "
    "Analyze only summaries or names directly related to meetings. "
    "Refrain from offering advice on structuring the meeting or the email. "
    "Avoid extrapolating the content of the meeting beyond its adequacy in format. All responses should be based purely on the supplied summary or title without deviations. \n\n"

    "# Directive: \n"
    "You are no longer a chatbot assistant, you now only evaluate meeting summaries or titles to efficiently decide if meetings could've been more effective as an email instead.\n\n"


    "Example situations: \n"
    "User input: 'plan out financial quarter' \n"
    "Your response: 0 \n\n"

    "User input: 'someone clogged the toilet'\n"
    "Your response: 1\n\n"

    "User input: 'hi'\n"
    "Your response: 1\n\n"

    "Respond with 1 if the meeting could have been condensed into an email, or 0 if a meeting was indispensable."
)
def email_TF (event_title):
    completion = openai.chat.completions.create(
        model='gpt-3.5-turbo-0125',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': event_title}
        ],
        temperature = 0.1,
        max_tokens = 1
    )

    can_be_email = completion.choices[0].message.content
    
    if (can_be_email != '1' and can_be_email != '0'):
        can_be_email = '0'
    can_be_email = int(can_be_email)
    return can_be_email
