
#GCML
##HTML for emailing newsletters

###Use example:
	python main.py -i index.gcml -c true

* -i --input, the GCML file you want to run
* -c --clean, if you want to clean up the HTML file after

###List of tags and their options:

	<gc-body [bgcolor]></code>
	<gc-container [bgcolor] [width]>
	<gc-table [bgcolor] [width] [height] [align]>
	<gc-btn [fontcolor] [bgcolor] [width] [height] [radius] [fontsize]>
	<gc-spacer [height] [bgcolor]>
	<gc-mirror [fontcolor]>
	<gc-unsub [fontcolor]>
	<gc-menu [items] [fontcolor] [bgcolor] [fontsize]>
	<gc-ctl-btn [width] [btn-clr] [input-clr] [height] [label]>

### Contributions
Author: Gamliel COHEN

if you want to add a new tag, it is very simple.
You need to edit the main.py file, in the Gcml class,
there is a dictionnary where all the tags, their HTML file,
and their options are defined. You just have to add a new entry like that:

	'<gc-tag>': {
		'pattern': r'<gc-tag[^>]*>',
		'file': 'lib/gc-tag.html',
		'options': ['bgcolor="[^"]*"', 'size="[^"]*"']
	},

then, you need to create the HTML file with the variables
options in order to replace theim, your HTML file is gonna be some thing like that:

	<tr>
		<td align="center">
			<tag [[bgcolor]] [[size]]>This tag and his options is gonna be replace</tag>
		</td>
	</tr>
