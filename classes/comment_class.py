class Comment_Class():

    """

    |---------------------------------------------------------------------
    |                                                                    |
    |     Comment Class                                                  |
    |                                                                    |
    |---------------------------------------------------------------------
    |                                                                    |
    |   1 - initial Class with account_name ,text ,author and likes      |
    |                                                                    |
    |   2 - return class object property as list                         |
    |                                                                    |
    ----------------------------------------------------------------------

    """

    # ? -> 1
    def __init__(self, account_name, text, author, likes):
        self.account_name = account_name
        self.text = text
        self.author = author
        self.likes = likes


    # ? -> 2
    def return_prop_as_list(self):
        prop_list = []
        prop_list.append(self.account_name)
        prop_list.append(self.text)
        prop_list.append(self.author)
        prop_list.append(self.likes)
        return prop_list