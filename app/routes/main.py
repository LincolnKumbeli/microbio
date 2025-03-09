from flask import Blueprint, render_template, request, redirect, url_for, flash

main_bp = Blueprint('main', __name__)

# Confirmatory tests data
CONFIRMATORY_TESTS_DATA = {
    'e_coli': [
        {
            'name': 'IMViC (Indole, Methyl Red, Voges-Proskauer, Citrate Utilization) Tests',
            'tests': [
                {'test': 'Indole Test', 'result': 'Positive (red ring)', 'explanation': 'Indicates tryptophanase production'},
                {'test': 'Methyl Red', 'result': 'Positive (red color)', 'explanation': 'Shows mixed acid fermentation'},
                {'test': 'Voges-Proskauer', 'result': 'Negative', 'explanation': 'No acetoin production'},
                {'test': 'Citrate Utilization', 'result': 'Negative', 'explanation': 'Cannot use citrate as sole carbon source'}
            ]
        },
        {
            'name': 'Triple Sugar Iron Agar (TSIA)',
            'tests': [
                {'test': 'Slant/Butt', 'result': 'A/A (Yellow/Yellow)', 'explanation': 'A/A: Acid/Acid - Ferments both glucose and lactose/sucrose, yellow slant and yellow butt'},
                {'test': 'Gas Production', 'result': 'Positive (bubbles/cracks)', 'explanation': 'Produces gas from glucose fermentation'},
                {'test': 'H₂S Production', 'result': 'Negative', 'explanation': 'No black precipitate formation'}
            ]
        },
        {
            'name': 'Sugar Fermentation',
            'tests': [
                {'test': 'Lactose', 'result': 'Positive (acid & gas)', 'explanation': 'Ferments lactose rapidly'},
                {'test': 'Glucose', 'result': 'Positive (acid & gas)', 'explanation': 'Ferments glucose rapidly'}
            ]
        }
    ],
    's_aureus': [
        {
            'name': 'Enzyme Tests',
            'tests': [
                {'test': 'Coagulase Test', 'result': 'Positive (clot formation)', 'explanation': 'Distinguishes S. aureus from other Staphylococci'},
                {'test': 'Catalase Test', 'result': 'Positive (bubble formation)', 'explanation': 'Differentiates from Streptococci'},
                {'test': 'DNase Test', 'result': 'Positive (clear zone)', 'explanation': 'Confirms S. aureus identification'}
            ]
        },
        {
            'name': 'Biochemical Tests',
            'tests': [
                {'test': 'Mannitol Fermentation', 'result': 'Positive (yellow color)', 'explanation': 'Ferments mannitol under aerobic and anaerobic conditions'},
                {'test': 'Novobiocin Susceptibility', 'result': 'Sensitive', 'explanation': 'Distinguishes from S. saprophyticus'}
            ]
        }
    ],
    'p_aeruginosa': [
        {
            'name': 'Biochemical Tests',
            'tests': [
                {'test': 'Oxidase Test', 'result': 'Positive (purple color)', 'explanation': 'Indicates cytochrome oxidase production'},
                {'test': 'Catalase Test', 'result': 'Positive (bubble formation)', 'explanation': 'Shows catalase production'},
                {'test': 'Growth at 42°C', 'result': 'Positive', 'explanation': 'Distinguishes from other Pseudomonas species'}
            ]
        },
        {
            'name': 'Triple Sugar Iron Agar (TSIA)',
            'tests': [
                {'test': 'Slant/Butt', 'result': 'K/K (Red/Red)', 'explanation': 'K/K: Alkaline/Alkaline - Non-fermenter, uses peptones instead of sugars'},
                {'test': 'Gas Production', 'result': 'Negative', 'explanation': 'No gas production'},
                {'test': 'H₂S Production', 'result': 'Negative', 'explanation': 'No black precipitate formation'}
            ]
        },
        {
            'name': 'Additional Tests',
            'tests': [
                {'test': 'Fluorescence under UV', 'result': 'Positive (yellow-green)', 'explanation': 'Shows pyoverdin production'},
                {'test': 'Arginine Dihydrolase', 'result': 'Positive', 'explanation': 'Confirms P. aeruginosa identification'}
            ]
        }
    ],
    'k_pneumoniae': [
        {
            'name': 'IMViC (Indole, Methyl Red, Voges-Proskauer, Citrate Utilization) Tests',
            'tests': [
                {'test': 'Indole Test', 'result': 'Negative', 'explanation': 'No tryptophanase production'},
                {'test': 'Methyl Red', 'result': 'Negative', 'explanation': 'No mixed acid fermentation'},
                {'test': 'Voges-Proskauer', 'result': 'Positive (red color)', 'explanation': 'Produces acetoin'},
                {'test': 'Citrate Utilization', 'result': 'Positive (blue color)', 'explanation': 'Can use citrate as sole carbon source'}
            ]
        },
        {
            'name': 'Triple Sugar Iron Agar (TSIA)',
            'tests': [
                {'test': 'Slant/Butt', 'result': 'A/A (Yellow/Yellow)', 'explanation': 'A/A: Acid/Acid - Ferments both glucose and lactose/sucrose, yellow slant and yellow butt'},
                {'test': 'Gas Production', 'result': 'Positive (bubbles/cracks)', 'explanation': 'Produces abundant gas from fermentation'},
                {'test': 'H₂S Production', 'result': 'Negative', 'explanation': 'No black precipitate formation'}
            ]
        },
        {
            'name': 'Additional Tests',
            'tests': [
                {'test': 'Urease Test', 'result': 'Positive (pink color)', 'explanation': 'Shows urease production'},
                {'test': 'String Test', 'result': 'Positive (>5mm string)', 'explanation': 'Indicates hypermucoviscosity'},
                {'test': 'Capsule Stain', 'result': 'Positive (clear halo)', 'explanation': 'Shows capsule production'}
            ]
        }
    ],
    's_pneumoniae': {
        'identification_tests': [
            {
                'name': 'Optochin Susceptibility Test',
                'expected_result': 'Sensitive (≥14 mm zone of inhibition)',
                'explanation': 'S. pneumoniae is characteristically sensitive to optochin (ethylhydrocupreine), distinguishing it from other alpha-hemolytic streptococci'
            },
            {
                'name': 'Bile Solubility Test',
                'expected_result': 'Positive (colony lysis)',
                'explanation': 'S. pneumoniae colonies dissolve in the presence of bile salts (sodium deoxycholate), a unique characteristic among streptococci'
            },
            {
                'name': 'Catalase Test',
                'expected_result': 'Negative',
                'explanation': 'S. pneumoniae does not produce catalase enzyme, helping differentiate it from staphylococci'
            },
            {
                'name': 'Gram Stain',
                'expected_result': 'Gram-positive diplococci with characteristic lancet shape',
                'explanation': 'Microscopic examination reveals pairs of oval cocci with pointed ends (lancet-shaped)'
            }
        ],
        'antimicrobial_tests': [
            {
                'name': 'Penicillin Susceptibility',
                'method': 'Oxacillin disk (1 µg) screening',
                'interpretation': 'Zone size ≥20 mm indicates susceptibility to penicillin for non-meningeal isolates'
            }
        ]
    },
    'n_gonorrhoeae': [
        {
            'name': 'Primary Identification Tests',
            'tests': [
                {
                    'test': 'Gram Stain',
                    'result': 'Gram-negative diplococci (kidney bean shaped)',
                    'explanation': 'Characteristic morphology of intracellular and extracellular diplococci'
                },
                {
                    'test': 'Oxidase Test',
                    'result': 'Positive (purple color in 10 seconds)',
                    'explanation': 'Rapid oxidase positive reaction is characteristic'
                }
            ]
        },
        {
            'name': 'Biochemical Tests',
            'tests': [
                {
                    'test': 'Carbohydrate Utilization',
                    'result': 'Glucose positive, Maltose negative, Sucrose negative',
                    'explanation': 'Differentiates from other Neisseria species'
                },
                {
                    'test': 'Catalase Test',
                    'result': 'Positive',
                    'explanation': 'Helps differentiate from other organisms'
                }
            ]
        },
        {
            'name': 'Additional Tests',
            'tests': [
                {
                    'test': 'Superoxol Test (30% H₂O₂)',
                    'result': 'Strong positive (vigorous bubbling)',
                    'explanation': 'Distinguishes from other Neisseria species'
                },
                {
                    'test': 'Beta-lactamase Test',
                    'result': 'Variable (positive in resistant strains)',
                    'explanation': 'Determines penicillin resistance'
                }
            ]
        }
    ],
    'c_difficile': [
        {
            'name': 'Primary Tests',
            'tests': [
                {'test': 'GDH Antigen Test', 'result': 'Positive', 'explanation': 'Indicates presence of C. difficile (screening test)'},
                {'test': 'Toxin A/B Test', 'result': 'Positive', 'explanation': 'Confirms toxin production'},
                {'test': 'NAAT/PCR', 'result': 'Positive for tcdA/tcdB genes', 'explanation': 'Detects toxin genes'}
            ]
        },
        {
            'name': 'Additional Tests',
            'tests': [
                {'test': 'PRO Disk Test', 'result': 'Positive (yellow fluorescence)', 'explanation': 'Confirms proline aminopeptidase production'},
                {'test': 'L-proline-aminopeptidase', 'result': 'Positive', 'explanation': 'Characteristic of C. difficile'}
            ]
        }
    ],
    'h_influenzae': [
        {
            'name': 'Growth Factor Requirements',
            'tests': [
                {'test': 'X Factor Requirement', 'result': 'Positive', 'explanation': 'Requires hemin (X factor) for growth'},
                {'test': 'V Factor Requirement', 'result': 'Positive', 'explanation': 'Requires NAD (V factor) for growth'},
                {'test': 'Satellite Test', 'result': 'Positive', 'explanation': 'Growth around S. aureus streak on blood agar'}
            ]
        },
        {
            'name': 'Biochemical Tests',
            'tests': [
                {'test': 'Oxidase Test', 'result': 'Positive', 'explanation': 'Shows oxidase enzyme activity'},
                {'test': 'Catalase Test', 'result': 'Positive', 'explanation': 'Produces catalase enzyme'}
            ]
        }
    ],
    'l_pneumophila': [
        {
            'name': 'Growth Requirements',
            'tests': [
                {'test': 'L-cysteine Requirement', 'result': 'Positive', 'explanation': 'Requires L-cysteine for growth'},
                {'test': 'Iron Requirement', 'result': 'Positive', 'explanation': 'Requires iron salts for growth'},
                {'test': 'Growth on BCYE vs. Blood Agar', 'result': 'Growth on BCYE only', 'explanation': 'Distinguishes from other bacteria'}
            ]
        },
        {
            'name': 'Biochemical Tests',
            'tests': [
                {'test': 'Catalase Test', 'result': 'Positive', 'explanation': 'Shows catalase production'},
                {'test': 'Oxidase Test', 'result': 'Positive', 'explanation': 'Shows oxidase production'},
                {'test': 'Hippurate Hydrolysis', 'result': 'Positive', 'explanation': 'Distinguishes L. pneumophila from other Legionella species'}
            ]
        }
    ],
    'aspergillus': [
        {
            'name': 'Microscopic Examination',
            'tests': [
                {'test': 'KOH Mount', 'result': 'Septate hyphae with characteristic conidial heads', 'explanation': 'Shows typical Aspergillus morphology'},
                {'test': 'Lactophenol Cotton Blue Mount', 'result': 'Species-specific conidial head structure', 'explanation': 'Helps identify specific Aspergillus species'}
            ]
        },
        {
            'name': 'Culture Characteristics',
            'tests': [
                {'test': 'Growth Rate', 'result': 'Rapid (3-5 days)', 'explanation': 'Characteristic of Aspergillus species'},
                {'test': 'Temperature Tolerance', 'result': 'Growth at 37°C', 'explanation': 'Important for pathogenic species identification'}
            ]
        }
    ],
    'c_albicans': [
        {
            'name': 'Primary Tests',
            'tests': [
                {'test': 'Germ Tube Test', 'result': 'Positive within 2-3 hours', 'explanation': 'Rapid presumptive identification'},
                {'test': 'Chlamydospore Formation', 'result': 'Positive on corn meal agar', 'explanation': 'Characteristic of C. albicans'}
            ]
        },
        {
            'name': 'Biochemical Tests',
            'tests': [
                {'test': 'Carbohydrate Assimilation', 'result': 'Species-specific pattern', 'explanation': 'Confirms identification'},
                {'test': 'CHROMagar Growth', 'result': 'Green colonies', 'explanation': 'Distinguishes from other Candida species'}
            ]
        }
    ],
    'c_auris': [
        {
            'name': 'Identification Tests',
            'tests': [
                {'test': 'MALDI-TOF MS', 'result': 'Specific pattern for C. auris', 'explanation': 'Most reliable identification method'},
                {'test': 'Growth at 42°C', 'result': 'Positive', 'explanation': 'Distinguishes from many other Candida species'}
            ]
        },
        {
            'name': 'Biochemical Tests',
            'tests': [
                {'test': 'Carbohydrate Assimilation', 'result': 'Species-specific pattern', 'explanation': 'Helps differentiate from other Candida species'},
                {'test': 'CHROMagar Growth', 'result': 'Pale to pink colonies', 'explanation': 'Initial screening, requires confirmation'}
            ]
        }
    ],
    'a_baumannii': [
        {
            'name': 'Primary Identification Tests',
            'tests': [
                {'test': 'Gram Stain', 'result': 'Gram-negative coccobacilli', 'explanation': 'Often appears as diplococci or short chains'},
                {'test': 'Oxidase Test', 'result': 'Negative', 'explanation': 'Distinguishes from other non-fermenters like Pseudomonas'},
                {'test': 'Catalase Test', 'result': 'Positive', 'explanation': 'Characteristic of Acinetobacter species'}
            ]
        },
        {
            'name': 'Growth Characteristics',
            'tests': [
                {'test': 'Growth at 42°C', 'result': 'Positive', 'explanation': 'Helps differentiate from other Acinetobacter species'},
                {'test': 'Growth on MacConkey', 'result': 'Positive (non-lactose fermenter)', 'explanation': 'Shows ability to grow on selective media'},
                {'test': '10% OF Glucose', 'result': 'Oxidative', 'explanation': 'Shows oxidative metabolism of glucose'}
            ]
        },
        {
            'name': 'Biochemical Tests',
            'tests': [
                {'test': 'Citrate Utilization', 'result': 'Positive', 'explanation': 'Can use citrate as sole carbon source'},
                {'test': 'Triple Sugar Iron', 'result': 'K/NC (No change)', 'explanation': 'Non-fermenter, no acid or gas production'},
                {'test': 'Motility', 'result': 'Non-motile', 'explanation': 'Characteristic of Acinetobacter species'}
            ]
        }
    ]
}

growth_characteristics = {
    'e_coli': {
        'mac_conkey': {
            'morphology': 'Circular, smooth, convex colonies',
            'color': 'Pink to red (lactose fermenter)',
            'size': '2-3 mm in diameter',
            'other': 'May show bile precipitation'
        },
        'emb': {
            'morphology': 'Circular, flat colonies',
            'color': 'Green metallic sheen',
            'size': '2-3 mm in diameter',
            'other': 'Distinctive metallic sheen is characteristic'
        },
        'blood_agar': {
            'morphology': 'Circular, smooth colonies',
            'color': 'Grey-white, opaque',
            'size': '1-2 mm in diameter',
            'other': 'May show alpha or gamma hemolysis'
        },
        'chocolate_agar': {
            'morphology': 'Circular, smooth, convex colonies',
            'color': 'Grey to greyish-brown',
            'size': '2-3 mm in diameter',
            'other': 'Good growth due to X and V factors availability'
        }
    },
    's_aureus': {
        'mannitol_salt': {
            'morphology': 'Circular, convex colonies',
            'color': 'Yellow colonies with yellow zones',
            'size': '1-2 mm in diameter',
            'other': 'Yellow color indicates mannitol fermentation'
        },
        'blood_agar': {
            'morphology': 'Circular, convex colonies',
            'color': 'Golden yellow',
            'size': '1-2 mm in diameter',
            'other': 'Clear beta-hemolysis zone around colonies'
        },
        'chocolate_agar': {
            'morphology': 'Circular, convex colonies',
            'color': 'Golden yellow to cream',
            'size': '1-2 mm in diameter',
            'other': 'Excellent growth with typical pigmentation'
        }
    },
    'p_aeruginosa': {
        'mueller_hinton': {
            'morphology': 'Irregular, flat colonies',
            'color': 'Blue-green with fluorescence',
            'size': '2-4 mm in diameter',
            'other': 'Characteristic grape-like odor'
        },
        'blood_agar': {
            'morphology': 'Spreading, flat colonies',
            'color': 'Blue-green with metallic sheen',
            'size': '3-5 mm spreading growth',
            'other': 'Beta-hemolysis and pyocyanin production'
        },
        'chocolate_agar': {
            'morphology': 'Large, spreading colonies',
            'color': 'Blue-green to brown-green',
            'size': '3-4 mm in diameter',
            'other': 'Produces characteristic pigment, good growth'
        }
    },
    'k_pneumoniae': {
        'mac_conkey': {
            'morphology': 'Large, dome-shaped, mucoid colonies',
            'color': 'Pink (lactose fermenter)',
            'size': '4-5 mm in diameter',
            'other': 'Characteristically mucoid appearance'
        },
        'emb': {
            'morphology': 'Large, mucoid colonies',
            'color': 'Purple with dark centers',
            'size': '3-4 mm in diameter',
            'other': 'No metallic sheen unlike E. coli'
        },
        'chocolate_agar': {
            'morphology': 'Large, mucoid, dome-shaped colonies',
            'color': 'Grey to greyish-brown, mucoid',
            'size': '3-4 mm in diameter',
            'other': 'Characteristic mucoid appearance, good growth'
        }
    },
    's_pneumoniae': {
        'blood_agar': {
            'morphology': 'Small, round, mucoid colonies with characteristic "draughtsman" appearance (depressed center)',
            'color': 'Grayish-green colonies surrounded by a green zone (alpha-hemolysis)',
            'size': '1-2 mm in diameter after 24 hours incubation',
            'additional_features': 'Alpha-hemolysis (green zone) around colonies, colonies appear flat or slightly umbilicated (draughtsman-like)'
        }
    },
    'n_gonorrhoeae': {
        'chocolate_agar': {
            'morphology': 'Small, round, raised, convex colonies with smooth edges',
            'color': 'Gray to white, translucent to opaque',
            'size': '0.5-1 mm in diameter after 24 hours',
            'additional_features': 'Colonies appear moist and glistening, may show slight brown pigmentation in center'
        },
        'thayer_martin': {
            'morphology': 'Small, round, raised colonies with entire margins',
            'color': 'Gray to colorless, translucent',
            'size': '0.5-1 mm in diameter',
            'additional_features': 'Selective medium inhibits normal flora, allowing isolation of N. gonorrhoeae'
        }
    },
    'c_difficile': {
        'ccfa': {
            'morphology': 'Large, slightly raised, yellow colonies with ground-glass appearance',
            'color': 'Yellow to light yellow',
            'size': '2-4 mm in diameter after 48 hours',
            'additional_features': 'Characteristic ground-glass appearance and yellow fluorescence under UV light'
        }
    },
    'h_influenzae': {
        'chocolate_agar': {
            'morphology': 'Small, round, convex colonies with smooth edges',
            'color': 'Grayish, transparent to pearl-like',
            'size': '0.5-1 mm in diameter after 24 hours',
            'additional_features': 'Colonies appear moist and show satellite growth around Staphylococcus streak'
        }
    },
    'l_pneumophila': {
        'bcye': {
            'morphology': 'Round to oval colonies with entire margins',
            'color': 'Gray-white to blue-gray, glistening',
            'size': '1-2 mm in diameter after 48-72 hours',
            'additional_features': 'Ground-glass appearance, may show internal structure with dissecting microscope'
        }
    },
    'aspergillus': {
        'sab_dex': {
            'morphology': 'Filamentous colonies with powdery surface',
            'color': 'Initially white, then characteristic colors depending on species (green, yellow, black)',
            'size': 'Rapidly spreading, covering plate in 3-5 days',
            'additional_features': 'Distinctive conidial heads visible microscopically, reverse side may show characteristic pigmentation'
        }
    },
    'c_albicans': {
        'sab_dex': {
            'morphology': 'Smooth, creamy colonies with yeast-like appearance',
            'color': 'Cream to white',
            'size': '2-4 mm in diameter after 48-72 hours',
            'additional_features': 'Characteristic yeast odor, smooth pasty texture'
        },
        'chrom_agar': {
            'morphology': 'Smooth, convex colonies',
            'color': 'Distinctive green color',
            'size': '2-3 mm in diameter after 48 hours',
            'additional_features': 'Green color specific to C. albicans, helps differentiate from other Candida species'
        }
    },
    'c_auris': {
        'sab_dex': {
            'morphology': 'Smooth, white to cream colored colonies',
            'color': 'White to cream',
            'size': '1-3 mm in diameter after 48 hours',
            'additional_features': 'Similar to other Candida species, requires additional testing for confirmation'
        },
        'chrom_agar': {
            'morphology': 'Smooth, circular colonies',
            'color': 'Pale to light pink',
            'size': '1-2 mm in diameter after 48 hours',
            'additional_features': 'Color varies by strain and manufacturer, may appear similar to C. haemulonii'
        }
    },
    'a_baumannii': {
        'blood_agar': {
            'morphology': 'Smooth, dome-shaped colonies with entire margins',
            'color': 'White to cream-colored, opaque',
            'size': '1.5-2.5 mm in diameter after 24 hours',
            'additional_features': 'Non-hemolytic, mucoid appearance in some strains, colonies become more opaque with incubation'
        },
        'mac_conkey': {
            'morphology': 'Smooth, slightly domed colonies',
            'color': 'Pink to mauve (non-lactose fermenter)',
            'size': '1-2 mm in diameter',
            'additional_features': 'Faint pink color due to slight uptake of crystal violet, may appear slightly mucoid'
        }
    }
}

# Add plate image mapping
PLATE_IMAGES = {
    'e_coli': {
        'mac_conkey': [
            {
                'src': '/static/images/organisms/ecoli/e_coli_mac_1.jpg',
                'caption': 'E. coli on MacConkey Agar - Typical pink colonies (lactose fermenter)'
            },
            {
                'src': '/static/images/organisms/ecoli/e_coli_mac_2.jpg',
                'caption': 'E. coli on MacConkey Agar - Close-up view showing bile precipitation'
            },
            {
                'src': '/static/images/organisms/ecoli/e_coli_mac_3.jpg',
                'caption': 'E. coli on MacConkey Agar - Mixed culture showing distinct colonies'
            }
        ],
        'emb': [
            {
                'src': '/static/images/organisms/ecoli/e_coli_emb_1.jpg',
                'caption': 'E. coli on EMB Agar - Characteristic metallic sheen'
            }
        ],
        'blood_agar': [
            {
                'src': '/static/images/organisms/ecoli/e_coli_blood_1.jpg',
                'caption': 'E. coli on Blood Agar - Grey-white colonies'
            }
        ]
    },
    's_aureus': {
        'mannitol_salt': [
            {
                'src': 's_aureus_msa_1.jpg',
                'caption': 'S. aureus on MSA - Yellow colonies with yellow zones'
            }
        ],
        'blood_agar': [
            {
                'src': 's_aureus_blood_1.jpg',
                'caption': 'S. aureus on Blood Agar - Golden colonies with beta-hemolysis'
            }
        ]
    },
    'p_aeruginosa': {
        'mueller_hinton': [
            {
                'src': 'p_aeruginosa_mh.jpg',
                'caption': 'P. aeruginosa on Mueller Hinton Agar - Blue-green colonies with characteristic fluorescence'
            }
        ],
        'blood_agar': [
            {
                'src': 'p_aeruginosa_blood.jpg',
                'caption': 'P. aeruginosa on Blood Agar - Blue-green colonies with beta-hemolysis'
            }
        ]
    },
    'k_pneumoniae': {
        'mac_conkey': [
            {
                'src': 'k_pneumoniae_mac.jpg',
                'caption': 'K. pneumoniae on MacConkey Agar - Large, mucoid pink colonies'
            }
        ],
        'blood_agar': [
            {
                'src': 'k_pneumoniae_blood.jpg',
                'caption': 'K. pneumoniae on Blood Agar - Large, mucoid grey colonies'
            }
        ]
    },
    's_pneumoniae': {
        'blood_agar': [
            {
                'src': 's_pneumoniae_blood.jpg',
                'caption': 'S. pneumoniae on Blood Agar - Small colonies with alpha-hemolysis (green zone)'
            }
        ]
    },
    'n_gonorrhoeae': {
        'chocolate_agar': [
            {
                'src': 'n_gonorrhoeae_choc.jpg',
                'caption': 'N. gonorrhoeae on Chocolate Agar - Small, grey to white colonies'
            }
        ],
        'thayer_martin': [
            {
                'src': 'n_gonorrhoeae_tm.jpg',
                'caption': 'N. gonorrhoeae on Thayer-Martin Agar - Small, grey colonies on selective media'
            }
        ]
    },
    'c_difficile': {
        'ccfa': [
            {
                'src': 'c_difficile_ccfa.jpg',
                'caption': 'C. difficile on CCFA - Yellow colonies with ground-glass appearance'
            }
        ]
    },
    'h_influenzae': {
        'chocolate_agar': [
            {
                'src': 'h_influenzae_choc.jpg',
                'caption': 'H. influenzae on Chocolate Agar - Small, transparent colonies'
            }
        ]
    },
    'l_pneumophila': {
        'bcye': [
            {
                'src': 'l_pneumophila_bcye.jpg',
                'caption': 'L. pneumophila on BCYE - Grey-white, glistening colonies'
            }
        ]
    },
    'aspergillus': {
        'sab_dex': [
            {
                'src': 'aspergillus_sda.jpg',
                'caption': 'Aspergillus species on Sabouraud Dextrose Agar - Filamentous colonies with characteristic coloration'
            }
        ]
    },
    'c_albicans': {
        'sab_dex': [
            {
                'src': 'c_albicans_sda.jpg',
                'caption': 'C. albicans on Sabouraud Dextrose Agar - Cream colored, smooth colonies'
            }
        ],
        'chrom_agar': [
            {
                'src': 'c_albicans_chrom.jpg',
                'caption': 'C. albicans on CHROMagar - Characteristic green colonies'
            }
        ]
    },
    'c_auris': {
        'sab_dex': [
            {
                'src': 'c_auris_sda.jpg',
                'caption': 'C. auris on Sabouraud Dextrose Agar - White to cream colored colonies'
            }
        ],
        'chrom_agar': [
            {
                'src': 'c_auris_chrom.jpg',
                'caption': 'C. auris on CHROMagar - Pale to light pink colonies'
            }
        ]
    },
    'a_baumannii': {
        'blood_agar': [
            {
                'src': 'a_baumannii_blood.jpg',
                'caption': 'A. baumannii on Blood Agar - White to cream-colored, non-hemolytic colonies'
            }
        ],
        'mac_conkey': [
            {
                'src': 'a_baumannii_mac.jpg',
                'caption': 'A. baumannii on MacConkey Agar - Pink to mauve colonies (non-lactose fermenter)'
            }
        ]
    }
}

# Media example images mapping
MEDIA_EXAMPLE_IMAGES = {
    'emb': [
        {
            'src': '/static/images/plates/emb/emb_blank.jpg',
            'caption': 'Uninoculated EMB Agar plate'
        },
        {
            'src': '/static/images/plates/emb/emb_ecoli_metallic.jpg',
            'caption': 'E. coli showing characteristic metallic green sheen on EMB'
        },
        {
            'src': '/static/images/plates/emb/emb_mixed_culture.jpg',
            'caption': 'Mixed culture showing lactose fermenters (dark purple/metallic) and non-fermenters (colorless)'
        }
    ],
    'blood_agar': [
        {
            'src': '/static/images/plates/blood/blood_blank.jpg',
            'caption': 'Uninoculated Blood Agar plate'
        },
        {
            'src': '/static/images/plates/blood/blood_alpha_hemolysis.jpg',
            'caption': 'Example of alpha hemolysis on Blood Agar'
        },
        {
            'src': '/static/images/plates/blood/blood_beta_hemolysis.jpg',
            'caption': 'Example of beta hemolysis on Blood Agar'
        }
    ],
    'mac_conkey': [
        {
            'src': '/static/images/plates/mac/mac_blank.jpg',
            'caption': 'Uninoculated MacConkey Agar plate'
        },
        {
            'src': '/static/images/plates/mac/mac_lactose_pos.jpg',
            'caption': 'Example of lactose-fermenting colonies (pink/red)'
        },
        {
            'src': '/static/images/plates/mac/mac_lactose_neg.jpg',
            'caption': 'Example of non-lactose-fermenting colonies (colorless)'
        }
    ],
    'chocolate_agar': [
        {
            'src': '/static/images/plates/chocolate/choc_blank.jpg',
            'caption': 'Uninoculated Chocolate Agar plate'
        },
        {
            'src': '/static/images/plates/chocolate/choc_neisseria.jpg',
            'caption': 'Example of Neisseria growth on Chocolate Agar'
        },
        {
            'src': '/static/images/plates/chocolate/choc_haemophilus.jpg',
            'caption': 'Example of Haemophilus growth on Chocolate Agar'
        }
    ]
}

# Dictionary containing information about different culture media
MEDIA_INFO = {
    'blood_agar': {
        'name': 'Blood Agar',
        'type': 'General Purpose/Enriched Media',
        'purpose': 'Used for culturing fastidious organisms and detecting hemolytic patterns',
        'composition': [
            {'name': 'Blood', 'description': '5-10% sheep or horse blood'},
            {'name': 'Peptones', 'description': 'Provides nitrogen, vitamins, and amino acids'},
            {'name': 'Sodium Chloride', 'description': 'Maintains osmotic balance'},
            {'name': 'Agar', 'description': 'Solidifying agent'}
        ],
        'characteristics': [
            'Appears red-brown in color',
            'Can observe different types of hemolysis (alpha, beta, gamma)',
            'Supports growth of most clinically significant bacteria'
        ],
        'common_uses': [
            'Isolation of fastidious organisms',
            'Detection of hemolytic patterns in Streptococci and other bacteria',
            'Primary isolation medium for clinical specimens'
        ],
        'images': [
            {'src': '/static/images/plates/blood/blood_blank.jpg', 'caption': 'Uninoculated Blood Agar plate'},
            {'src': '/static/images/plates/blood/blood_beta.jpg', 'caption': 'Beta hemolysis on Blood Agar'},
            {'src': '/static/images/plates/blood/blood_alpha.jpg', 'caption': 'Alpha hemolysis on Blood Agar'}
        ]
    },
    'mac_conkey': {
        'name': 'MacConkey Agar',
        'type': 'Selective and Differential Media',
        'purpose': 'Selective for Gram-negative bacteria and differentiates lactose fermenters from non-fermenters',
        'composition': [
            {'name': 'Peptones', 'description': 'Provides nitrogen and other nutrients'},
            {'name': 'Lactose', 'description': 'Fermentable carbohydrate'},
            {'name': 'Bile Salts', 'description': 'Inhibits growth of Gram-positive organisms'},
            {'name': 'Neutral Red', 'description': 'pH indicator that turns red in acid conditions'},
            {'name': 'Crystal Violet', 'description': 'Additional inhibitor of Gram-positive organisms'}
        ],
        'characteristics': [
            'Appears pink to red in color',
            'Lactose fermenters produce pink/red colonies',
            'Non-lactose fermenters produce colorless colonies',
            'Selective against Gram-positive organisms'
        ],
        'common_uses': [
            'Isolation of Gram-negative enteric bacteria',
            'Differentiation of lactose-fermenting from non-lactose-fermenting bacteria',
            'Screening for potential pathogens in clinical specimens'
        ],
        'images': [
            {'src': '/static/images/plates/mac/mac_blank.jpg', 'caption': 'Uninoculated MacConkey Agar plate'},
            {'src': '/static/images/plates/mac/mac_ecoli.jpg', 'caption': 'E. coli growth (pink colonies)'},
            {'src': '/static/images/plates/mac/mac_mixed.jpg', 'caption': 'Mixed growth showing lactose and non-lactose fermenters'}
        ]
    },
    'chocolate_agar': {
        'name': 'Chocolate Agar',
        'type': 'Enriched Media',
        'purpose': 'Used for isolating fastidious organisms that require X factor (heme/hemin) and other nutrients released from lysed red blood cells',
        'composition': [
            {'name': 'Blood Base', 'description': 'Similar to blood agar base'},
            {'name': 'Lysed Red Blood Cells', 'description': 'Added to molten agar base and lysed during preparation, releasing intracellular nutrients'},
            {'name': 'X Factor (Heme/Hemin)', 'description': 'Released from lysed red blood cells, essential for growth of some fastidious bacteria'},
            {'name': 'Additional Nutrients', 'description': 'Released from lysed red blood cells during preparation'}
        ],
        'characteristics': [
            'Chocolate-brown color due to lysed red blood cells',
            'Enriched medium containing essential growth factors',
            'Similar to blood agar but with lysed red blood cells',
            'Provides X factor (heme/hemin) necessary for fastidious organisms'
        ],
        'common_uses': [
            'Isolation of Neisseria gonorrhoeae (causative agent of gonorrhea)',
            'Culture of Haemophilus influenzae (respiratory and middle ear infections)',
            'Growth of fastidious organisms that cannot grow on regular blood agar',
            'Primary isolation medium for organisms requiring X factor'
        ],
        'images': [
            {'src': '/static/images/plates/chocolate/choc_blank.jpg', 'caption': 'Uninoculated Chocolate Agar plate showing characteristic brown color'},
            {'src': '/static/images/plates/chocolate/choc_ng.jpg', 'caption': 'N. gonorrhoeae growth on Chocolate Agar'},
            {'src': '/static/images/plates/chocolate/choc_hi.jpg', 'caption': 'H. influenzae growth on Chocolate Agar'}
        ]
    },
    'emb': {
        'name': 'Eosin Methylene Blue (EMB) Agar, Levine',
        'type': 'Selective and Differential Media',
        'purpose': 'Primary selective and differential medium for isolation and differentiation of Gram-negative bacteria based on lactose fermentation',
        'composition': [
            {'name': 'Eosin Y', 'description': 'Inhibits growth of Gram-positive bacteria and acts as pH indicator'},
            {'name': 'Methylene Blue', 'description': 'Inhibits Gram-positive bacteria and serves as pH indicator'},
            {'name': 'Lactose', 'description': 'Fermentable carbohydrate for differentiation'},
            {'name': 'Peptone', 'description': 'Provides nitrogen and nutrients'},
            {'name': 'Agar', 'description': 'Solidifying agent'}
        ],
        'characteristics': [
            'Lactose fermenters appear dark purple to black, or with distinctive green metallic sheen',
            'Non-lactose fermenters remain colorless and translucent',
            'Selective against Gram-positive bacteria',
            'Color interpretation may be challenging with slow lactose fermenters',
            'Results may take longer than 24 hours for slow fermenters'
        ],
        'common_uses': [
            'Isolation and differentiation of Gram-negative bacteria',
            'Identification of lactose-fermenting organisms',
            'Detection of coliform bacteria (especially E. coli with its characteristic metallic sheen)',
            'Differentiation between lactose fermenters and non-fermenters like Shigella species'
        ],
        'images': [
            {'src': '/static/images/plates/emb/emb_blank.jpg', 'caption': 'Uninoculated EMB Agar plate'},
            {'src': '/static/images/plates/emb/emb_ecoli.jpg', 'caption': 'E. coli showing characteristic metallic green sheen'},
            {'src': '/static/images/plates/emb/emb_mixed.jpg', 'caption': 'Mixed culture showing lactose fermenters (dark) and non-fermenters (colorless)'}
        ],
        'special_notes': [
            'Interpretation requires experience due to subtle color differences',
            'Slow lactose fermenters may not show typical reactions within 24 hours',
            'Results should be interpreted with caution for organism identification',
            'Color changes may be difficult to distinguish from media background'
        ]
    },
    'mueller_hinton': {
        'name': 'Mueller Hinton Agar',
        'type': 'Susceptibility Testing Media',
        'purpose': 'Standard medium for antimicrobial susceptibility testing (AST) of non-fastidious bacteria',
        'composition': [
            {'name': 'Beef Extract', 'description': 'Provides nutrients and growth factors'},
            {'name': 'Acid Hydrolysate of Casein', 'description': 'Source of amino acids and proteins'},
            {'name': 'Starch', 'description': 'Absorbs toxic metabolites and provides slow nutrient release'},
            {'name': 'Agar', 'description': 'Solidifying agent'}
        ],
        'characteristics': [
            'Standardized depth (4mm) for consistent diffusion',
            'Low in sulfonamide, trimethoprim, and tetracycline inhibitors',
            'Controlled calcium and magnesium content',
            'pH standardized to 7.2-7.4 at room temperature'
        ],
        'common_uses': [
            'Disk diffusion antibiotic susceptibility testing',
            'E-test (MIC determination)',
            'Quality control testing of antimicrobials',
            'Standard medium for CLSI/EUCAST testing protocols'
        ],
        'images': [
            {'src': '/static/images/plates/mueller_hinton/mh_blank.jpg', 'caption': 'Uninoculated Mueller Hinton Agar plate'},
            {'src': '/static/images/plates/mueller_hinton/mh_ast.jpg', 'caption': 'Antibiotic susceptibility testing showing zones of inhibition'},
            {'src': '/static/images/plates/mueller_hinton/mh_etest.jpg', 'caption': 'E-test on Mueller Hinton Agar'}
        ]
    },
    'mannitol_salt': {
        'name': 'Mannitol Salt Agar',
        'type': 'Selective and Differential Media',
        'purpose': 'Selective medium for isolation and differentiation of Staphylococci based on mannitol fermentation',
        'composition': [
            {'name': 'Mannitol', 'description': 'Fermentable carbohydrate for differentiation'},
            {'name': 'Sodium Chloride (7.5%)', 'description': 'Selective agent inhibiting most bacteria except Staphylococci'},
            {'name': 'Phenol Red', 'description': 'pH indicator showing mannitol fermentation'},
            {'name': 'Peptones', 'description': 'Provides nutrients for bacterial growth'},
            {'name': 'Agar', 'description': 'Solidifying agent'}
        ],
        'characteristics': [
            'High salt concentration (7.5% NaCl) selects for Staphylococci',
            'Mannitol fermentation produces yellow zones around colonies',
            'Original medium color is red/pink',
            'S. aureus typically produces yellow colonies with yellow zones'
        ],
        'common_uses': [
            'Isolation of Staphylococci from clinical specimens',
            'Differentiation of S. aureus (mannitol-positive) from other Staphylococci',
            'Screening for pathogenic Staphylococci',
            'Processing of nasal swabs for MRSA screening'
        ],
        'images': [
            {'src': '/static/images/plates/mannitol_salt/msa_blank.jpg', 'caption': 'Uninoculated Mannitol Salt Agar plate'},
            {'src': '/static/images/plates/mannitol_salt/msa_saureus.jpg', 'caption': 'S. aureus showing yellow colonies with yellow zones'},
            {'src': '/static/images/plates/mannitol_salt/msa_mixed.jpg', 'caption': 'Mixed culture showing mannitol fermenters and non-fermenters'}
        ]
    }
}

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        organism = request.form.get('organism')
        media = request.form.get('media')
        
        # Get organism-specific tests and growth characteristics
        confirmatory_tests = CONFIRMATORY_TESTS_DATA.get(organism, {})
        characteristics = growth_characteristics.get(organism, {}).get(media, {})
        
        # Get the corresponding plate images if available
        plate_images = PLATE_IMAGES.get(organism, {}).get(media, [])
        
        return render_template('results.html',
                             organism=organism,
                             media=media,
                             confirmatory_tests=confirmatory_tests,
                             characteristics=characteristics,
                             plate_images=plate_images)
    return redirect(url_for('main.home'))

@main_bp.route('/media-search')
def media_search():
    """Route for the media search page"""
    return render_template('media_search.html')

@main_bp.route('/organism_search')
def organism_search():
    """Route for the organism search page"""
    return render_template('organism_search.html')

@main_bp.route('/media-info', methods=['POST'])
def media_info():
    """Route for displaying detailed media information"""
    media_id = request.form.get('media')
    if media_id not in MEDIA_INFO:
        flash('Selected media not found', 'error')
        return redirect(url_for('main.media_search'))
    
    media_data = MEDIA_INFO[media_id]
    # Get both specific media info images and example images
    media_images = media_data.get('images', [])
    example_images = MEDIA_EXAMPLE_IMAGES.get(media_id, [])
    
    return render_template('media_info.html',
                         media_name=media_data['name'],
                         media_type=media_data['type'],
                         purpose=media_data['purpose'],
                         composition=media_data['composition'],
                         characteristics=media_data['characteristics'],
                         common_uses=media_data['common_uses'],
                         media_images=media_images,
                         example_images=example_images) 