class Critter:
    def __init__(self, discord_id):
        self.discord_id = discord_id
        self.category_id = None
        self.voice_id = None
        self.text_id = None
        self.private_text_id = None

    # discord id - int
    def get_discord_id(self):
        return self.discord_id
    
    def set_discord_id(self, a):
        self.discord_id = a
        
    def del_discord_id(self):
        self.discord_id = None

    # category id - int
    def get_category_id(self):
        return self.category_id

    def set_category_id(self, a):
        self.category_id = a

    def del_category_id(self):
        self.category_id = None

    # voice channel id - int
    def get_voice_id(self):
        return self.voice_id

    def set_voice_id(self, a):
        self.voice_id = a

    def del_voice_id(self):
        self.voice_id = None

    # text channel - int
    def get_text_id(self):
        return self.text_id

    def set_text_id(self, a):
        self.text_id = a

    def del_text_id(self):
        self.text_id = None

    # private text channel - int
    def get_private_text_id(self):
        return self.private_text_id

    def set_private_text_id(self, a):
        self.private_text_id = a

    def del_private_text_id(self):
        self.private_text_id = None
