class Record():
    def __init__(self, sharer, file, description, size, official_url, direct_url, short_url, status):
        self.sharer = sharer
        self.file = file
        self.description = description
        self.size = size
        self.official_url = official_url
        self.direct_url = direct_url
        self.short_url = short_url
        self.status = status

    def to_dict(self):
        return {
            "sharer": self.sharer,
            "file": self.file,
            "description": self.description,
            "size": self.size,
            "official_url": self.official_url,
            "direct_url": self.direct_url,
            "short_url": self.short_url,
        }
