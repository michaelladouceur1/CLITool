import pprint

routes = {
	'costPart': {
		'type': 'router',
		'display': 'Cost Part Menu',
		'subItems': {
			'stuff': {
				'type': 'input',
				'display': 'Stuff Menu'
			},
			'cool stuff': {
				'type': 'input',
				'display': 'Cool Stuff Menu'
			}
		}
	},
	'costAssembly': {
		'type': 'router',
		'display': 'Cost Assembly Menu',
		'subItems': {
			'noStuff': {
				'type': 'input',
				'display': 'Stuff Menu'
			},
			'no cool stuff': {
				'type': 'input',
				'display': 'Cool Stuff Menu'
			}
		}
	}

}

# pp = pprint.PrettyPrinter(indent=1)
# for key, value in routes.items():
# 	print(f'{key}: {value}')

def validate():
	for value in routes.values():
		if any(value['display']):
			print(value['display'])
		else:
			print('not found')

validate()