from time import localtime, strftime

urlBlog = '/var/www/index.html'
urlArchive = '/var/www/archives.html'
intHistoryLength_Blog = 10
intHistoryLength_Board = 20

def msgBoard(req, strName, strMessage):
    if not (strName and strMessage):
        return "A required parameter is missing!"

    # Removes \n from strMessage and replaces them by spaces
    strMessage = strMessage.replace('\n', ' ')
    
    # Reads the current blog file
    file = open(urlBlog, 'r')
    lstBlog = file.readlines()
    file.close()

    # Inserts the new comment
    for i in range(len(lstBlog)):
        if '<!--board-01-->' in lstBlog[i]:
            lstBlog.insert(i, '<!--board-01-->\n')
            lstBlog.insert(i+1, '<div class="board"><div class="board-name">' + strName + '</div><div class="board-message">' + strMessage + '</div></div>\n')
            break

    # Increment the history
    booIncrement = False
    for item in range(intHistoryLength_Board):
        for i in range(len(lstBlog)):
            if ('<!--board-%(index)02d-->' % {'index': item+1} in lstBlog[i]):
                if booIncrement:
                    lstBlog.pop(i)
                    lstBlog.insert(i, '<!--board-%(index)02d-->\n' % {'index': item+2})
                    booIncrement = False
                    break
                else: booIncrement = True

    # Purges the history
    booPurgeHistory = False
    lstPurges = []
    lstArchives = []
    for i in range(len(lstBlog)):
        if ('<!--board-%(index)02d-->' % {'index': intHistoryLength_Board+1} in lstBlog[i]):
            if booPurgeHistory:
                lstPurges.append(i)
                break
            else:
                booPurgeHistory = True
        elif booPurgeHistory:
            lstPurges.append(i)
    for i in lstPurges:
        lstArchives.append(lstBlog.pop(lstPurges[0]))

    # Archives the purged messages
    # Reads the archive file
    file = open(urlArchive, 'r')
    lstArchiveFile = file.readlines()
    file.close()
    # Inserts the new comment
    for i in range(len(lstArchiveFile)):
        if '<!--board-->' in lstArchiveFile[i]:
            for j in range(len(lstArchives)-1):
                lstArchiveFile.insert(i+j+1, lstArchives[j])
            break
    # Updates the archive
    file = open(urlArchive, 'w')
    file.writelines(lstArchiveFile)
    file.close()

    # Updates the blog
    file = open(urlBlog, 'w')
    file.writelines(lstBlog)
    file.close()

    return "<html>\n<a href='http://huitcent.homeip.net:8080/index.html'>Retour</a>\n</html>"

def newMessage(req, strMessage):
    if not strMessage:
        return "A required parameter is missing!"

    # Removes \n from strMessage and replaces them by spaces
    strMessage = strMessage.replace('\n', ' ')

    # Reads the current blog file
    file = open(urlBlog, 'r')
    lstBlog = file.readlines()
    file.close()

    # Inserts the new comment
    for i in range(len(lstBlog)):
        if '<!--blog-01-->' in lstBlog[i]:
            lstBlog.insert(i, '<!--blog-01-->\n')
            lstBlog.insert(i+1, '<div class="blog"><div class="blog-name">[' + strftime("%d %b %Y %H:%M", localtime()) + '] - <a class="white" href="mailto:lavoie.michel@gmail.com">Mike</a></div><div class="blog-message">' + strMessage + '</div></div>\n')
            break

    # Increment the history
    booIncrement = False
    for item in range(intHistoryLength_Blog):
        for i in range(len(lstBlog)):
            if ('<!--blog-%(index)02d-->' % {'index': item+1} in lstBlog[i]):
                if booIncrement:
                    lstBlog.pop(i)
                    lstBlog.insert(i, '<!--blog-%(index)02d-->\n' % {'index': item+2})
                    booIncrement = False
                    break
                else: booIncrement = True

    # Purges the history
    booPurgeHistory = False
    lstPurges = []
    lstArchives = []
    for i in range(len(lstBlog)):
        if ('<!--blog-%(index)02d-->' % {'index': intHistoryLength_Blog+1} in lstBlog[i]):
            if booPurgeHistory:
                lstPurges.append(i)
                break
            else:
                booPurgeHistory = True
        elif booPurgeHistory:
            lstPurges.append(i)
    for i in lstPurges:
        lstArchives.append(lstBlog.pop(lstPurges[0]))

    # Archives the purged messages
    # Reads the archive file
    file = open(urlArchive, 'r')
    lstArchiveFile = file.readlines()
    file.close()
    # Inserts the new comment
    for i in range(len(lstArchiveFile)):
        if '<!--blog-->' in lstArchiveFile[i]:
            for j in range(len(lstArchives)-1):
                lstArchiveFile.insert(i+j+1, lstArchives[j])
            break
    # Updates the archive
    file = open(urlArchive, 'w')
    file.writelines(lstArchiveFile)
    file.close()

    # Updates the blog
    file = open(urlBlog, 'w')
    file.writelines(lstBlog)
    file.close()

    return "<html>\n<a href='http://huitcent.homeip.net:8080/index.html'>Retour</a>\n</html>"
