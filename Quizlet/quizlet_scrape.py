import time
from os import path
import undetected_chromedriver as uc
import re #For regex

def get_terms(URL):
    driver = uc.Chrome()
    driver.maximize_window()
    #Get pdage
    print('Getting page 1...')
    driver.get(URL)
    print('Getting page 2...')
    page = driver.execute_script("return document.body.innerHTML;")
    print('Page retrieved.')
    # print(page)

    term_list = []
    # soup = BeautifulSoup(page, 'html.parser')

    #Gets list of terms from HTML, but not text directly 
    # terms = soup.findAll('Flashcard')

    # Use regex to find the flashcard, which always begins with "hasPart\":[" and ends with "]"
    print('Finding terms...')
    flashcard_content = re.findall(r'\"hasPart\\\":\[(.*?)\]', page)
    print(len(flashcard_content))

    # Find the terms and definition pairs from the flashcard content, which always surounded by {}"
    terms = re.findall(r'\{(.*?)\}', flashcard_content[0])

    #Gets each term from the list of terms, and gets the text for each term and definition
    #Then puts it in the term list
    for i in terms:
        #Gets term
        #term is in the format of \"Question\",\"eduQuestionType\":\"Flashcard\",\"text\":
        a = re.findall(r'\\"Flashcard\\\",\\\"text\\\":\\\"(.*?)\"', i)


        #Gets definition
        # Definition is in the format of \"Flashcard\",\"text\":\"Sequence\",\"acceptedAnswer\":{\"@type\":\"Answer\",\"text\":\
        b = re.findall(r'\\\"Answer\\\",\\\"text\\\":\\\"(.*?)\"', i)

        current_term = (a, b)

        term_list.append(current_term)

    print(term_list)
    driver.quit()
    if(len(term_list) == 0):
        raise Exception('Invalid URL')

    return term_list

input_text = """
What filetype do you want to export to?
1 for .csv (Comma separated)
2 for .txt (Tab separated)
3 for .xls (Excel)
4 for .apkg (Anki package)
5 to quit
"""

#Asks for filename and returns it. Also checks if it exists
def get_filename(filetype):
    filename = input('Filename: ')
    check_file(filename + filetype)
    return filename + filetype

def get_deck_name():
    return input('Deck name: ')

#Checks if file exists, if it does not, throw exception
def check_file(filename):
    if(path.exists(filename)):
        print('File already exists')
        raise Exception("File already exists")


def main():
    url = input('Please enter a quizlet URL:\n--> ')

    #Asks for URL, makes sure it is a good URL
    try:
        term_list = get_terms(url)
    except:
        print('Not a valid Quizlet URL.')
        time.sleep(2)
        quit()

    #Repeatedly asks for selection until a valid one is given,
    #then creates a file of that selection
    while True:
        try:
            filetype = int(input(input_text))
            if (filetype < 1 or filetype > 5):
                raise Exception('Invalid selection')
            elif (filetype == 1):
                name = get_filename('.csv')
                term_list.csv(name)
                break
            elif (filetype == 2):
                name = get_filename('.txt')
                term_list.txt(name)
                break
            elif (filetype == 3):
                name = get_filename('.xls')
                term_list.xls(name)
                break
            elif (filetype == 4):
                deck_name = get_deck_name()
                name = get_filename('.apkg')
                term_list.anki(deck_name, name)
                break
            elif (filetype == 5):
                break
        except:
            print('Invalid input.')

if __name__ == "__main__":
    main()