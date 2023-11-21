from flask import Flask, render_template, request
import csv
import openai

app = Flask(__name__)

# Set  OpenAI GPT-3 API key
openai.api_key = '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'

# Function to read prompts from CSV file
def read_prompts_from_csv(Oreo_test):
    prompts = []
    with open(Oreo_test, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in list(csv_reader)[1:26]:
            prompt = row[3]  
            prompts.append(prompt)
    return prompts

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Getting user input for business-related information
        business_info = request.form['business_info']

        # Reading prompts from the CSV file
        csv_filename = 'Oreo_test.csv'  # Adjust the filename if needed
        prompts = read_prompts_from_csv(csv_filename)

        # Generating and run prompts for each line
        chatgpt_responses = []
        for prompt in prompts:
            # Generate a prompt for ChatGPT
            chatgpt_prompt = f"[Our Business] Information: {business_info}\n"
            chatgpt_prompt += f"\nUser: {prompt}\nAssistant: "

            # Run ChatGPT to get responses
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=chatgpt_prompt,
                max_tokens=150
            )

            # Append the response to the list
            chatgpt_responses.append(response.choices[0].text.strip())

        # Zip the prompts and responses together
        zipped_data = zip(prompts, chatgpt_responses)

        return render_template('result.html', business_info=business_info, zipped_data=zipped_data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
