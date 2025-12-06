import json
from flask import Flask, request, jsonify
from pyfinn import fetch_ad, scrape_ad

app = Flask(__name__)

@app.route("/", methods=["GET"])
def ad_detail():
    finnkode = request.args.get("finnkode")
    
    # Sjekk om finnkode mangler
    if not finnkode or not finnkode.isdigit():
        return jsonify({"error": "Missing or invalid param finnkode. Try /?finnkode=KODE"}), 400

    try:
        # 1. Bygg URL
        url = f"https://www.finn.no/realestate/homes/ad.html?finnkode={finnkode}"
        
        # 2. Hent HTML fra Finn
        html = fetch_ad(url)
        
        # 3. Skrap data fra HTMLen
        ad_data = scrape_ad(html)
        
        # 4. Legg til URL i resultatet for referanse
        if isinstance(ad_data, dict):
            ad_data['url'] = url
            
        # 5. Returner data som JSON
        return jsonify(ad_data)

    except Exception as e:
        # Hvis noe går galt (f.eks. Finn endrer kode), gi beskjed
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
