from flask import Flask, render_template, jsonify, request
import csv

app = Flask(__name__)

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to search post offices based on District, Post Office Name, and/or Pincode
@app.route('/search_post_office', methods=['GET'])
def search_post_office():
    district_query = request.args.get('district', '').lower()
    office_name_query = request.args.get('office_name', '').lower()
    pincode_query = request.args.get('pincode', '').lower()
    post_offices = []

    try:
        # Open and read the CSV file
        with open('MAP1.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)

            # Debugging: Print CSV headers to confirm they're correct
            headers = csv_reader.fieldnames


            # Iterate through the CSV and filter based on the search query
            for row in csv_reader:
                office_name = row['OfficeName'].strip().lower()
                pincode = row['Pincode'].strip().lower()
                district = row['District'].strip().lower()
                latitude = row['Latitude'].strip()
                longitude = row['Longitude'].strip()

                # Debugging: Print row to see if data is read correctly


                # Filter based on district, office name, and pincode
                if (district_query in district) and (office_name_query in office_name) and (pincode_query in pincode):
                    post_offices.append({
                        'office_name': row['OfficeName'],
                        'pincode': row['Pincode'],
                        'district': row['District'],
                        'latitude': row['Latitude'],
                        'longitude': row['Longitude']
                    })

    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return jsonify({"error": "Error reading CSV file"}), 500

    return jsonify(post_offices)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
