from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
#pip install playwright selectolax 

#assunto = 'cassação registro profissional conselho federal de medicina'

def generate_url(base, assunto):
    base_urls = {
        'acordaos': 'https://jurisprudencia.stf.jus.br/pages/search?base=acordaos&sinonimo=true&plural=true&page=1&pageSize=250&queryString={}&sort=_score&sortBy=desc',
        'decisoes': 'https://jurisprudencia.stf.jus.br/pages/search?base=decisoes&pesquisa_inteiro_teor=false&sinonimo=true&plural=true&radicais=false&buscaExata=true&page=1&pageSize=10&queryString={}&sort=_score&sortBy=desc',
        'informativos': 'https://jurisprudencia.stf.jus.br/pages/search?base=informativos&pesquisa_inteiro_teor=false&sinonimo=true&plural=true&radicais=false&buscaExata=true&page=1&pageSize=10&queryString={}&sort=_score&sortBy=desc'
    }
    return base_urls.get(base, '').format(assunto)

def parse_item(html_page):
    results = []
    html = HTMLParser(html_page)
    data = html.css("div.result-container")
    for item in data:
        product = {
            "Title": item.css_first("h4.ng-star-inserted").text(),
            "Ementa": item.css_first("p.jud-text.m-0").text(),
            "Decisão": item.css("p.jud-text.m-0")[1].text() if len(item.css("p.jud-text")) > 1 else "",
            "Indexação": item.css("p.jud-text.m-0")[2].text() if len(item.css("p.jud-text")) > 2 else "",
            "Partes": item.css("p.jud-text.m-0")[3].text() if len(item.css("p.jud-text")) > 3 else ""
        }
        results.append(product)
    return results

def main(base, assunto):
    url = generate_url(base, assunto)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        #next_page = page.locator("a._ngcontent-ekl-c137")
        while True:
            print(parse_item(page.content()))
            #if next_page.is_disabled():
            break
            #page.click("a._ngcontent-ekl-c137")
            page.wait_for_load_state("networkidle")
            break

if __name__ == "__main__":
    base = input("Enter the base (acordaos, decisoes, or informativos): ").lower()
    assunto = input("Enter the subject: ")
    main(base, assunto)