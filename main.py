#! /usr/bin/python
# coding: utf8

import re
from optparse import OptionParser
from sys import exit
from requests import post
from ast import literal_eval

class Gcml:
	aGcmlTags = {
		# body
		'<gc-body>': {
			'pattern': r'<gc-body[^>]*>',
			'file': 'lib/gc-body.html',
			'options': ['bgcolor="[^"]*"']
		},
		'</gc-body>': {
			'pattern': r'</gc-body>',
			'file': 'lib/gc-body.end.html',
			'options': False
		},

		# container
		'<gc-container>': {
			'pattern': r'<gc-container[^>]*>',
			'file': 'lib/gc-container.html',
			'options': ['width="[^"]*"', 'bgcolor="[^"]*"', 'height="[^"]*"', 'align="[^"]*"']
		},
		'</gc-container>': {
			'pattern': r'</gc-container>',
			'file': 'lib/gc-container.end.html',
			'options': False
		},

		# btn
		'<gc-btn>': {
			'pattern': r'<gc-btn[^>]*>',
			'file': 'lib/gc-btn.html',
			'options': ['fontcolor="[^"]*"', 'bgcolor="[^"]*"', 'width="[^"]*"', 'height="[^"]*"', 'radius="[^"]*"', 'size="[^"]*"', 'label="[^"]*"']
		},

		# spacer
		'<gc-spacer>': {
			'pattern': r'<gc-spacer[^>]*>',
			'file': 'lib/gc-spacer.html',
			'options': ['height="[^"]*"', 'bgcolor="[^"]*"']
		},

		# mirror url
		'<gc-mirror>': {
			'pattern': r'<gc-mirror[^>]*>',
			'file': 'lib/gc-mirror.html',
			'options': ['fontcolor="[^"]*"']
		},

		# unsub url
		'<gc-unsub>': {
			'pattern': r'<gc-unsub[^>]*>',
			'file': 'lib/gc-unsub.html',
			'options': ['fontcolor="[^"]*"']
		},

		# menu resp
		'<gc-menu>': {
			'pattern': r'<gc-menu[^>]*>',
			'file': 'lib/gc-menu.html',
			'options': ['fontcolor="[^"]*"', 'size="[^"]*"', 'bgcolor="[^"]*"', 'items="[^"]*"']
		}
	}

	"""from Gcml to html emailing"""
	def __init__(self, file, clean):
		self.file = open(file, 'r+')
		self.nameFile = file.split('.')[0]
		self.parseGcml()

		if clean != False:
			self.clean()

	########################################################################
	# parse the GCML with HTML
	########################################################################
	def parseGcml(self):
		gcml = self.file.read()
		newFile = open(self.nameFile + '.html', 'w+')
		
		for tag in self.aGcmlTags.iteritems():
			tagGcml = tag[0]
			pattern = tag[1]['pattern']
			pathFileHtml = tag[1]['file']
			aOptions = tag[1]['options']

			fileHtml = open(pathFileHtml, 'r').read()

			matches = re.findall(pattern, gcml)

			# if the tag is optinable
			if aOptions:
				# all the tag found
				for match in matches:
					# all the options
					tagsToReplace={}
					for option in aOptions:
						optionToReplace = '[['+option.split('=')[0]+']]'
						opt = re.search(option, match)

						# if the tag has the option
						if opt:
							rpl = ' '+opt.group(0)+' '
							# if the key exist in the object
							if match in tagsToReplace.keys():
								tagsToReplace[match]['options'][optionToReplace] = rpl
							else:
								tagsToReplace[match] = {
									'file': pathFileHtml,
									'options': {
										optionToReplace: rpl
									}
								}

						# option not found
						else:
							if match in tagsToReplace.keys():
								tagsToReplace[match]['options'][optionToReplace] = ' '
							else:
								tagsToReplace[match] = {
									'file': pathFileHtml,
									'options': {
										optionToReplace: ' '
									}
								}
					
					# now that we have the match, file, options and value
					# we can replace all of them in once
					# print tagsToReplace; exit(0)
					for tagToReplace in tagsToReplace.iteritems():
						match = tagToReplace[0]
						options = tagToReplace[1]['options']
						file = tagToReplace[1]['file']

						newContentHtml = open(file, 'r').read()
						for o in options.iteritems():
							opt = o[0]
							val = o[1]

							# if the option is a radius
							if opt == '[[radius]]' and val != '':
								radiusVal = re.search('radius="([0-9]*)"', val)
								# pattern found
								if radiusVal:
									radiusTable = '-moz-border-radius: {0}px; border-radius: {0}px;border-collapse: initial;'.format(radiusVal.group(1))
									radiusClass = ' class="bradius" '
									radiusColor = re.search('bgcolor="#([^"]*)"', match)
									radiusTd = '-webkit-border-radius: {0}px; -moz-border-radius: {0}px; border-radius: {0}px;border-collapse: initial; border:1px solid #{1};'.format(radiusVal.group(1), radiusColor.group(1))

									# replace
									newContentHtml = newContentHtml.replace('[[radiusTable]]', radiusTable)
									newContentHtml = newContentHtml.replace('[[radiusClass]]', radiusClass)
									newContentHtml = newContentHtml.replace('[[radiusTd]]', radiusTd)
								# radius value not found
								else:
									print 'ERROR: radius option enabled but value not found'
									exit(3)
							# if the option is a label
							elif opt == '[[label]]' and val != '':
								labelValue = re.search('label="([^"]*)"', val)
								# label value found
								if labelValue:
									opt = '[[labelValue]]'
									val = labelValue.group(1)
								# label value not found
								else:
									print 'ERROR: label option enabled but without value'
									exit(3)
							# if the option is a height
							elif opt == '[[height]]' and val != '':
								heightValue = re.search('height="([^"]*)"', val)
								# height value found
								if heightValue:
										newContentHtml = newContentHtml.replace('[[heightValue]]', heightValue.group(1))
								# height value not found
								else:
									print 'WARNING: No value for height option (chelou)'
							# if the option is color
							elif opt == '[[fontcolor]]' and val != '':
								colorValue = re.search('fontcolor="([^"]*)"', val)
								# if the color value were found
								if colorValue:
									newContentHtml = newContentHtml.replace('[[colorValue]]', colorValue.group(1))
								# color value not found
								else:
									print 'ERROR: color option enabled but no value found.'
									exit(3)
							# if the option is items
							elif opt == '[[items]]' and val != '':
								aItems = re.search('items="([^"]*)"', val).group(1).split(',')
								# if menu values found
								if aItems:
									itemCode = re.search('\[\[item:([^(&&)]*):enditem\]\]', newContentHtml).group(1)
									colorValue = re.search('fontcolor="([^"]*)"', match).group(1)
									bgColorValue = re.search('bgcolor="([^"]*)"', match).group(1)
									fontSize = re.search('size="([^"]*)"', match).group(1)
									beginItemsCode = newContentHtml.split('[[item:')[0]
									endItemsCode = newContentHtml.split(':enditem]]')[1]
									htmlFinal = beginItemsCode
									for item in aItems:
										htmlFinal = htmlFinal + itemCode.replace('[[colorValue]]', colorValue).replace('[[bgcolor]]', bgColorValue).replace('[[sizeValue]]', fontSize).replace('[[itemN]]', item)
									htmlFinal = htmlFinal + endItemsCode
									newContentHtml = htmlFinal

								# value of menu not found
								else:
									print 'ERROR: values of menu items not found'
									exit(3)

							print 'tag: ' + match
							print 'option: ' + opt
							print 'val: '+val+'\n'

							# set align="center" by default
							if opt == '[[align]]' and val == ' ':
								val = ' align="center" '

							newContentHtml = newContentHtml.replace(opt, val)
						gcml = gcml.replace(match, newContentHtml)
			# if the tag is not optionable
			else:
				for match in matches:
					gcml = gcml.replace(match, fileHtml)
		# write the new html content in the new file
		newFile.write(gcml)

	########################################################################
	# Clean the html with DIRTY MARKUP API
	########################################################################
	def clean(self):
		htmlFile = open(self.nameFile + '.html', 'r+').read()
		data = {
			'code': htmlFile,
			'indent': 4,
			'allow-proprietary-attribs': True
		}
		res = post('https://dirtymarkup.com/api/html', data=data)
		newHtml = literal_eval(res.text)['clean']

		print 'DIRTY MARKUP: clean'
		open(self.nameFile + '.html', 'w').write(newHtml)


# options du script
parser = OptionParser(usage='%prog -i -c index.gcml')
parser.add_option('-i', '--input', action='store', default='index.gcml')
parser.add_option('-c', '--clean', action='store', default=False)
options, args = parser.parse_args()

html = Gcml(options.input, options.clean)
