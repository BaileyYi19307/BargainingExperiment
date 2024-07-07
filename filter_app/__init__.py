from otree.api import *

doc = """
Survey
"""


class Constants(BaseConstants):
    name_in_url = 'filter_app'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label="1. What is your age?",
                              min=12,max=60)
    country = models.StringField(label="2. In which country were you born?",
                                choices=['Other','Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa',
                                         'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda',
                                         'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan',
                                         'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize',
                                         'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of',
                                         'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana',
                                         'Bouvet Island', 'Brazil', 'British Indian Ocean Territory',
                                         'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia',
                                         'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands',
                                         'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island',
                                         'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo',
                                         'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica',
                                         "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic',
                                         'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt',
                                         'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia',
                                         'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France',
                                         'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon',
                                         'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland',
                                         'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea',
                                         'Guinea-Bissau', 'Guyana', 'Haiti',
                                         'Heard Island and McDonald Islands', 'Holy See (Vatican City State)',
                                         'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia',
                                         'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel',
                                         'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya',
                                         'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of',
                                         'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia',
                                         'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania',
                                         'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi',
                                         'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
                                         'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
                                         'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco',
                                         'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar',
                                         'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand',
                                         'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island',
                                         'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau',
                                         'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay',
                                         'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico',
                                         'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda',
                                         'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha',
                                         'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)',
                                         'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa',
                                         'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia',
                                         'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)',
                                         'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa',
                                         'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan',
                                         'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden',
                                         'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China',
                                         'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste',
                                         'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey',
                                         'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine',
                                         'United Arab Emirates', 'United Kingdom', 'United States',
                                         'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu',
                                         'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British',
                                         'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']
                                )
    education = models.StringField(label="3. What is your highest education level?",
                                   choices=["Did not complete high school", "Completed high school",
                                            "Completed college degree", "Master’s degree", "PhD"]
                                   )
    gender = models.StringField(label="4. What is your gender?",
                                choices= ["Female", "Male", "Other", "Do not wish to respond"],
                                widget=widgets.RadioSelect,
                                )
    icon = models.StringField(label="4a. Choose an icon to represent you", choices=[
        ("female_icon1.png", "Image 1"),
        ("female_icon2.png", "Image 2"),
        ("male_icon1.png", "Image 3"),
        ("male_icon2.png", "Image 4")
    ])

# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'country', 'education', 'gender', 'icon']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        icons = [
            ("female_icon1.png", "Image 1"),
            ("female_icon2.png", "Image 2"),
            ("male_icon1.png", "Image 3"),
            ("male_icon2.png", "Image 4")
        ]
        return {'icons': icons}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['selected_icon'] = player.icon




page_sequence = [Survey]
