class Record:
    def __init__(self, sharer, file, description, size, share_url, direct_url, short_url, status):
        self.sharer = sharer
        self.file = file
        self.description = description
        self.size = size
        self.share_url = share_url
        self.direct_url = direct_url
        self.short_url = short_url
        self.status = status

    def to_dict(self):
        return {
            "sharer": self.sharer,
            "file": self.file,
            "description": self.description,
            "size": self.size,
            "share_url": self.share_url,
            "direct_url": self.direct_url,
            "short_url": self.short_url,
        }
