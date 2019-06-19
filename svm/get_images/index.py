from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()


def main():
    sentece = getSentece()
    qtd = getQtd()
    runImageRobot(sentece, qtd)


def getQtd():
    return int(input('Type how many images do you want: '))


def getSentece():
    return str(input('Type the search sentence: '))


def runImageRobot(searchContent, qtd):
    print('[IMAGE ROBOT] Initializing...')
    downloadImagesFromGoogle(searchContent, qtd)
    print('[IMAGE ROBOT] Shutting down...')


def downloadImagesFromGoogle(searchContent, qtd):
    arguments = {'keywords': '{}'.format(
        searchContent), 'limit': qtd, 'print_urls': True, 'image_directory': './{}'.format(searchContent)}
    response.download(arguments)


if __name__ == '__main__':
    main()
