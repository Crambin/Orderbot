# logging
error_log_channel_id = 702517343141756980

# development
bot_developer_ids = (212241077695021056,)  # Crambor
ignored_extensions = ("music",)

# misc
default_prefix = '!'

# music
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

# language codes for translation
lang_settings = {'-s': 'auto', '-d': 'en'}
lang_codes = {'el': 'Greek', 'eo': 'Esperanto', 'en': 'English', 'af': 'Afrikaans', 'sw': 'Swahili',
              'ca': 'Catalan',
              'it': 'Italian', 'iw': 'Hebrew', 'sv': 'Swedish', 'cs': 'Czech', 'cy': 'Welsh', 'ar': 'Arabic',
              'ga': 'Irish', 'eu': 'Basque', 'et': 'Estonian', 'id': 'Indonesian', 'es': 'Spanish', 'ur': 'Urdu',
              'ru': 'Russian', 'gl': 'Galician', 'nl': 'Dutch', 'pt': 'Portuguese', 'vi': 'Vietnamese',
              'az': 'Azerbaijani',
              'la': 'Latin', 'tr': 'Turkish', 'tl': 'Filipino', 'lv': 'Latvian', 'lt': 'Lithuanian', 'th': 'Thai',
              'gu': 'Gujarati', 'ro': 'Romanian', 'is': 'Icelandic', 'pl': 'Polish', 'ta': 'Tamil',
              'ht': 'Haitian Creole',
              'yi': 'Yiddish', 'be': 'Belarusian', 'fr': 'French', 'bg': 'Bulgarian', 'uk': 'Ukrainian',
              'hr': 'Croatian',
              'bn': 'Bengali', 'sl': 'Slovenian', 'da': 'Danish', 'fa': 'Persian', 'mk': 'Macedonian',
              'zh-TW': 'Chinese Traditional',
              'hi': 'Hindi', 'fi': 'Finnish', 'hu': 'Hungarian', 'ja': 'Japanese', 'ka': 'Georgian',
              'zh-CN': 'Chinese Simplified',
              'sq': 'Albanian', 'no': 'Norwegian', 'ko': 'Korean', 'kn': 'Kannada', 'te': 'Telugu',
              'sk': 'Slovak', 'mt': 'Maltese', 'de': 'German', 'ms': 'Malay', 'sr': 'Serbian'}
