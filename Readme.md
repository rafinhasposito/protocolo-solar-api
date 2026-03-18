# Swiss Ephemeris API and WordPress Plugin

This project consists of two main components:

1. A Python-based REST API for the Swiss Ephemeris library
2. A WordPress plugin that utilizes this API to provide astrological calculations

# Swiss Ephemeris API

This is a simple Python API endpoint for the Swiss Ephemeris library. It is a REST API that provides planetary positions for a given date and time.

## Installation Using Docker

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mohammad-ammad/swiss-Ephemeris-api.git
   ```

2. **Build the Docker image:**

   ```bash
   sudo docker build -t pyswisseph-api .
   ```

3. **Run the Docker container:**

   ```bash
   sudo docker run -p 5000:5000 pyswisseph-api
   ```

## Installation Without Docker

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mohammad-ammad/swiss-Ephemeris-api.git
   ```

2. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API:**

   ```bash
   python app.py
   ```

## Testing the API

Now you have an API running on `http://localhost:5000`. You can send POST requests to `/calculate_chart` with JSON data to get astrological calculations.

### Using CURL

```bash
curl -X POST http://localhost:5000/calculate_chart \
 -H "Content-Type: application/json" \
 -d '{
  "name": "John Doe",
  "place_of_birth": "New York, USA",
  "dob": "18/06/1998",
  "time": "14:30"
}'
```

### Using Postman

1.  Open Postman and create a new request.

2.  Set the request type to POST.

3.  Set the request URL to http://localhost:5000/calculate_chart.

4.  Set the request body to JSON and enter the following data:

```json
{
  "name": "John Doe",
  "place_of_birth": "New York, USA",
  "dob": "18/06/1998",
  "time": "14:30" // optional
}
```

5. Click the Send button to make the request.

6. You should see the response from the API with the astrological calculations.

# Astrology Sign Calculator WordPress Plugin

This WordPress plugin provides an astrology sign calculator form that can be easily embedded into your posts or pages using a shortcode. It uses the Swiss Ephemeris API to calculate astrological signs based on user input.

## Installation

1. Download the plugin files and place them in a new directory named `astrology-calculator` in your WordPress plugins directory (`wp-content/plugins/`).

2. Activate the plugin through the 'Plugins' menu in WordPress.

3. Use the shortcode `[astrology_calculator]` in any post or page where you want the calculator form to appear.

## Configuration

Before using the plugin, you need to set the correct API URL for the Swiss Ephemeris API:

1. Open the file `wp-content/plugins/astrology-calculator/dist/index.js` in a text editor.

2. Locate the line that sets the `API_URL` constant:

   ```javascript
   const API_URL = "YOUR_API_URL";
   ```

3. Replace the URL with the correct URL of your Swiss Ephemeris API. For example
   
      ```javascript
      const API_URL = "https://your-api-domain.com";
      ```

4. Save the file.

## Usage
Once installed and configured, you can use the shortcode `[astrology_calculator]` in any post or page to display the astrology calculator form.
The form allows users to input their name, place of birth, date of birth, and time of birth. When submitted, it will contact the Swiss Ephemeris API and display the calculated astrological signs.
