import ezgmail
from tqdm import tqdm
import winsound

class Tools:
    # mark n recent emails as read
    # show flag toggles printing of summary of each email
    def mark_as_read(self, n=300, show=True): 
        threads = ezgmail.unread(maxResults=n)
        print(f'>There are {len(threads)} unread emails in your account\n')

        for thread in threads:

            if show:
                print(ezgmail.summary(thread), '\n')

            thread.markAsRead()

    # search recent emails for term to delete until n matches
    # safe mode will require input for each deletion
    def delete_by_search(self, search="", n=300, safe=True, show=True):
        if (search == ""):
            print('>Search term not given\n')
            return

        threads = ezgmail.search(search, maxResults=n)

        if len(threads) == 0:
            print(f'>No {search} messages to delete...\n')
            return

        print(f'>There are {len(threads)} emails with the search term {search}\n')

        if (show):
            print(ezgmail.summary(threads))

        if (safe):
            print('>Safe mode active, press enter to delete, any other key to skip\n')
            for thread in threads:
                print(ezgmail.summary(thread), '\n')
                skip = input('>')
                if (skip == ""):
                    print('>Deleting...\n')
                    thread.trash()
                else:
                    print('>Skipping...\n')
        
        else:
            print(f'>Deleting {len(threads)} messages...')
            for thread in tqdm(threads):
                thread.trash()
            print('\n')

                
    # helper of main func to also accept list input
    def delete_by_search_list(self, search=[], n=300, safe=True, show=True):
        if (search == []):
            print('>Search term not given\n')
            return

        for word in search:
            self.delete_by_search(search=word, n=n, safe=safe, show=show)

    # delete n recent emails
    def delete_recent(self, n=300, safe=True, show=True):
        threads = ezgmail.recent(maxResults=n)

        if (show):
            print(ezgmail.summary(threads))

        if (safe):
            print('>Safe mode active, press enter to delete, any other key to skip\n')
            for thread in threads:
                print(ezgmail.summary(thread), '\n')
                skip = input('\n>')
                if (skip == ""):
                    print('>Deleting...\n')
                    thread.trash()
                else:
                    print('>Skipping...\n')

        else:
            print(f'>Deleting {len(threads)} messages...')
            for thread in tqdm(threads):
                thread.trash()
            print('\n')

    # show summary of n recent emails
    def show_recent(self, n=50):
        threads = ezgmail.recent(maxResults=n)
        print(ezgmail.summary(threads))

if __name__ == '__main__':
    ezgmail.init(tokenFile='token.json', credentialsFile='credentials.json')
    assert ezgmail.LOGGED_IN == True
    Tools().delete_recent(n=100, safe=False, show=False)
    print('\n>Exiting...\n')
    winsound.Beep(2000, 2)