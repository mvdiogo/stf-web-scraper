import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# pip install playwright beautifulsoup4


def generate_url(base, assunto):
    base_urls = {
        "acordaos": "https://jurisprudencia.stf.jus.br/pages/search?base=acordaos&sinonimo=true&plural=true&page=1&pageSize=250&queryString={}&sort=_score&sortBy=desc",
        "decisoes": "https://jurisprudencia.stf.jus.br/pages/search?base=decisoes&pesquisa_inteiro_teor=false&sinonimo=true&plural=true&radicais=false&buscaExata=true&page=1&pageSize=10&queryString={}&sort=_score&sortBy=desc",
        "informativos": "https://jurisprudencia.stf.jus.br/pages/search?base=informativos&pesquisa_inteiro_teor=false&sinonimo=true&plural=true&radicais=false&buscaExata=true&page=1&pageSize=10&queryString={}&sort=_score&sortBy=desc",
    }
    return base_urls.get(base, "").format(assunto)


def parse_item(html_page):
    results = []
    html_page = bytes(html_page, encoding="utf-8")
    soup = BeautifulSoup(html_page, "html.parser")
    data = soup.find_all("div", class_="result-container")
    for item in data:
        title_element = item.find("h4", class_="ng-star-inserted")
        ementa_element = item.find("span", class_="jud-text ng-star-inserted")
        if title_element and ementa_element:
            title = title_element.text.strip()
            ementa = ementa_element.text.strip()
            dates = item.find_all("span", style="font-weight: normal;")
            turma = dates[0].text.strip() if len(dates) > 0 else ""
            ministro = dates[1].text.strip() if len(dates) > 1 else ""
            indexacao_partes = [
                part.text.strip() for part in item.find_all("p", class_="jud-text m-0")
            ]
            indexacao = indexacao_partes[0] if len(indexacao_partes) > 0 else ""
            partes = indexacao_partes[1] if len(indexacao_partes) > 1 else ""
            product = {
                "Title": title,
                "Ementa": ementa,
                "Orgao colegiado": turma,
                "Ministro": ministro,
                "Indexação": indexacao,
                "Partes": partes,
            }
            results.append(product)
    return results


def main(base, assunto):
    url = generate_url(base="acordaos", assunto="conselho federal de contabilidade")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        parsed = parse_item(page.content())
        print(json.dumps(parsed, indent=3, ensure_ascii=False))
        with open(f"{base} - {assunto}.json", "w", encoding="utf-8") as file:
            json.dump(parsed, file, indent=3, ensure_ascii=False)
            file.close()
        browser.close()


if __name__ == "__main__":
    base = input("Enter the base (acordaos, decisoes, or informativos): ").lower()
    assunto = input("Enter the subject: ")
    main(base, assunto)
