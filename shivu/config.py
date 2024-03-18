class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "2064735436"
    SUDOERS = "6295947116, 2064735436"
    GROUP_ID = -1001440080728
    TOKEN = "7198935197:AAGjehZVUgx2DzPquirZPlEs31kPUsn7Pfs"
    mongo_url = "mongodb+srv://gotouhitoriii:7vzXrCihdSZfTtEs@haremgod.rxndc2y.mongodb.net/?retryWrites=true&w=majority"
    PHOTO_URL = ["https://raw.githubusercontent.com/theredactedentity/databasepics/main/photo_url1.jpg", "https://raw.githubusercontent.com/theredactedentity/databasepics/main/photo_url2.jpg", "https://raw.githubusercontent.com/theredactedentity/databasepics/main/photo_url3.jpg", "https://raw.githubusercontent.com/theredactedentity/databasepics/main/photo_url4.jpg", "https://raw.githubusercontent.com/theredactedentity/databasepics/main/photo_url5.jpg", "https://raw.githubusercontent.com/theredactedentity/databasepics/main/photo_url6.jpg", "https://raw.githubusercontent.com/theredactedentity/databasepics/main/photo_url7.jpg", "https://raw.githubusercontent.com/theredactedentity/databasepics/main/photo_url8.jpg", "https://raw.githubusercontent.com/theredactedentity/databasepics/main/photo_url9.jpg", "https://raw.githubusercontent.com/theredactedentity/databasepics/main/photo_url10.png", "https://raw.githubusercontent.com/theredactedentity/databasepics/main/photo_url11.png"]
    SUPPORT_CHAT = "GlobalAnimeCommunityOfficial"
    UPDATE_CHAT = "BotsByChad"
    BOT_USERNAME = "HaremGodBot"
    CHARA_CHANNEL_ID = "-1001782672183"
    api_id = 21927988
    api_hash = "e18f720acdff1e5b0ec80616aecd8a5a"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
