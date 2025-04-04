import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Sprawdzanie Marek – TIM", layout="centered")
st.title("🔍 Sprawdź obecność marki na TIM.pl")

# Funkcja do sprawdzania obecności marki na TIM.pl
def check_brand_on_tim(brand):
    url = f"https://www.tim.pl/szukaj?q={brand}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            product_tiles = soup.select("div.catalog-tile")
            if len(product_tiles) > 0:
                return "✅ Obecna"
            else:
                return "❌ Brak"
        else:
            return "⚠️ Błąd zapytania"
    except Exception as e:
        return f"❌ Błąd: {e}"

# Interfejs użytkownika
brand_input = st.text_area("Wprowadź marki do sprawdzenia (jedna na linię):")

if st.button("Sprawdź marki") and brand_input:
    brands = [line.strip() for line in brand_input.split("\n") if line.strip()]
    results = []

    with st.spinner("🔄 Sprawdzam marki na TIM.pl..."):
        for brand in brands:
            tim_status = check_brand_on_tim(brand)

            results.append({
                "Marka": brand,
                "TIM.pl": tim_status
            })

    st.success("Gotowe! ✅")
    st.write("### 📊 Wyniki wyszukiwania:")
    st.table(results)
else:
    st.info("✏️ Wprowadź marki i kliknij przycisk powyżej, aby rozpocząć.")
