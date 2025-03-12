from flask import Blueprint, render_template, request, redirect, url_for, flash
import os

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
    's_pneumoniae': [
        {
            'name': 'Primary Tests',
            'tests': [
                {
                    'test': 'Optochin Sensitivity Test',
                    'result': 'Sensitive (zone of inhibition ≥14 mm)',
                    'explanation': 'Differentiates S. pneumoniae (optochin-sensitive) from viridans streptococci (optochin-resistant).'
                },
                {
                    'test': 'Bile Solubility Test',
                    'result': 'Positive (colony lysis in bile salts)',
                    'explanation': 'S. pneumoniae is bile-soluble, while other alpha-hemolytic streptococci are not.'
                },
                {
                    'test': 'Gram Stain',
                    'result': 'Gram-positive, lancet-shaped diplococci',
                    'explanation': 'Distinctive morphology of S. pneumoniae.'
                }
            ]
        },
        {
            'name': 'Additional Tests',
            'tests': [
                {
                    'test': 'Catalase Test',
                    'result': 'Negative',
                    'explanation': 'Differentiates S. pneumoniae from catalase-positive bacteria like Staphylococcus species.'
                },
                {
                    'test': 'Quellung Reaction',
                    'result': 'Positive (capsular swelling seen under microscope)',
                    'explanation': 'Identifies S. pneumoniae by detecting its polysaccharide capsule using specific antisera.'
                },
                {
                    'test': 'PCR for S. pneumoniae',
                    'result': 'Positive for pneumococcal-specific genes (e.g., lytA, ply)',
                    'explanation': 'Molecular confirmation of S. pneumoniae in clinical samples.'
                }
            ]
        }
    ],
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
            'name': 'Cycloserine Cefoxitin Fructose Agar (CCFA)',
            'type': 'Selective and Differential Media',
            'purpose': 'Isolation and identification of Clostridioides difficile from fecal specimens',
            'composition': [
                {'name': 'Fructose', 'description': 'Main carbohydrate for fermentation by C. difficile'},
                {'name': 'Neutral Red Indicator', 'description': 'Detects acid production from fructose fermentation (color change)'},
                {'name': 'Cycloserine', 'description': 'Inhibits Gram-negative bacteria'},
                {'name': 'Cefoxitin', 'description': 'Inhibits most Gram-positive bacteria (except C. difficile)'},
                {'name': 'Agar Base', 'description': 'Provides nutrients and support for bacterial growth'}
            ],
            'characteristics': [
                'C. difficile ferments fructose, producing acid which turns the medium yellow',
                'Colonies appear yellow, irregular, and have a characteristic horse manure-like odor',
                'Not completely specific for C. difficile - further confirmation required',
                'Requires toxigenic testing (PCR, ELISA for toxins A & B) for confirmation'
            ],
            'common_uses': [
                'Primary isolation of C. difficile from stool samples in suspected pseudomembranous colitis',
                'Isolation in cases of C. difficile infection (CDI)',
                'Differentiation of C. difficile from other Clostridium species based on fructose fermentation and antibiotic resistance'
            ],
            'special_notes': [
                'Some non-C. difficile Clostridium species may also grow',
                'Does not differentiate toxigenic from non-toxigenic strains—additional testing needed for toxin detection',
                'CCFA has largely been replaced by chromogenic media and molecular methods'
            ]
        },
        'xld': {
            'name': 'Xylose-Lysine-Deoxycholate (XLD) Agar',
            'type': 'Selective and Differential Media',
            'purpose': 'Used for the isolation and differentiation of Shigella species and Salmonella species from other non-pathogenic enteric bacteria',
            'composition': [
                {'name': 'Sodium Deoxycholate', 'description': 'Selective agent that inhibits gram-positive organisms and many non-enteric gram-negative bacilli'},
                {'name': 'Xylose', 'description': 'Fermentable carbohydrate for differentiation'},
                {'name': 'Lysine', 'description': 'Amino acid for detecting lysine decarboxylation'},
                {'name': 'Lactose and Sucrose', 'description': 'Additional fermentable carbohydrates for differentiation'},
                {'name': 'Phenol Red', 'description': 'pH indicator that detects acid production from carbohydrate fermentation'},
                {'name': 'Sodium Thiosulfate and Ferric Ammonium Citrate', 'description': 'H₂S indicator system'},
                {'name': 'Agar Base', 'description': 'Solidifying agent'}
            ],
            'characteristics': [
                'Base medium appears pink to red in color',
                'Differential characteristics based on:',
                '- Carbohydrate fermentation (xylose, lactose, sucrose)',
                '- Lysine decarboxylation',
                '- H₂S production',
                'Colony appearances:',
                '- Shigella spp.: Colorless colonies (red, same as medium)',
                '- Salmonella spp.: Colorless colonies with black centers (H₂S production)',
                '- Non-pathogenic fermenters: Yellow colonies'
            ],
            'common_uses': [
                'Isolation and identification of Shigella species',
                'Isolation and identification of Salmonella species',
                'Differentiation of pathogenic enteric bacteria from non-pathogenic organisms',
                'Processing of stool specimens for enteric pathogens'
            ],
            'special_notes': [
                'Salmonella colonies remain colorless despite xylose fermentation due to lysine decarboxylation raising pH',
                'Black center in Salmonella colonies is due to H₂S production',
                'Yellow colonies typically indicate non-pathogenic organisms that ferment one or more of the carbohydrates'
            ],
            'images': [
                {'src': '/static/images/plates/xld/xld_blank.jpg', 'caption': 'Uninoculated XLD Agar plate'},
                {'src': '/static/images/plates/xld/xld_salmonella.jpg', 'caption': 'Salmonella species showing characteristic black-centered colonies'},
                {'src': '/static/images/plates/xld/xld_shigella.jpg', 'caption': 'Shigella species showing colorless colonies'}
            ]
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
    },
    'bcye': {
        'name': 'Buffered Charcoal Yeast Extract (BCYE) Agar',
        'type': 'Selective and Enriched Medium',
        'purpose': 'Used for the isolation of Legionella species, particularly Legionella pneumophila, from clinical and environmental samples',
        'composition': [
            {'name': 'Yeast Extract', 'description': 'Provides essential nutrients'},
            {'name': 'Activated Charcoal', 'description': 'Detoxifies peroxides and reactive compounds'},
            {'name': 'L-Cysteine', 'description': 'Essential for Legionella growth'},
            {'name': 'Ferric Pyrophosphate', 'description': 'Essential for Legionella growth'},
            {'name': 'α-Ketoglutarate', 'description': 'Enhances Legionella proliferation'},
            {'name': 'Optional Antibiotics', 'description': 'Polymyxin B, anisomycin, vancomycin to suppress competing flora'}
        ],
        'characteristics': [
            'Appears black or dark gray due to activated charcoal',
            'Supports the growth of fastidious Legionella species, which do not grow on standard media',
            'Can be non-selective or selective depending on whether antibiotics are added'
        ],
        'common_uses': [
            'Isolation of Legionella pneumophila from respiratory specimens (e.g., sputum, BAL)',
            'Detection of Legionella from environmental sources (e.g., water systems, cooling towers)',
            'Used in conjunction with serological or molecular methods for definitive identification'
        ],
        'special_notes': [
            'Does not differentiate Legionella species',
            'Requires prolonged incubation (3–7 days) at 35–37°C in a humidified atmosphere'
        ],
        'images': [
            {'src': '/static/images/plates/bcye/bcye_blank.jpg', 'caption': 'Uninoculated BCYE Agar plate'},
            {'src': '/static/images/plates/bcye/bcye_growth.jpg', 'caption': 'Legionella pneumophila growth on BCYE Agar'}
        ]
    },
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
            {'src': '/static/images/plates/mac/e_coli_mac_1.jpg', 'caption': 'E. coli on MacConkey Agar - Example 1'},
            {'src': '/static/images/plates/mac/e_coli_mac_2.jpg', 'caption': 'E. coli on MacConkey Agar - Example 2'},
            {'src': '/static/images/plates/mac/e_coli_mac_3.jpg', 'caption': 'E. coli on MacConkey Agar - Example 3'}
        ]
    },
    'chocolate_agar': {
        'name': 'Chocolate Agar',
        'type': 'Enriched Media',
        'purpose': 'Supports the growth of fastidious organisms, especially Haemophilus and Neisseria species',
        'composition': [
            {'name': 'Hemoglobin', 'description': 'Provides X factor (hemin) for growth'},
            {'name': 'NAD (V factor)', 'description': 'Essential for the growth of Haemophilus species'},
            {'name': 'Peptones', 'description': 'Provides nutrients for bacterial growth'},
            {'name': 'Agar', 'description': 'Solidifying agent'}
        ],
        'characteristics': [
            'Enriched with hemoglobin and NAD',
            'Brown color due to lysed red blood cells',
            'Supports growth of fastidious organisms'
        ],
        'common_uses': [
            'Isolation of Haemophilus influenzae',
            'Isolation of Neisseria gonorrhoeae',
            'Culturing of other fastidious organisms'
        ],
        'images': [
            {'src': '/static/images/plates/chocolate/choc_growth1.jpg', 'caption': 'Growth pattern on Chocolate Agar - Example 1'},
            {'src': '/static/images/plates/chocolate/choc_growth2.jpg', 'caption': 'Growth pattern on Chocolate Agar - Example 2'}
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
    },
    'modified_thayer_martin': {
        'name': 'Modified Thayer-Martin Agar',
        'type': 'Enrichment and Selective Media',
        'purpose': 'Isolation of N. gonorrhoeae and Neisseria meningitidis from specimens containing mixed microbiota',
        'composition': [
            {'name': 'Peptone Starch', 'description': 'Provides nutrients and growth factors'},
            {'name': 'Amino Acids', 'description': 'Essential for bacterial growth'},
            {'name': 'Glucose', 'description': 'Fermentable carbohydrate with lower concentration'},
            {'name': 'Nucleotides', 'description': 'Supports nucleic acid synthesis'},
            {'name': 'Chocolatized Blood', 'description': 'Enrichment component'},
            {'name': 'Trimethoprim', 'description': 'Inhibits Proteus spp. to prevent swarming'},
            {'name': 'Colistin', 'description': 'Inhibits other Gram-negative bacteria'},
            {'name': 'Vancomycin', 'description': 'Inhibits Gram-positive bacteria'},
            {'name': 'Nystatin', 'description': 'Inhibits yeast'}
        ],
        'characteristics': [
            'Lower glucose and agar concentrations improve growth of fastidious organisms',
            'Selective capacity due to added antibiotics'
        ],
        'common_uses': [
            'Isolation of N. gonorrhoeae',
            'Isolation of Neisseria meningitidis'
        ],
        'special_notes': [
            'Martin-Lewis agar substitutes ansamycin for nystatin and has a higher concentration of vancomycin'
        ]
    },
    'ccfa': {
        'name': 'Cycloserine Cefoxitin Fructose Agar (CCFA)',
        'type': 'Selective and Differential Media',
        'purpose': 'Isolation and identification of Clostridioides difficile from fecal specimens',
        'composition': [
            {'name': 'Fructose', 'description': 'Main carbohydrate for fermentation by C. difficile'},
            {'name': 'Neutral Red Indicator', 'description': 'Detects acid production from fructose fermentation (color change)'},
            {'name': 'Cycloserine', 'description': 'Inhibits Gram-negative bacteria'},
            {'name': 'Cefoxitin', 'description': 'Inhibits most Gram-positive bacteria (except C. difficile)'},
            {'name': 'Agar Base', 'description': 'Provides nutrients and support for bacterial growth'}
        ],
        'characteristics': [
            'C. difficile ferments fructose, producing acid which turns the medium yellow',
            'Colonies appear yellow, irregular, and have a characteristic horse manure-like odor',
            'Not completely specific for C. difficile - further confirmation required',
            'Requires toxigenic testing (PCR, ELISA for toxins A & B) for confirmation'
        ],
        'common_uses': [
            'Primary isolation of C. difficile from stool samples in suspected pseudomembranous colitis',
            'Isolation in cases of C. difficile infection (CDI)',
            'Differentiation of C. difficile from other Clostridium species based on fructose fermentation and antibiotic resistance'
        ],
        'special_notes': [
            'Some non-C. difficile Clostridium species may also grow',
            'Does not differentiate toxigenic from non-toxigenic strains—additional testing needed for toxin detection',
            'CCFA has largely been replaced by chromogenic media and molecular methods'
        ]
    },
    'xld': {
        'name': 'Xylose-Lysine-Deoxycholate (XLD) Agar',
        'type': 'Selective and Differential Media',
        'purpose': 'Used for the isolation and differentiation of Shigella species and Salmonella species from other non-pathogenic enteric bacteria',
        'composition': [
            {'name': 'Sodium Deoxycholate', 'description': 'Selective agent that inhibits gram-positive organisms and many non-enteric gram-negative bacilli'},
            {'name': 'Xylose', 'description': 'Fermentable carbohydrate for differentiation'},
            {'name': 'Lysine', 'description': 'Amino acid for detecting lysine decarboxylation'},
            {'name': 'Lactose and Sucrose', 'description': 'Additional fermentable carbohydrates for differentiation'},
            {'name': 'Phenol Red', 'description': 'pH indicator that detects acid production from carbohydrate fermentation'},
            {'name': 'Sodium Thiosulfate and Ferric Ammonium Citrate', 'description': 'H₂S indicator system'},
            {'name': 'Agar Base', 'description': 'Solidifying agent'}
        ],
        'characteristics': [
            'Base medium appears pink to red in color',
            'Differential characteristics based on:',
            '- Carbohydrate fermentation (xylose, lactose, sucrose)',
            '- Lysine decarboxylation',
            '- H₂S production',
            'Colony appearances:',
            '- Shigella spp.: Colorless colonies (red, same as medium)',
            '- Salmonella spp.: Colorless colonies with black centers (H₂S production)',
            '- Non-pathogenic fermenters: Yellow colonies'
        ],
        'common_uses': [
            'Isolation and identification of Shigella species',
            'Isolation and identification of Salmonella species',
            'Differentiation of pathogenic enteric bacteria from non-pathogenic organisms',
            'Processing of stool specimens for enteric pathogens'
        ],
        'special_notes': [
            'Salmonella colonies remain colorless despite xylose fermentation due to lysine decarboxylation raising pH',
            'Black center in Salmonella colonies is due to H₂S production',
            'Yellow colonies typically indicate non-pathogenic organisms that ferment one or more of the carbohydrates'
        ],
        'images': [
            {'src': '/static/images/plates/xld/xld_blank.jpg', 'caption': 'Uninoculated XLD Agar plate'},
            {'src': '/static/images/plates/xld/xld_salmonella.jpg', 'caption': 'Salmonella species showing characteristic black-centered colonies'},
            {'src': '/static/images/plates/xld/xld_shigella.jpg', 'caption': 'Shigella species showing colorless colonies'}
        ]
    },
    'sab_dex': {
        'name': 'Sabouraud Dextrose Agar (SDA)',
        'type': 'General Purpose & Selective Medium',
        'purpose': 'Used for the isolation and cultivation of fungi, including yeasts and molds, and supports the growth of dermatophytes, Candida species, and other pathogenic/non-pathogenic fungi',
        'composition': [
            {'name': 'Dextrose (40g/L)', 'description': 'Provides a rich carbohydrate source to support fungal growth'},
            {'name': 'Peptones (10g/L)', 'description': 'Supply nitrogen, vitamins, and amino acids for fungal metabolism'},
            {'name': 'Agar (15g/L)', 'description': 'Solidifying agent'},
            {'name': 'pH Adjustment', 'description': 'Low pH (5.6) inhibits bacterial growth while promoting fungal growth'},
            {'name': 'Optional Antibiotics', 'description': 'Chloramphenicol or Gentamicin can be added in selective formulations to suppress bacterial contamination'}
        ],
        'characteristics': [
            'Appears pale yellow to light amber before inoculation',
            'Fungi grow as filamentous colonies (molds) or creamy, smooth colonies (yeasts)',
            'Supports a broad range of fungal species, including:',
            '- Candida spp. (e.g., C. albicans, C. glabrata, C. krusei)',
            '- Aspergillus spp.',
            '- Trichophyton spp. (causes dermatophytosis)',
            '- Microsporum spp.',
            '- Epidermophyton spp.'
        ],
        'common_uses': [
            'Primary isolation of yeasts and molds from clinical specimens (skin, nails, sputum, vaginal swabs)',
            'Diagnosis of fungal infections, including dermatophytosis, candidiasis, and systemic mycoses',
            'Environmental and food microbiology applications for detecting fungal contaminants'
        ],
        'limitations': [
            'Non-specific for Candida identification (CHROMagar Candida is preferred for species differentiation)',
            'May not fully inhibit bacterial growth unless antibiotics are added',
            'Slow-growing fungi may require prolonged incubation (up to 4 weeks at 25–30°C)'
        ],
        'images': [
            {'src': '/static/images/plates/sab_dex/sda_blank.jpg', 'caption': 'Uninoculated Sabouraud Dextrose Agar plate'},
            {'src': '/static/images/plates/sab_dex/sda_candida.jpg', 'caption': 'Candida species growth showing typical yeast colonies'},
            {'src': '/static/images/plates/sab_dex/sda_mold.jpg', 'caption': 'Filamentous fungal growth on SDA'}
        ]
    },
    'chromagar_candida': {
        'name': 'CHROMagar Candida',
        'type': 'Selective and Differential Medium',
        'purpose': 'Used for the isolation, differentiation, and presumptive identification of Candida species based on colony color resulting from enzymatic reactions with chromogenic substrates',
        'composition': [
            {'name': 'Peptones', 'description': 'Provide essential nutrients for fungal growth'},
            {'name': 'Chromogenic Substrates', 'description': 'React with species-specific enzymes to produce characteristic colony colors'},
            {'name': 'Chloramphenicol', 'description': 'Inhibits bacterial growth, ensuring fungal isolation'},
            {'name': 'Agar Base', 'description': 'Solidifying agent to support colony formation'}
        ],
        'characteristics': [
            'Appears light pink before inoculation',
            'Different Candida species produce distinct colony colors:',
            '- C. albicans: Green colonies',
            '- C. tropicalis: Blue to metallic blue colonies',
            '- C. krusei: Pink, fuzzy colonies',
            '- C. glabrata: Pale to purple colonies',
            '- C. parapsilosis: Off-white to pale pink colonies',
            'Rapid differentiation within 24–48 hours of incubation',
            'Reduces the need for additional biochemical tests like germ tube test or sugar assimilation tests'
        ],
        'common_uses': [
            'Primary isolation of Candida species from clinical samples (e.g., urine, blood, sputum, vaginal swabs)',
            'Differentiation of major Candida species without molecular testing',
            'Guiding antifungal therapy, as species like C. krusei and C. glabrata may exhibit fluconazole resistance'
        ],
        'images': [
            {'src': '/static/images/plates/chromagar/chrom_blank.jpg', 'caption': 'Uninoculated CHROMagar Candida plate'},
            {'src': '/static/images/plates/chromagar/chrom_mixed.jpg', 'caption': 'Mixed Candida species showing characteristic colors'},
            {'src': '/static/images/plates/chromagar/chrom_albicans.jpg', 'caption': 'C. albicans showing characteristic green colonies'}
        ]
    }
}

# Growth results for all organism-media combinations
GROWTH_RESULTS = {
    'e_coli': {
        'mac_conkey': {'result': 'GOOD', 'description': 'Pink colonies (lactose fermenter)'},
        'emb': {'result': 'GOOD', 'description': 'Metallic green sheen (vigorous lactose fermenter)'},
        'blood_agar': {'result': 'GOOD', 'description': 'Gray, non-hemolytic or beta-hemolytic colonies'},
        'sab_dex': {'result': 'POOR', 'description': 'Poor or minimal growth. SDA is not recommended for E. coli because: 1) The acidic pH (5.6) inhibits bacterial growth, 2) The medium lacks essential nutrients for bacterial metabolism, 3) SDA is specifically designed for fungi, not bacteria'},
        'chocolate_agar': {'result': 'GOOD', 'description': 'Good growth due to enriched medium'},
        'default': {'result': 'VARIABLE', 'description': 'Growth may be variable. MacConkey or EMB Agar recommended for optimal isolation and identification of E. coli. These media provide selective pressure against Gram-positive organisms and differentiate lactose fermenters.'}
    },
    's_aureus': {
        'mannitol_salt': {'result': 'GOOD', 'description': 'Yellow colonies (ferments mannitol, turning the agar yellow)'},
        'blood_agar': {'result': 'GOOD', 'description': 'Beta-hemolysis (clear zones around colonies)'},
        'mac_conkey': {'result': 'POOR', 'description': 'No growth expected. MacConkey agar contains bile salts and crystal violet which inhibit Gram-positive organisms like S. aureus. This selective pressure is specifically designed to prevent growth of Gram-positive bacteria.'},
        'emb': {'result': 'POOR', 'description': 'No growth expected. EMB agar contains selective agents (eosin Y and methylene blue) that inhibit Gram-positive organisms like S. aureus. The medium is designed for Gram-negative bacteria only.'},
        'chocolate_agar': {'result': 'GOOD', 'description': 'Good growth with typical golden pigmentation'},
        'default': {'result': 'VARIABLE', 'description': 'Growth may be variable. Mannitol Salt Agar or Blood Agar recommended as they support S. aureus growth and provide diagnostic characteristics (mannitol fermentation and hemolysis respectively).'}
    },
    's_pneumoniae': {
        'blood_agar': {'result': 'GOOD', 'description': 'Alpha-hemolysis (greenish discoloration around colonies)'},
        'chocolate_agar': {'result': 'GOOD', 'description': 'Good growth (no hemolysis visible due to lysed RBCs)'},
        'mac_conkey': {'result': 'POOR', 'description': 'No growth expected. S. pneumoniae is a Gram-positive organism and is inhibited by the bile salts and crystal violet in MacConkey agar. Additionally, this fastidious organism requires enriched media for growth.'},
        'emb': {'result': 'POOR', 'description': 'No growth expected. EMB agar contains inhibitors of Gram-positive bacteria and lacks the enrichment factors required by S. pneumoniae. This fastidious organism needs blood-based media for growth.'},
        'thayer_martin': {'result': 'POOR', 'description': 'Poor or no growth expected. While Modified Thayer-Martin agar contains enriched nutrients from chocolatized blood, it also contains antibiotics (vancomycin) that inhibit Gram-positive organisms like S. pneumoniae. Blood Agar is recommended as it provides both necessary nutrients and allows observation of characteristic alpha-hemolysis.'},
        'default': {'result': 'POOR', 'description': 'Poor growth expected. S. pneumoniae requires enriched media (particularly blood-based) for growth due to its fastidious nature. Blood Agar is recommended as it provides both necessary nutrients and allows observation of characteristic alpha-hemolysis.'}
    },
    'h_influenzae': {
        'chocolate_agar': {'result': 'GOOD', 'description': 'Small, smooth, grayish colonies (requires factor V and X)'},
        'blood_agar': {'result': 'POOR', 'description': 'No growth unless streaked with S. aureus (satellite growth). H. influenzae requires both X (hemin) and V (NAD) factors. While blood agar provides X factor, the V factor is not readily available unless released by other bacteria.'},
        'mac_conkey': {'result': 'POOR', 'description': 'No growth expected. H. influenzae is a fastidious organism requiring X and V factors for growth. MacConkey agar lacks these essential growth factors and contains inhibitory compounds.'},
        'emb': {'result': 'POOR', 'description': 'No growth expected. EMB agar lacks the X and V factors required for H. influenzae growth. This fastidious organism cannot grow without these essential nutrients.'},
        'default': {'result': 'POOR', 'description': 'Poor or no growth expected. H. influenzae requires both X (hemin) and V (NAD) factors for growth. Chocolate Agar is recommended as it provides both factors through the heating of blood, making them readily available.'}
    },
    'l_pneumophila': {
        'bcye': {'result': 'GOOD', 'description': 'Grayish-white or blue-green colonies after 3-5 days'},
        'blood_agar': {'result': 'POOR', 'description': 'No growth expected. L. pneumophila has specific growth requirements including L-cysteine and iron salts, which are not present in blood agar. The organism cannot synthesize cysteine and requires it for growth.'},
        'mac_conkey': {'result': 'POOR', 'description': 'No growth expected. L. pneumophila requires L-cysteine and iron salts for growth, which are absent in MacConkey agar. Additionally, the medium lacks the buffering capacity needed for Legionella growth.'},
        'chocolate_agar': {'result': 'POOR', 'description': 'No growth expected. Despite being an enriched medium, chocolate agar lacks the specific requirements (L-cysteine and iron salts) essential for L. pneumophila growth.'},
        'default': {'result': 'POOR', 'description': 'No growth expected. L. pneumophila requires a specialized medium (BCYE) containing L-cysteine, iron salts, and activated charcoal. The organism cannot grow without these specific nutrients and environmental conditions.'}
    },
    'n_gonorrhoeae': {
        'thayer_martin': {'result': 'GOOD', 'description': 'Small, gray, translucent colonies'},
        'chocolate_agar': {'result': 'GOOD', 'description': 'Gray, sticky, smooth colonies'},
        'blood_agar': {'result': 'POOR', 'description': 'Poor or no growth expected. N. gonorrhoeae is extremely fastidious and requires enriched media with specific growth factors. Blood agar lacks the optimal concentration of nutrients and growth factors needed.'},
        'mac_conkey': {'result': 'POOR', 'description': 'No growth expected. N. gonorrhoeae is highly fastidious and cannot grow on MacConkey agar due to its basic nutritional requirements not being met. The medium also contains inhibitory compounds.'},
        'default': {'result': 'POOR', 'description': 'Poor or no growth expected. N. gonorrhoeae requires specialized media (Modified Thayer-Martin or Chocolate Agar) due to its fastidious nature. These media provide essential growth factors and, in the case of MTM, selective agents to inhibit competing flora.'}
    },
    'p_aeruginosa': {
        'mac_conkey': {'result': 'GOOD', 'description': 'Colorless colonies (non-lactose fermenter)'},
        'mueller_hinton': {'result': 'GOOD', 'description': 'Produces blue-green pigment (pyocyanin)'},
        'blood_agar': {'result': 'GOOD', 'description': 'Beta-hemolysis (clear zones around colonies)'},
        'emb': {'result': 'GOOD', 'description': 'Colorless colonies, sometimes metallic sheen'},
        'default': {'result': 'VARIABLE', 'description': 'Growth may be variable. MacConkey or Mueller Hinton Agar recommended'}
    },
    'aspergillus': {
        'sab_dex': {'result': 'GOOD', 'description': 'White, then turning black/green/yellow (depending on species) with surface mycelia'},
        'blood_agar': {'result': 'POOR', 'description': 'Poor or no growth expected. Blood agar has a neutral pH and lacks the high glucose concentration needed for optimal fungal growth. Additionally, faster-growing bacteria may overgrow any fungal colonies.'},
        'mac_conkey': {'result': 'POOR', 'description': 'No growth expected. MacConkey agar lacks appropriate nutrients for fungal growth and contains compounds that may inhibit fungal development.'},
        'default': {'result': 'POOR', 'description': 'Poor or no growth expected. Aspergillus species require acidic pH and high glucose concentration for optimal growth. Sabouraud Dextrose Agar is recommended as it provides these conditions and inhibits bacterial growth.'}
    },
    'c_albicans': {
        'chrom_agar': {'result': 'GOOD', 'description': 'Green colonies'},
        'sab_dex': {'result': 'GOOD', 'description': 'Creamy white colonies, smooth and pasty'},
        'blood_agar': {'result': 'VARIABLE', 'description': 'Variable growth. While C. albicans can grow on blood agar, it is not optimal because: 1) The neutral pH does not suppress bacterial contamination, 2) The medium lacks the high glucose concentration preferred by yeasts, 3) Morphological features may be harder to observe.'},
        'mac_conkey': {'result': 'POOR', 'description': 'Poor or no growth expected. MacConkey agar contains bile salts and crystal violet which can inhibit fungal growth. The medium also lacks the nutrients required for proper fungal development.'},
        'default': {'result': 'VARIABLE', 'description': 'Growth may be variable. CHROMagar or Sabouraud Dextrose Agar recommended as they provide optimal conditions for fungal growth and allow for better identification. SDA\'s acidic pH and high glucose content favor fungal growth while inhibiting bacteria.'}
    },
    'c_auris': {
        'chrom_agar': {'result': 'GOOD', 'description': 'Pink or mauve colonies (varies by formulation)'},
        'sab_dex': {'result': 'GOOD', 'description': 'Creamy white colonies, often dry and wrinkled'},
        'blood_agar': {'result': 'VARIABLE', 'description': 'Variable growth. While C. auris can grow on blood agar, it is not optimal because: 1) The neutral pH allows bacterial overgrowth, 2) The medium lacks the high glucose concentration needed for optimal growth, 3) Colony morphology may be atypical.'},
        'mac_conkey': {'result': 'POOR', 'description': 'Poor or no growth expected. MacConkey agar contains inhibitory compounds and lacks the necessary nutrients for fungal growth.'},
        'default': {'result': 'VARIABLE', 'description': 'Growth may be variable. CHROMagar or Sabouraud Dextrose Agar recommended as they provide optimal conditions for fungal growth and facilitate proper identification. These media offer selective pressure against bacteria and support characteristic colony development.'}
    },
    'k_pneumoniae': {
        'mac_conkey': {'result': 'GOOD', 'description': 'Large, mucoid pink colonies (lactose fermenter)'},
        'emb': {'result': 'GOOD', 'description': 'Large, mucoid colonies with dark centers'},
        'blood_agar': {'result': 'GOOD', 'description': 'Large, grayish-white mucoid colonies'},
        'chocolate_agar': {'result': 'VARIABLE', 'description': 'While growth is possible, chocolate agar is not recommended for primary isolation. MacConkey or EMB agar are preferred as they allow better differentiation of K. pneumoniae based on lactose fermentation and colony characteristics.', 'note': 'For optimal isolation and identification, use MacConkey Agar (shows lactose fermentation) or EMB Agar (shows mucoid colonies with dark centers).'},
        'sab_dex': {
            'result': 'UNKNOWN',
            'description': 'Growth characteristics are not well-documented for this combination.',
            'note': 'Sabouraud Dextrose Agar is designed for fungal isolation and is not routinely used for Klebsiella pneumoniae. The recommended medium for this organism is MacConkey Agar, where it grows as mucoid pink colonies (lactose fermentation positive).'
        },
        'default': {
            'result': 'UNKNOWN',
            'description': 'Growth characteristics are not well-documented for this combination.',
            'note': 'For optimal isolation and identification of Klebsiella pneumoniae, use MacConkey Agar (shows lactose fermentation) or EMB Agar (shows mucoid colonies with dark centers).'
        }
    },
    'c_difficile': {
        'ccfa': {
            'result': 'GOOD',
            'description': 'Yellow, irregular colonies with characteristic horse manure-like odor after 24-48 hours of anaerobic incubation.',
            'note': 'CCFA is the selective medium of choice for C. difficile isolation. The medium contains cycloserine and cefoxitin to inhibit other organisms while allowing C. difficile growth.'
        },
        'blood_agar': {
            'result': 'VARIABLE',
            'description': 'Growth possible but not recommended due to overgrowth by other organisms.',
            'note': 'Blood agar lacks selective agents needed to inhibit competing flora. CCFA is the recommended medium for isolation.'
        },
        'sab_dex': {
            'result': 'POOR',
            'description': 'Poor or no growth expected.',
            'note': 'C. difficile is an obligate anaerobe and requires selective media like CCFA (Cycloserine-Cefoxitin Fructose Agar) for optimal isolation. SDA is not suitable because: 1) Low pH (~5.6) inhibits bacterial growth, especially obligate anaerobes, 2) Lacks selective antibiotics (cycloserine, cefoxitin) required to suppress competing flora, 3) Aerobic incubation conditions inhibit C. difficile, which requires an anaerobic environment.'
        },
        'default': {
            'result': 'POOR',
            'description': 'Poor or no growth expected.',
            'note': 'C. difficile requires selective media (CCFA) for isolation from clinical specimens. CCFA contains cycloserine and cefoxitin to inhibit competing flora while allowing C. difficile to grow.'
        }
    },
    'a_baumannii': {
        'blood_agar': {'result': 'GOOD', 'description': 'Smooth, dome-shaped colonies with entire margins. White to cream-colored, opaque, 1.5-2.5 mm in diameter after 24 hours. Non-hemolytic.'},
        'mac_conkey': {'result': 'GOOD', 'description': 'Smooth, slightly domed colonies. Pink to mauve (non-lactose fermenter), 1-2 mm in diameter.'},
        'default': {'result': 'VARIABLE', 'description': 'Growth may be variable. Blood Agar or MacConkey Agar recommended for optimal isolation and identification of A. baumannii.'}
    }
}

# Organism name mappings
ORGANISM_NAMES = {
    's_pneumoniae': 'Streptococcus pneumoniae',
    'e_coli': 'Escherichia coli',
    's_aureus': 'Staphylococcus aureus',
    'p_aeruginosa': 'Pseudomonas aeruginosa',
    'k_pneumoniae': 'Klebsiella pneumoniae',
    'n_gonorrhoeae': 'Neisseria gonorrhoeae',
    'c_difficile': 'Clostridioides difficile',
    'h_influenzae': 'Haemophilus influenzae',
    'l_pneumophila': 'Legionella pneumophila',
    'aspergillus': 'Aspergillus species',
    'c_albicans': 'Candida albicans',
    'c_auris': 'Candida auris',
    'a_baumannii': 'Acinetobacter baumannii'
}

# Media name mappings
MEDIA_NAMES = {
    'blood_agar': 'Blood Agar',
    'mac_conkey': 'MacConkey Agar',
    'emb': 'EMB (Eosin Methylene Blue) Agar',
    'chocolate_agar': 'Chocolate Agar',
    'mueller_hinton': 'Mueller Hinton Agar',
    'mannitol_salt': 'Mannitol Salt Agar',
    'thayer_martin': 'Modified Thayer-Martin Agar',
    'ccfa': 'CCFA (Cycloserine-Cefoxitin Fructose Agar)',
    'bcye': 'BCYE Agar',
    'sab_dex': 'Sabouraud Dextrose Agar',
    'chrom_agar': 'CHROMagar Candida'
}

# Individual media dictionaries
blood_agar = {
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
    ]
}

mac_conkey = {
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
    ]
}

emb = {
    'name': 'Eosin Methylene Blue (EMB) Agar',
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
        'Selective against Gram-positive bacteria'
    ],
    'common_uses': [
        'Isolation and differentiation of Gram-negative bacteria',
        'Identification of lactose-fermenting organisms',
        'Detection of coliform bacteria (especially E. coli with its characteristic metallic sheen)'
    ]
}

chocolate_agar = {
    'name': 'Chocolate Agar',
    'type': 'Enriched Media',
    'purpose': 'Supports the growth of fastidious organisms, especially Haemophilus and Neisseria species',
    'composition': [
        {'name': 'Hemoglobin', 'description': 'Provides X factor (hemin) for growth'},
        {'name': 'NAD (V factor)', 'description': 'Essential for the growth of Haemophilus species'},
        {'name': 'Peptones', 'description': 'Provides nutrients for bacterial growth'},
        {'name': 'Agar', 'description': 'Solidifying agent'}
    ],
    'characteristics': [
        'Enriched with hemoglobin and NAD',
        'Brown color due to lysed red blood cells',
        'Supports growth of fastidious organisms'
    ],
    'common_uses': [
        'Isolation of Haemophilus influenzae',
        'Isolation of Neisseria gonorrhoeae',
        'Culturing of other fastidious organisms'
    ]
}

mueller_hinton = {
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
        'Quality control testing of antimicrobials'
    ]
}

mannitol_salt = {
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
        'Screening for pathogenic Staphylococci'
    ]
}

modified_thayer_martin = {
    'name': 'Modified Thayer-Martin Agar',
    'type': 'Enrichment and Selective Media',
    'purpose': 'Isolation of N. gonorrhoeae and Neisseria meningitidis from specimens containing mixed microbiota',
    'composition': [
        {'name': 'Peptone Starch', 'description': 'Provides nutrients and growth factors'},
        {'name': 'Amino Acids', 'description': 'Essential for bacterial growth'},
        {'name': 'Glucose', 'description': 'Fermentable carbohydrate with lower concentration'},
        {'name': 'Nucleotides', 'description': 'Supports nucleic acid synthesis'},
        {'name': 'Chocolatized Blood', 'description': 'Enrichment component'},
        {'name': 'Trimethoprim', 'description': 'Inhibits Proteus spp. to prevent swarming'},
        {'name': 'Colistin', 'description': 'Inhibits other Gram-negative bacteria'},
        {'name': 'Vancomycin', 'description': 'Inhibits Gram-positive bacteria'},
        {'name': 'Nystatin', 'description': 'Inhibits yeast'}
    ],
    'characteristics': [
        'Lower glucose and agar concentrations improve growth of fastidious organisms',
        'Selective capacity due to added antibiotics'
    ],
    'common_uses': [
        'Isolation of N. gonorrhoeae',
        'Isolation of Neisseria meningitidis'
    ]
}

ccfa = {
    'name': 'Cycloserine Cefoxitin Fructose Agar (CCFA)',
    'type': 'Selective and Differential Media',
    'purpose': 'Isolation and identification of Clostridioides difficile from fecal specimens',
    'composition': [
        {'name': 'Fructose', 'description': 'Main carbohydrate for fermentation by C. difficile'},
        {'name': 'Neutral Red Indicator', 'description': 'Detects acid production from fructose fermentation'},
        {'name': 'Cycloserine', 'description': 'Inhibits Gram-negative bacteria'},
        {'name': 'Cefoxitin', 'description': 'Inhibits most Gram-positive bacteria (except C. difficile)'},
        {'name': 'Agar Base', 'description': 'Provides nutrients and support for bacterial growth'}
    ],
    'characteristics': [
        'C. difficile ferments fructose, producing acid which turns the medium yellow',
        'Colonies appear yellow, irregular, and have a characteristic horse manure-like odor',
        'Not completely specific for C. difficile - further confirmation required'
    ],
    'common_uses': [
        'Primary isolation of C. difficile from stool samples',
        'Isolation in cases of C. difficile infection (CDI)',
        'Differentiation of C. difficile from other Clostridium species'
    ]
}

bcye = {
    'name': 'Buffered Charcoal Yeast Extract (BCYE) Agar',
    'type': 'Selective and Enriched Medium',
    'purpose': 'Used for the isolation of Legionella species, particularly Legionella pneumophila',
    'composition': [
        {'name': 'Yeast Extract', 'description': 'Provides essential nutrients'},
        {'name': 'Activated Charcoal', 'description': 'Detoxifies peroxides and reactive compounds'},
        {'name': 'L-Cysteine', 'description': 'Essential for Legionella growth'},
        {'name': 'Ferric Pyrophosphate', 'description': 'Essential for Legionella growth'},
        {'name': 'α-Ketoglutarate', 'description': 'Enhances Legionella proliferation'}
    ],
    'characteristics': [
        'Appears black or dark gray due to activated charcoal',
        'Supports the growth of fastidious Legionella species',
        'Can be non-selective or selective depending on whether antibiotics are added'
    ],
    'common_uses': [
        'Isolation of Legionella pneumophila from respiratory specimens',
        'Detection of Legionella from environmental sources',
        'Used in conjunction with serological or molecular methods for identification'
    ]
}

sab_dex = {
    'name': 'Sabouraud Dextrose Agar (SDA)',
    'type': 'General Purpose & Selective Medium',
    'purpose': 'Used for the isolation and cultivation of fungi, including yeasts and molds',
    'composition': [
        {'name': 'Dextrose (40g/L)', 'description': 'Provides a rich carbohydrate source'},
        {'name': 'Peptones (10g/L)', 'description': 'Supply nitrogen, vitamins, and amino acids'},
        {'name': 'Agar (15g/L)', 'description': 'Solidifying agent'},
        {'name': 'pH Adjustment', 'description': 'Low pH (5.6) inhibits bacterial growth'}
    ],
    'characteristics': [
        'Appears pale yellow to light amber before inoculation',
        'Fungi grow as filamentous colonies (molds) or creamy, smooth colonies (yeasts)',
        'Supports a broad range of fungal species'
    ],
    'common_uses': [
        'Primary isolation of yeasts and molds from clinical specimens',
        'Diagnosis of fungal infections',
        'Environmental and food microbiology applications'
    ]
}

chromagar_candida = {
    'name': 'CHROMagar Candida',
    'type': 'Selective and Differential Medium',
    'purpose': 'Used for the isolation and differentiation of Candida species',
    'composition': [
        {'name': 'Peptones', 'description': 'Provide essential nutrients for fungal growth'},
        {'name': 'Chromogenic Substrates', 'description': 'React with species-specific enzymes'},
        {'name': 'Chloramphenicol', 'description': 'Inhibits bacterial growth'},
        {'name': 'Agar Base', 'description': 'Solidifying agent'}
    ],
    'characteristics': [
        'Appears light pink before inoculation',
        'Different Candida species produce distinct colony colors',
        'Rapid differentiation within 24–48 hours'
    ],
    'common_uses': [
        'Primary isolation of Candida species from clinical samples',
        'Differentiation of major Candida species',
        'Guiding antifungal therapy'
    ]
}

xld = {
    'name': 'Xylose-Lysine-Deoxycholate (XLD) Agar',
    'type': 'Selective and Differential Media',
    'purpose': 'Used for the isolation and differentiation of Shigella and Salmonella species',
    'composition': [
        {'name': 'Sodium Deoxycholate', 'description': 'Selective agent that inhibits gram-positive organisms'},
        {'name': 'Xylose', 'description': 'Fermentable carbohydrate for differentiation'},
        {'name': 'Lysine', 'description': 'Amino acid for detecting lysine decarboxylation'},
        {'name': 'Lactose and Sucrose', 'description': 'Additional fermentable carbohydrates'},
        {'name': 'Phenol Red', 'description': 'pH indicator'},
        {'name': 'Sodium Thiosulfate and Ferric Ammonium Citrate', 'description': 'H₂S indicator system'}
    ],
    'characteristics': [
        'Base medium appears pink to red in color',
        'Differential characteristics based on carbohydrate fermentation and H₂S production',
        'Shigella: Colorless colonies',
        'Salmonella: Colorless colonies with black centers'
    ],
    'common_uses': [
        'Isolation and identification of Shigella species',
        'Isolation and identification of Salmonella species',
        'Processing of stool specimens for enteric pathogens'
    ]
}

# Consolidated media information dictionary
MEDIA_INFO = {
    'blood_agar': blood_agar,
    'mac_conkey': mac_conkey,
    'emb': emb,
    'chocolate_agar': chocolate_agar,
    'mueller_hinton': mueller_hinton,
    'mannitol_salt': mannitol_salt,
    'modified_thayer_martin': modified_thayer_martin,
    'ccfa': ccfa,
    'bcye': bcye,
    'sab_dex': sab_dex,
    'chromagar_candida': chromagar_candida,
    'xld': xld
}

def get_images_from_directory(media_type):
    """
    Scans the plates directory for images related to a specific media type.
    Returns a list of dictionaries containing image information.
    """
    base_path = os.path.join('app', 'static', 'images', 'plates', media_type)
    images = []
    
    if os.path.exists(base_path):
        for filename in os.listdir(base_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.jfif')):
                # Convert filename to title by:
                # 1. Remove extension
                # 2. Replace underscores and hyphens with spaces
                # 3. Title case the result
                caption = os.path.splitext(filename)[0]  # Remove extension
                caption = caption.replace('_', ' ').replace('-', ' ')  # Replace separators
                caption = caption.title()  # Convert to title case
                
                images.append({
                    'src': f'/static/images/plates/{media_type}/{filename}',
                    'caption': caption
                })
    
    return images

# Replace the static MEDIA_EXAMPLE_IMAGES with a dynamic function
def get_media_example_images():
    """
    Dynamically generates the MEDIA_EXAMPLE_IMAGES dictionary based on directory contents.
    """
    media_images = {}
    plates_dir = os.path.join('app', 'static', 'images', 'plates')
    
    if os.path.exists(plates_dir):
        for media_type in os.listdir(plates_dir):
            if os.path.isdir(os.path.join(plates_dir, media_type)):
                images = get_images_from_directory(media_type)
                if images:  # Only add to dictionary if images were found
                    media_images[media_type] = images
    
    return media_images

def get_organism_images(organism, media_type=None):
    """
    Scans the organisms directory for images related to a specific organism.
    If media_type is provided, returns only images from that media type's subfolder.
    Returns a list of dictionaries containing image information.
    """
    images = []
    
    # Base path for the organism
    base_path = os.path.join('app', 'static', 'images', 'organisms', organism)
    
    if not os.path.exists(base_path):
        return images
    
    if media_type:
        # Look for images in the media-specific subfolder
        media_path = os.path.join(base_path, media_type)
        if os.path.exists(media_path):
            for filename in os.listdir(media_path):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.jfif')):
                    caption = os.path.splitext(filename)[0]
                    caption = caption.replace('_', ' ').replace('-', ' ')
                    caption = caption.title()
                    
                    images.append({
                        'src': f'/static/images/organisms/{organism}/{media_type}/{filename}',
                        'caption': caption
                    })
    
    return images

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        organism = request.form.get('organism')
        media = request.form.get('media')
        
        # Get full names for organism and media
        organism_name = ORGANISM_NAMES.get(organism, organism)
        media_name = MEDIA_NAMES.get(media, media)
        
        # Get organism-specific tests and growth characteristics
        confirmatory_tests = CONFIRMATORY_TESTS_DATA.get(organism, {})
        characteristics = growth_characteristics.get(organism, {}).get(media, {})
        
        # Get media information
        media_info = MEDIA_INFO.get(media, {})
        
        # Get growth results for the organism-media combination
        default_result = {
            'result': 'UNKNOWN',
            'description': 'Growth characteristics are not well-documented for this combination.',
            'note': f'This combination is not routinely used in clinical microbiology. Please refer to standard media recommendations for {organism_name}.'
        }
        
        organism_results = GROWTH_RESULTS.get(organism, {})
        growth_result = organism_results.get(media, organism_results.get('default', default_result))
        
        # Get images from the organism's media-specific folder only
        all_images = get_organism_images(organism, media)
        
        return render_template('results.html',
                             organism=organism,
                             organism_name=organism_name,
                             media=media,
                             media_name=media_name,
                             confirmatory_tests=confirmatory_tests,
                             characteristics=characteristics,
                             plate_images=all_images,
                             growth_result=growth_result,
                             media_info=media_info)
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
    print(f"Media ID: {media_id}")  # Debug print
    
    # Handle different media ID formats
    media_id_mappings = {
        'chrom_agar': 'chromagar_candida',
        'thayer_martin': 'modified_thayer_martin'
    }
    
    # Try to get the standardized media ID
    standardized_media_id = media_id_mappings.get(media_id, media_id)
    
    if standardized_media_id not in MEDIA_INFO:
        flash(f'Media type "{media_id}" not found in database', 'error')
        return redirect(url_for('main.media_search'))
    
    media_data = MEDIA_INFO[standardized_media_id]
    
    # Get example images dynamically from the directory
    example_images = get_images_from_directory(media_id)  # Use original media_id for image lookup
    
    return render_template('media_info.html',
                         media_name=media_data['name'],
                         media_type=media_data['type'],
                         purpose=media_data['purpose'],
                         composition=media_data['composition'],
                         characteristics=media_data['characteristics'],
                         common_uses=media_data['common_uses'],
                         dynamic_images=example_images)