import os
import subprocess
import re

def download_patreon_video(post_id, output_dir):
    URL = f"https://www.patreon.com/posts/{post_id}"
    resolution_id = "bv+ba/b"

    # Specify output directory and filename
    output_path = os.path.join(output_dir, "%(title)s.%(ext)s")

    download_command = ["yt-dlp", "--cookies", "cookies.txt", URL, "-f", resolution_id, "-o", output_path]
    print(download_command)
    subprocess.run(download_command)

def extract_post_links_from_content(html_content):
    # Utiliser une expression régulière pour trouver tous les liens commençant par "https://www.patreon.com/posts/"
    pattern = r'https://www.patreon.com/posts/\d+'
    post_links = re.findall(pattern, html_content)
    return post_links

def extract_tagged_post_links_from_content(html_content):
    # Utiliser une expression régulière pour trouver tous les liens commençant par "https://www.patreon.com/posts/"
    pattern = r'filters%5Btag%5D=[a-zA-Z%\d+-]+'
    post_links = re.findall(pattern, html_content)
    return post_links

def extract_post_id(url):
    # Utiliser une expression régulière pour extraire le numéro à la fin de l'URL
    match = re.search(r'/posts/(\d+)', url)
    if match:
        return match.group(1)
    return None

# Ecrit la fonction extract_tagged_post_id qui recevra un post_link issue de extract_tagged_post_links_from_content
# extract_tagged_post_id devras extraire la chaine de caratères qui suit le symbole =
def extract_tagged_post_id(post_link):
    match = re.search(r'filters%5Btag%5D=([a-zA-Z%\d+-]+)', post_link)
    if match:
        return match.group(1)
    return None


def process_mhtml_files_in_dir(directory):
    # Parcourir tous les fichiers dans le répertoire donné
    for filename in os.listdir(directory):
        if filename.endswith('.mhtml'):
            # Extraire le nom du dossier à partir du nom de fichier
            folder_name = filename.split('_')[0].strip()

            # Créer un dossier pour chaque fichier
            output_dir = os.path.join(directory, folder_name)
            os.makedirs(output_dir, exist_ok=True)

            # Chemin complet du fichier
            file_path = os.path.join(directory, filename)

            # Lire le contenu du fichier
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Extraire et afficher les liens des posts
            print(f"Processing file: {filename}")
            post_links = extract_post_links_from_content(html_content)
            for link in post_links:
                post_id = extract_post_id(link)
                if post_id:
                    download_patreon_video(post_id, output_dir)

def process_collection_file():

    filename ="collections_list.html"
    with open(filename, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Extraire et afficher les liens des posts
    print(f"Processing file: {filename}")
    # TODO revoir la fonction extract_tagged_post_links_from_content pour avoir l'url complète.
    post_links = extract_tagged_post_links_from_content(html_content)
    print(f"nb of links: {len(post_links)}")
    for link in post_links:
        post_id = extract_tagged_post_id(link)
        if post_id:            
            # Créer un dossier ayant pour nom le post_id en remplaçant les + et les %3A par des espace sans toutdefois obtenir 2 espaces concecutif et les %26, %27, %28 et %29 par leur caractère respectif
            folder_name = post_id.replace('+', ' ').replace('%3A', ' ').replace('%26', '&').replace('%27', "'").replace('%28', '(').replace('%29', ')')
            folder_name = re.sub(r'\s+', ' ', folder_name).strip()
            print(f"Creating folder: {folder_name}")
            output_dir = os.path.join('.', folder_name)
            os.makedirs(output_dir, exist_ok=True)
            # TODO recuperer la page html de chaque post_id. Soit la sauvegarder soit re essayer de la parcourir ave beautifulsoup afin de récupérer les liens de vidéos.
            # exemple : le lien suivant https://www.patreon.com/c/school_of_arms/posts?filters%5Btag%5D=2HS+Second+Assault
            # contiens les liens :
            #   https://www.patreon.com/posts/two-handed-sword-118812910
            #   https://www.patreon.com/posts/two-handed-sword-100608876

            

if __name__ == "__main__":
    # Spécifiez le répertoire contenant les fichiers .mhtml
    directory_path = '.'


    process_collection_file()

    # Traiter tous les fichiers .mhtml de collection dans le répertoire spécifié
#    process_mhtml_files_in_dir(directory_path)
