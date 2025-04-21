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

def extract_post_id(url):
    # Utiliser une expression régulière pour extraire le numéro à la fin de l'URL
    match = re.search(r'/posts/(\d+)', url)
    if match:
        return match.group(1)
    return None

def process_mhtml_files(directory):
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

if __name__ == "__main__":
    # Spécifiez le répertoire contenant les fichiers .mhtml
    directory_path = '.'

    # Traiter tous les fichiers .mhtml dans le répertoire spécifié
    process_mhtml_files(directory_path)
