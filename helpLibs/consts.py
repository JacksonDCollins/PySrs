import configparser
import os
import ctypes.wintypes

for i in range(1):
	CSIDL_PERSONAL = 5      # My Documents
	SHGFP_TYPE_CURRENT = 0   # Get current, not default value

	buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
	ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

workloc = buf.value + '\PySrs'
confile = workloc + '\config.ini'
config = configparser.ConfigParser()
config.read(confile)


if not config.sections():
	config['GENERAL'] = {'cwd': workloc,#os.getcwd(),
						 'month': 30,
						 'workdoc': workloc + '\sentences.csv', #os.getcwd() + '\sentences.csv',
						 'hwdoc': '\history.csv',
						 'fname': 'data',
						 'images':'pics',
						 'backups': workloc + '\\backups\\',#os.getcwd() + '\\backups\\',
						 'newPerLesson': 5,
						 'reviewPerLesson': 25,
						 'defaultLang': 'None'}
elif not config['GENERAL']['cwd'] == workloc:#os.getcwd():
		config['GENERAL'] = {'cwd': workloc,#os.getcwd(),
						 'month': config['GENERAL']['month'],
						 'workdoc': workloc + '\sentences.csv', #os.getcwd() + '\sentences.csv',
						 'hwdoc': config['GENERAL']['hwdoc'],
						 'fname': config['GENERAL']['fname'],
						 'images':config['GENERAL']['images'],
						 'backups': workloc + '\\backups\\',#os.getcwd() + '\\backups\\',
						 'newPerLesson': config['GENERAL']['newPerLesson'],
						 'reviewPerLesson': config['GENERAL']['reviewPerLesson'],
						 'defaultLang': config['GENERAL']['defaultLang']}

with open(confile, 'w') as c:
	config.write(c)

def cwd():
	config.read(confile)
	return config['GENERAL']['cwd']
def month():
	config.read(confile)
	return int(config['GENERAL']['month'])
def workdoc():
	config.read(confile)
	return config['GENERAL']['workdoc']
def hwdoc():
	config.read(confile)
	return config['GENERAL']['hwdoc']
def fname():
	config.read(confile)
	return config['GENERAL']['fname']
def backups():
	config.read(confile)
	return config['GENERAL']['backups']
def newPerLesson():
	config.read(confile)
	return int(config['GENERAL']['newPerLesson'])
def reviewPerLesson():
	config.read(confile)
	return int(config['GENERAL']['reviewPerLesson'])
def defaultLang():
	config.read(confile)
	return config['GENERAL']['defaultLang']
def images():
	config.read(confile)
	return config['GENERAL']['images']
def supportedLangs():
	return {'none' : 'None', 'af' : 'Afrikaans', 'sq' : 'Albanian', 'ar' : 'Arabic', 'hy' : 'Armenian', 'bn' : 'Bengali', 'ca' : 'Catalan', 'zh' : 'Chinese', 'zh-cn' : 'Chinese (Mandarin/China)', 'zh-tw' : 'Chinese (Mandarin/Taiwan)', 'zh-yue' : 'Chinese (Cantonese)', 'hr' : 'Croatian', 'cs' : 'Czech', 'da' : 'Danish', 'nl' : 'Dutch', 'en' : 'English', 'en-au' : 'English (Australia)', 'en-uk' : 'English (United Kingdom)', 'en-us' : 'English (United States)', 'eo' : 'Esperanto', 'fi' : 'Finnish', 'fr' : 'French', 'de' : 'German', 'el' : 'Greek', 'hi' : 'Hindi', 'hu' : 'Hungarian', 'is' : 'Icelandic', 'id' : 'Indonesian', 'it' : 'Italian', 'ja' : 'Japanese', 'km' : 'Khmer (Cambodian)', 'ko' : 'Korean', 'la' : 'Latin', 'lv' : 'Latvian', 'mk' : 'Macedonian', 'no' : 'Norwegian', 'pl' : 'Polish', 'pt' : 'Portuguese', 'ro' : 'Romanian', 'ru' : 'Russian', 'sr' : 'Serbian', 'si' : 'Sinhala', 'sk' : 'Slovak', 'es' : 'Spanish', 'es-es' : 'Spanish (Spain)', 'es-us' : 'Spanish (United States)', 'sw' : 'Swahili', 'sv' : 'Swedish', 'ta' : 'Tamil', 'th' : 'Thai', 'tr' : 'Turkish', 'uk' : 'Ukrainian', 'vi' : 'Vietnamese', 'cy' : 'Welsh'}
