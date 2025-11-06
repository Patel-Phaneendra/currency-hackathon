from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

API_KEY = 'demo'  # Replace with your Alpha Vantage API key

HTML_FORM = '''
    <h2>Currency Converter</h2>
    <form method="POST">
      Amount: <input type="text" name="amount" required><br><br>
      From Currency (e.g., USD): <input type="text" name="from_currency" maxlength="3" required><br><br>
      To Currency (e.g., INR): <input type="text" name="to_currency" maxlength="3" required><br><br>
      <input type="submit" value="Convert">
    </form>
    {% if result %}
      <h3>Conversion Result:</h3>
      <p>{{ amount }} {{ from_currency }} = {{ result }} {{ to_currency }}</p>
    {% elif error %}
      <p style="color: red;">Error: {{ error }}</p>
    {% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def convert_currency():
    if request.method == 'POST':
        amount = request.form.get('amount')
        from_currency = request.form.get('from_currency').upper()
        to_currency = request.form.get('to_currency').upper()

        # Validate numeric amount
        try:
            amount = float(amount)
        except ValueError:
            return render_template_string(HTML_FORM, error="Please enter a valid numeric amount.")

        # Call Alpha Vantage API for exchange rate
        url = (f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE'
               f'&from_currency={from_currency}&to_currency={to_currency}&apikey={API_KEY}')

        try:
            response = requests.get(url)
            data = response.json()
            rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
            converted_amount = round(rate * amount, 4)
            return render_template_string(HTML_FORM, result=converted_amount, amount=amount,
                                          from_currency=from_currency, to_currency=to_currency)
        except Exception:
            return render_template_string(HTML_FORM, error="Failed to get exchange rate. Please check the currencies or try later.")

    return render_template_string(HTML_FORM)

if __name__ == '__main__':
    app.run(debug=True)

