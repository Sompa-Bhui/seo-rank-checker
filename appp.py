from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def get_rank(driver, keyword, domain):
    try:
        search = driver.find_element(By.NAME, "q")
        search.clear()
        search.send_keys(keyword)
        search.send_keys(Keys.RETURN)

        print("👉 CAPTCHA solve karo + scroll karo")
        input("👉 READY ho jao phir ENTER dabao...")

        current_position = 0

        for page in range(5):  # top 50
            time.sleep(5)

            results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")

            if not results:
                print("⚠️ Results load nahi hue, retrying...")
                time.sleep(3)
                continue

            for result in results:
                try:
                    link = result.find_element(By.TAG_NAME, "a")
                    href = link.get_attribute("href")

                    current_position += 1

                    if href and domain in href:
                        return current_position

                except:
                    continue

            try:
                next_btn = driver.find_element(By.ID, "pnnext")
                next_btn.click()
            except:
                break

        return "Above 50"

    except Exception as e:
        print("❌ ERROR:", e)
        return "API Failed"


@app.route("/api/rank")
def rank_api():
    keyword = request.args.get("keyword")
    domain = request.args.get("domain")
    location = request.args.get("location")  # NEW 🔥

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        # 🌍 LOCATION MAP
        if location.lower() == "india":
            url = "https://www.google.com/?hl=en&gl=in"
        elif location.lower() == "usa":
            url = "https://www.google.com/?hl=en&gl=us"
        elif location.lower() == "canada":
            url = "https://www.google.com/?hl=en&gl=ca"
        else:
            return jsonify({
                "error": "Invalid location (choose India, USA, Canada)"
            })

        driver.get(url)
        time.sleep(2)

        rank = get_rank(driver, keyword, domain)

    except Exception as e:
        print("❌ DRIVER ERROR:", e)
        rank = "API Failed"

    driver.quit()

    return jsonify({
        "keyword": keyword,
        "domain": domain,
        "location": location,
        "rank": rank
    })


if __name__ == "__main__":
    app.run(debug=True)
