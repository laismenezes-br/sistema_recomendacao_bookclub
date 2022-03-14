#Importando as bibliotecas necessárias para web-scraping
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

#Função para tratamento da 'url' de cada livro
def tratamento_urls(book_url):  
    result = requests.get(book_url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return(soup)

def main():
###########################  Botões de navegação entre as páginas  ##################################################
    #Criação para uso do funcionamento da automação com Selenium
    navegador = webdriver.Chrome()
    navegador.get('https://books.toscrape.com/catalogue/category/books_1/page-1.html')

    #Loop para navegação entre as páginas
    pages = 0
    books_urls = []
    while (pages < 50):
        #Recolhe as 'urls' para acesso de cada livro
        #Imprimir todo conteúdo 'html' na aba do elemento selecionado
        page_content = navegador.page_source
        #Organização do conteúdo 'html'
        soup = BeautifulSoup(page_content, 'html.parser')
        #print(soup.prettify()[:1000])

        books = soup.findAll('div', attrs = {'class':'image_container'})
        for book in books:
            #Tratamento dos links para seus acessos posteriores
            url = book.find('a').get('href').replace('../../','')
            book_url = 'https://books.toscrape.com/catalogue/' + url
            books_urls.append(book_url)
            
            #DataFrame com os links de cada livro
            enderecos = pd.DataFrame(books_urls)  

        
        #Verificação se exitem botões 'next', caso estejam na página são clicados
        elementos = soup.findAll('li', attrs = {'class':'next'})
        for elemento in elementos:
            condicao = elemento.find('a').text
            if (condicao == 'next'):
                button = navegador.find_element(By.CSS_SELECTOR,'#default > div > div > div > div > section > div:nth-child(2) > div > ul > li.next > a')
                button.click()
                sleep(1)
            
        pages += 1
    navegador.close() #Fecha o Chrome

################  Listas para armazenamento dos dados dos livros  ##########################
    #O acesso de cada 'url' foi escolhido, porque desse modo recolhe-se todas as informações necessárias
    titles = []
    prices = []
    av = []
    categories = []
    ratings = []

    #Scraper referente a url de cada livro - parte mais demorada do programa
    for book_url in books_urls:
        soup = tratamento_urls(book_url)
        #Nome do livro
        title = soup.find('h1')
        titles.append(title.text)
        #print(titles)

        #Preço do livro - parte desnecessária do dado é retirada
        price = soup.find('p',attrs = {'class':'price_color'})
        price = price.text.replace('£','')
        prices.append(price)
        #print(prices)
        
        #Categoria do livro - parte desnecessária do dado é retirada
        listas = soup.find('ul', attrs = {'class':'breadcrumb'})
        listas = listas.findAll('a')
        categorie = listas[2].text
        categories.append(categorie)
        #print(categories)

        #Avaliação dos livros - parte desnecessária do dado é retirada
        rating = soup.find('p',attrs ={'class':'star-rating'})
        rating = rating.get('class')
        ratings.append(rating[1])
        #print(ratings)

        #Número de produtos disponíveis parte - desnecessária do dado é retirada
        nb = soup.find('p', attrs ={'class': 'instock availability'})
        nb = nb.text.replace('\n\n    \n        In stock (','').replace(' available)\n    \n','')
        av.append(nb)
        #print(av)
        
    #Criando um DataFrame para as informações dos livros
    dados = pd.DataFrame({'Títulos': titles,'Categorias':categories,'Preços(£)': prices, "Avaliações": ratings, 'Estocagem': av})
    print(dados)

    #Criando um arquivo '.csv' para ser feito o tratamento e a análise dos dados
    dados.to_csv('dados.csv', index=False)
main()


    

        


    








    




