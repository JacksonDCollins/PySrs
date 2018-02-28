import configparser
import os
confile = 'config.ini'
config = configparser.ConfigParser()
config.read(confile)

if not config.sections():
	config['GENERAL'] = {'cwd': os.getcwd(),
						 'month': 30,
						 'workdoc': os.getcwd() + '\sentences.csv',
						 'hwdoc': '\history.csv',
						 'fname': 'data',
						 'backups': os.getcwd() + '\\backups\\',
						 'newPerLesson': 5,
						 'reviewPerLesson': 25}
elif not config['GENERAL']['cwd'] == os.getcwd():
		config['GENERAL'] = {'cwd': os.getcwd(),
						 'month': config['GENERAL']['month'],
						 'workdoc': os.getcwd() + '\sentences.csv',
						 'hwdoc': config['GENERAL']['hwdoc'],
						 'fname': config['GENERAL']['fname'],
						 'backups': os.getcwd() + '\\backups\\',
						 'newPerLesson': config['GENERAL']['newPerLesson'],
						 'reviewPerLesson': config['GENERAL']['reviewPerLesson']}


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
def supportedLangs():
	return {'none' : 'None', 'af' : 'Afrikaans', 'sq' : 'Albanian', 'ar' : 'Arabic', 'hy' : 'Armenian', 'bn' : 'Bengali', 'ca' : 'Catalan', 'zh' : 'Chinese', 'zh-cn' : 'Chinese (Mandarin/China)', 'zh-tw' : 'Chinese (Mandarin/Taiwan)', 'zh-yue' : 'Chinese (Cantonese)', 'hr' : 'Croatian', 'cs' : 'Czech', 'da' : 'Danish', 'nl' : 'Dutch', 'en' : 'English', 'en-au' : 'English (Australia)', 'en-uk' : 'English (United Kingdom)', 'en-us' : 'English (United States)', 'eo' : 'Esperanto', 'fi' : 'Finnish', 'fr' : 'French', 'de' : 'German', 'el' : 'Greek', 'hi' : 'Hindi', 'hu' : 'Hungarian', 'is' : 'Icelandic', 'id' : 'Indonesian', 'it' : 'Italian', 'ja' : 'Japanese', 'km' : 'Khmer (Cambodian)', 'ko' : 'Korean', 'la' : 'Latin', 'lv' : 'Latvian', 'mk' : 'Macedonian', 'no' : 'Norwegian', 'pl' : 'Polish', 'pt' : 'Portuguese', 'ro' : 'Romanian', 'ru' : 'Russian', 'sr' : 'Serbian', 'si' : 'Sinhala', 'sk' : 'Slovak', 'es' : 'Spanish', 'es-es' : 'Spanish (Spain)', 'es-us' : 'Spanish (United States)', 'sw' : 'Swahili', 'sv' : 'Swedish', 'ta' : 'Tamil', 'th' : 'Thai', 'tr' : 'Turkish', 'uk' : 'Ukrainian', 'vi' : 'Vietnamese', 'cy' : 'Welsh'}
