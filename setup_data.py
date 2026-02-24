import urllib.request
import os

def download_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    os.makedirs("backend", exist_ok=True)
    destination = os.path.join("backend", "titanic.csv")
    print(f"Downloading dataset to {destination}...")
    try:
        urllib.request.urlretrieve(url, destination)
        print("Download complete!")
    except Exception as e:
        print(f"Failed to download dataset: {e}")

if __name__ == "__main__":
    download_data()
