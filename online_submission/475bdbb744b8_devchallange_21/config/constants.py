#DB_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres' # rin as unicorn web server 
DB_URL = 'postgresql+asyncpg://postgres:postgres@db:5432/postgres' # run in docker-compose

EMOTIONAL_TONES = ["Neutral", "Positive", "Negative", "Angry"]

ANGRY_KEYWORDS = [
    "angry", "furious", "hate", "rage", "irritated", "annoyed",
    "frustrated", "upset", "mad", "disgusted", "hostile",
    "seething", "fuming", "boiling", "livid", "miffed", "peeved",
    "steamed", "vexed", "bitter", "resentful", "spiteful",
    "vengeful", "hostile", "antagonistic", "belligerent", "combative",
    "confrontational"
]

UKRAINIAN_CITIES = [
    "Kyiv", "Kiev", "Kharkiv", "Lviv", "Odessa", "Dnipro", "Zaporizhzhia", "Mykolaiv",
    "Vinnytsia", "Donetsk", "Luhansk", "Krivyi Rih", "Mariupol", "Zhytomyr",
    "Chernivtsi", "Khmelnytskyi", "Poltava", "Chernihiv", "Sumy", "Kirovohrad",
    "Ivano-Frankivsk", "Uzhhorod", "Lutsk", "Rivne", "Ternopil", "Kropyvnytskyi",
    "Kamianets-Podilskyi", "Kremenchuk", "Bakhmut", "Kramatorsk", "Selydove",
    "Sloviansk", "Druzhkivka", "Horlivka", "Sievierodonetsk", "Lysychansk",
    "Volnovakha", "Enerhodar", "Berdiansk", "Melitopol", "Nova Kakhovka",
    "Skadovsk"
]

COUNTRY = "Ukraine"

POSITIVE_THRESHOLD = 0.15
NEGATIVE_THRESHOLD = -0.1

DEFAULT_CATEGORIES = ["Visa and Passport Services", "Diplomatic Inquiries", "Travel Advisories", "Consular Assistance",
                      "Trade and Economic Cooperation"]

MSG_FAILED_DOWNLOAD = "Failed to download audio file"
MSG_UNEXPECTED_ERROR = "An unexpected error"
MSG_CALL_NOT_FOUND = "Call not found"
MSG_URL_REQUIRED = "Audio URL is required"
MSG_CATEGORY_NOT_FOUND = "Category not found"
MSG_CATEGORY_DELETED = "Category deleted successfully"
MSG_DB_NOT_CONFIGURED = "Database is not configured correctly"
MSG_DB_CONNECT_ERROR = "Error connecting to the database"
MSG_WELCOME = "Welcome to Calls Processing API"
MSG_CATEGORY_TITLE_REQUIRED = "Category title is required"
