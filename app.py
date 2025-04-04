import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Sprawdzanie Marek", layout="centered")
st.title("🔍 Sprawdź obecność marki w sklepach online")

# Dokładna funkcja sprawdzająca obecność marki na stronie
def check_brand_on_site(brand, site):
    query = f"site:{site} {brand}"
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            search_results = soup.select("a[href^='https://']")

            # Tylko linki z danej domeny (np. allegro.pl)
            valid_links = [link['href'] for link in search_results if site in link['href']]

            if len(valid_links) == 0:
                return "❌ Brak"
            else:
                for link in valid_links:
                    if brand.lower() in link.lower():
                        return "✅ Obecna"
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

    with st.spinner("🔄 Sprawdzam marki..."):
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

    st.success("Gotowe! ✅")
    st.write("### 📊 Wyniki wyszukiwania:")
    st.table(results)
else:
    st.info("✏️ Wprowadź marki i kliknij przycisk powyżej, aby rozpocząć.")
