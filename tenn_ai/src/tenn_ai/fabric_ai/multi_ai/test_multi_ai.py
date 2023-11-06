from tenn_ai.fabric_ai.multi_ai.tenn_multi_ai import TENN_MultiAI, TENN_MultiAI_Response

chatbot = TENN_MultiAI(passed_verbose=True)

print("------------------------------------------------------------------")
user_prompt = "What is the population of Lebanon and what is the original of the Lebanese population?"
print("User Prompt: " + user_prompt)
system_prompt = "You are a very helpful, accurate and concise assistant called TENN. Provide only a one sentence answer and nothing more."
print("System Prompt: " + system_prompt)

print("------------------------------------------------------------------")
# responses = chatbot.chat_with_all_models(passed_prompt=user_prompt, passed_system_prompt=system_prompt)
# responses = chatbot.chat(passed_model="j2-light", passed_prompt=user_prompt, passed_system_prompt=system_prompt)
responses = chatbot.chat_with_models(passed_models=["command-nightly", "j2-light", "j2-mid", "j2-ultra"], passed_prompt=user_prompt, passed_system_prompt=system_prompt)

# for choice in responses.choices:
#     print(choice.message.content)

# for model in chatbot.properties.model_map.keys():
#     chatbot.set_model(model)
#     response = chatbot.chat(passed_prompt=user_prompt, passed_system_prompt=system_prompt)
#     print("------------------------------------------------------------------")
#     print(chatbot.model_friendly_name + " response: " + response.choices[0].message.content)

# print("------------------------------------------------------------------")


# print(chatbot.get_model() + " response: " + str(response.get_all_choices_content()))

# print(response.choices[0].message.content)
