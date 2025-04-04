import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Sprawdzanie Marek", layout="centered")
st.title("🔍 Sprawdź obecność marki w sklepach online")

def check_brand_on_site(brand, site):
    query = f"site:{site} {brand}"
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            search_results = soup.select("a")
            if len(search_results) > 0:
                return "✅ Obecna"
            else:
                return "❌ Brak"
        else:
            return "⚠️ Błąd zapytania"
    except Exception as e:
        return f"❌ Błąd: {e}"

brand_input = st.text_area("Wprowadź marki do sprawdzenia (jedna na linię):")

if st.button("Sprawdź marki") and brand_input:
    brands = [line.strip() for line in brand_input.split("\n") if line.strip()]
    results = []

    with st.spinner("Sprawdzam marki..."):
        for brand in brands:
            allegro_status = check_brand_on_site(brand, "allegro.pl")
            tim_status = check_brand_on_site(brand, "tim.pl")
            conrad_status = check_brand_on_site(brand, "conrad.pl")

            results.append({
                "Marka": brand,
                "Allegro": allegro_status,
                "TIM": tim_status,
                "Conrad": conrad_status
            })

    st.success("Gotowe!")
    st.write("### Wyniki")
    st.table(results)
else:
    st.info("Wprowadź marki i kliknij przycisk powyżej, aby rozpocząć.")
