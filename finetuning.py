import openai, os, json, csv

openai.api_key = os.getenv("OPENAI_API_KEY")

# Read JSON data
with open('response.json', 'r') as json_file:
    data = json.load(json_file)

# Write to CSV
with open('data.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Write the header (if needed)
    csv_writer.writerow(data[0].keys())

    # Write the data
    for item in data:
        csv_writer.writerow(item.values())


# Initialize the output data list
output_data = []

# Read the CSV file and process the data
with open('input.csv', 'r', newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        useremail = row['useremail']
        prompt = row['prompt']
        results = row['results']

        # Create a dictionary for the transformed data
        transformed_data = {
            "system": "AI assistant",
            "user": prompt,
            "assisted": results
        }

        # Append the transformed data dictionary to the output_data list
        output_data.append(transformed_data)

with open('chatfinetune.json1', 'w') as json_file:
    json.dump(output_data, json_file, indent=4)

print("JSON transformation complete")

# Print the list of dictionaries
for data in output_data:
    print(data)

#uploading the data

response = openai.File.create(
    file=open("chatfinetune.json1", "rb"), 
    purpose='fine-tune'
)