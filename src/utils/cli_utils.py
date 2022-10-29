from PyInquirer import prompt, Separator


def checkbox_select(message, choices, validate=None):
    choices_list = []
    for key, values in choices.items():
        choices_list.append(Separator("= " + key + " ="))
        
        for i, choice in enumerate(values['options']):
            checked = False
            if 'checked' in values:
                if type(values['checked']) == 'list':
                    checked = values['checked'][i]
                else:
                    checked = values['checked']

            choices_list.append(
                {
                    'name': choice,
                    'checked': checked
                }
            )

    questions = [
        {
            'type': 'checkbox',
            'name': 'checkbox',
            'message': message,
            'choices': choices_list,
            'validate': lambda answer: validate(answer) \
                if validate else True
        }
    ]

    ans = prompt(questions)

    selected_options = { key:[] for key, _ in choices.items()}
    for opt in ans['checkbox']:
        for key, values in choices.items():
            if opt in values['options']:
                selected_options[key].append(opt)

    return selected_options


def list_select(message, choices):
    questions = [
        {
            'type': 'list',
            'name': 'list',
            'message': message,
            'choices': choices,
        }
    ]

    ans = prompt(questions)
    return choices.index(ans['list'])

def ask_input(message):
    questions = [
        {
            'type': 'input',
            'name': 'input',
            'message': message,
        }
    ]
    ans = prompt(questions)
    return ans['input']