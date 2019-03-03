import enchant
import sys
import os
import time

class SpellCheckerMedical:
	def __init__(self, word_list_path, no_suggestions=5):
		self.no_suggestions = no_suggestions
		self.word_list_path = word_list_path
		self.medical_dict = enchant.PyPWL(self.word_list_path)

	def check(self, word):
		word_exists = self.medical_dict.check(word)
		suggestions = []
		if not word_exists:
			suggestions = self.medical_dict.suggest(word)

		return suggestions[:self.no_suggestions]

if __name__ == '__main__':
	start = time.time()
	spellchecker = SpellCheckerMedical('wordlist.txt')
	print('Initialized: {} sec'.format(time.time() - start))
	start = time.time()
	print(spellchecker.check('abdomen'))
	print('Done: {} sec'.format(time.time() - start))
