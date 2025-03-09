// Media recommendations data
const mediaRecommendations = {
    e_coli: [
        {
            name: 'MacConkey Agar',
            value: 'mac_conkey',
            reason: 'Primary choice for isolating gram-negative enteric bacteria. E. coli will appear as pink colonies due to lactose fermentation.',
            composition: 'Contains bile salts and crystal violet (inhibits gram-positive bacteria), lactose (fermented by E. coli), and neutral red indicator (turns pink in acid conditions). The selective ingredients allow only gram-negative bacteria to grow while differentiating lactose fermenters (pink) from non-fermenters (colorless).',
            priority: 1
        },
        {
            name: 'EMB Agar',
            value: 'emb',
            reason: 'Differential medium where E. coli produces distinctive metallic green sheen colonies.',
            composition: 'Contains Eosin Y and Methylene Blue dyes which inhibit gram-positive bacteria and indicate acid production from lactose/sucrose fermentation. E. coli produces strong acid, causing the dyes to precipitate and create a distinctive green metallic sheen. Also contains lactose and sucrose as fermentable carbohydrates.',
            priority: 1
        },
        {
            name: 'Blood Agar',
            value: 'blood_agar',
            reason: 'Can be used to observe hemolysis patterns, though not primary choice for E. coli.',
            composition: 'Contains 5% sheep blood in nutrient agar base. Rich medium supporting growth of most bacteria. Allows visualization of hemolysis patterns: E. coli typically shows alpha or gamma hemolysis.',
            priority: 2
        },
        {
            name: 'Chocolate Agar',
            value: 'chocolate_agar',
            reason: 'Provides excellent growth with X and V factors',
            composition: 'Made from heated blood, releasing growth factors',
            priority: 'medium'
        }
    ],
    's_pneumoniae': [
        {
            name: 'Blood Agar',
            value: 'blood_agar',
            reason: 'Primary choice for S. pneumoniae. Shows characteristic alpha-hemolysis (green zone) around colonies.',
            composition: 'Contains 5% sheep blood in nutrient agar base. S. pneumoniae produces alpha-hemolysis (green zone) due to partial breakdown of hemoglobin to methemoglobin, creating the characteristic "draughtsman" colonies.',
            priority: 1
        },
        {
            name: 'Chocolate Agar',
            value: 'chocolate_agar',
            reason: 'Excellent growth medium due to X and V factors from heated blood.',
            composition: 'Contains heated blood which releases essential growth factors. The heat-treated blood provides nutrients required for optimal growth of S. pneumoniae.',
            priority: 1
        },
        {
            name: 'Mueller-Hinton Agar',
            value: 'mueller_hinton',
            reason: 'Used for susceptibility testing when supplemented with blood.',
            composition: 'When supplemented with 5% sheep blood, provides necessary growth factors and allows clear visualization of growth patterns.',
            priority: 2
        }
    ],
    s_aureus: [
        {
            name: 'Mannitol Salt Agar',
            value: 'mannitol_salt',
            reason: 'Selective and differential medium for S. aureus. Shows yellow colonies due to mannitol fermentation.',
            composition: 'Contains 7.5% NaCl (selects for halophilic bacteria), mannitol (fermented by S. aureus), and phenol red indicator. The high salt concentration inhibits most bacteria except Staphylococci. S. aureus ferments mannitol, producing acid that turns the phenol red indicator yellow.',
            priority: 1
        },
        {
            name: 'Blood Agar',
            value: 'blood_agar',
            reason: 'Excellent for observing beta-hemolysis pattern characteristic of S. aureus.',
            composition: 'Contains 5% sheep blood in nutrient agar base. S. aureus typically shows clear beta-hemolysis due to production of multiple hemolysins (alpha, beta, delta, and gamma). The clear zone around colonies indicates complete lysis of red blood cells.',
            priority: 1
        },
        {
            name: 'Chocolate Agar',
            value: 'chocolate_agar',
            reason: 'Supports growth with typical pigmentation',
            composition: 'Heat-treated blood providing essential growth factors',
            priority: 'medium'
        }
    ],
    p_aeruginosa: [
        {
            name: 'Mueller-Hinton Agar',
            value: 'mueller_hinton',
            reason: 'Ideal for observing characteristic blue-green pigment production.',
            composition: 'Contains beef infusion, casein hydrolysate, and starch. The low thymine/thymidine content and appropriate cation levels make it ideal for P. aeruginosa growth. The medium\'s composition enhances production of pyocyanin (blue-green) and pyoverdin (fluorescent yellow-green) pigments.',
            priority: 1
        },
        {
            name: 'Blood Agar',
            value: 'blood_agar',
            reason: 'Shows characteristic spreading growth and pigment production.',
            composition: 'The rich nutrient base supports production of pyocyanin and pyoverdin pigments. P. aeruginosa typically shows beta-hemolysis and a characteristic metallic sheen on the colony surface. The medium also allows observation of the spreading growth pattern.',
            priority: 2
        },
        {
            name: 'Chocolate Agar',
            value: 'chocolate_agar',
            reason: 'Excellent growth with characteristic pigmentation',
            composition: 'Provides X and V factors, supports pigment production',
            priority: 'medium'
        }
    ],
    k_pneumoniae: [
        {
            name: 'MacConkey Agar',
            value: 'mac_conkey',
            reason: 'Primary choice for isolating Klebsiella. Shows pink, mucoid colonies.',
            composition: 'Contains bile salts and crystal violet (inhibits gram-positive bacteria), lactose (fermented by K. pneumoniae), and neutral red indicator. K. pneumoniae produces distinctively large, dome-shaped, mucoid pink colonies due to lactose fermentation and capsule production. The selective agents allow isolation from mixed samples.',
            priority: 1
        },
        {
            name: 'EMB Agar',
            value: 'emb',
            reason: 'Differential medium showing dark centers with mucoid appearance.',
            composition: 'Contains Eosin Y and Methylene Blue dyes which inhibit gram-positives and indicate acid production. K. pneumoniae produces large, mucoid colonies with dark centers due to acid production from lactose/sucrose fermentation, but without the metallic sheen characteristic of E. coli.',
            priority: 2
        },
        {
            name: 'Chocolate Agar',
            value: 'chocolate_agar',
            reason: 'Supports growth with characteristic mucoid appearance',
            composition: 'Rich medium with available growth factors',
            priority: 'medium'
        }
    ],
    'a_baumannii': [
        {
            name: 'Blood Agar',
            value: 'blood_agar',
            reason: 'Primary choice for isolation and identification of A. baumannii. Shows opaque, smooth colonies.',
            composition: 'Contains 5% sheep blood in nutrient agar base. Supports growth of A. baumannii and allows observation of colony morphology. Non-hemolytic colonies are typical.',
            priority: 1
        },
        {
            name: 'MacConkey Agar',
            value: 'mac_conkey',
            reason: 'Selective medium for isolation from clinical specimens. Shows non-lactose fermenting colonies.',
            composition: 'Contains bile salts and crystal violet that inhibit gram-positive bacteria. A. baumannii appears as colorless colonies due to lack of lactose fermentation.',
            priority: 1
        }
    ],
    'c_difficile': [
        {
            name: 'CCFA',
            value: 'ccfa',
            reason: 'Highly selective medium specifically designed for C. difficile isolation.',
            composition: 'Contains cycloserine and cefoxitin to inhibit other bacteria, and fructose as a carbon source. C. difficile produces characteristic yellow, ground-glass appearing colonies.',
            priority: 1
        }
    ],
    'n_gonorrhoeae': [
        {
            name: 'Modified Thayer-Martin Agar',
            value: 'thayer_martin',
            reason: 'Selective medium specifically designed for isolation of N. gonorrhoeae.',
            composition: 'Contains antibiotics (vancomycin, colistin, nystatin, trimethoprim) to inhibit other bacteria and fungi. Enriched with hemoglobin and growth supplements.',
            priority: 1
        },
        {
            name: 'Chocolate Agar',
            value: 'chocolate_agar',
            reason: 'Supports growth with essential X and V factors.',
            composition: 'Heat-treated blood provides X factor (hemin) and V factor (NAD) required for growth.',
            priority: 2
        }
    ],
    'h_influenzae': [
        {
            name: 'Chocolate Agar',
            value: 'chocolate_agar',
            reason: 'Primary choice as it provides essential X and V factors required for H. influenzae growth.',
            composition: 'Contains heated blood which releases X factor (hemin) and V factor (NAD). These factors are essential for H. influenzae growth.',
            priority: 1
        }
    ],
    'l_pneumophila': [
        {
            name: 'BCYE Agar',
            value: 'bcye',
            reason: 'Specifically designed for isolation of Legionella species.',
            composition: 'Contains L-cysteine, iron salts, and α-ketoglutarate which are essential for Legionella growth. Includes selective antibiotics to inhibit other bacteria.',
            priority: 1
        }
    ],
    'c_albicans': [
        {
            name: 'CHROMagar Candida',
            value: 'chrom_agar',
            reason: 'Differential medium allowing identification of Candida species based on color.',
            composition: 'Contains chromogenic substrates that produce different colored colonies for different Candida species. C. albicans appears as green colonies.',
            priority: 1
        },
        {
            name: 'Sabouraud Dextrose Agar',
            value: 'sab_dex',
            reason: 'Traditional fungal isolation medium.',
            composition: 'Contains peptone and dextrose, pH is acidic (5.6) which inhibits bacterial growth while supporting fungal growth.',
            priority: 2
        }
    ],
    'c_auris': [
        {
            name: 'CHROMagar Candida',
            value: 'chrom_agar',
            reason: 'Allows differentiation of C. auris from other Candida species.',
            composition: 'Chromogenic medium where C. auris typically appears as pale colored colonies, distinct from other Candida species.',
            priority: 1
        },
        {
            name: 'Sabouraud Dextrose Agar',
            value: 'sab_dex',
            reason: 'Standard fungal isolation medium.',
            composition: 'Acidic pH and high glucose concentration favors fungal growth while inhibiting bacteria.',
            priority: 2
        }
    ],
    'aspergillus': [
        {
            name: 'Sabouraud Dextrose Agar',
            value: 'sab_dex',
            reason: 'Primary choice for isolation and identification of Aspergillus species.',
            composition: 'The acidic pH and high glucose concentration supports rapid growth of Aspergillus. Allows development of characteristic conidial heads for species identification.',
            priority: 1
        }
    ]
};

document.addEventListener('DOMContentLoaded', function() {
    const organismSelect = document.getElementById('organism');
    const recommendationsDiv = document.getElementById('recommendations');
    const recommendationList = document.getElementById('recommendationList');
    const customMediaSelection = document.getElementById('customMediaSelection');
    const mediaSelect = document.getElementById('media');
    const submitButton = document.getElementById('submitButton');
    const useRecommendedBtn = document.getElementById('useRecommended');
    const chooseCustomBtn = document.getElementById('chooseCustom');

    if (organismSelect && mediaSelect) {
        organismSelect.addEventListener('change', function() {
            const organism = this.value;
            
            // Reset UI state
            customMediaSelection.style.display = 'none';
            submitButton.style.display = 'none';
            
            // Show/hide recommendations
            if (organism && mediaRecommendations[organism]) {
                const recommendations = mediaRecommendations[organism];
                
                // Clear and populate recommendations
                recommendationList.innerHTML = `
                    <div class="d-flex">
                        <div class="flex-grow-1 me-3" style="width: 70%;">
                            ${recommendations.map((rec, index) => `
                                <div class="list-group-item ${rec.priority === 1 ? 'list-group-item-primary' : rec.priority === 2 ? 'list-group-item-secondary' : ''} mb-2">
                                    <div class="d-flex justify-content-between align-items-start">
                                        <h6 class="mb-1">${rec.name}</h6>
                                        ${rec.priority === 1 && index === 0 ? '<span class="badge bg-success">Auto-selected</span>' : ''}
                                    </div>
                                    <p class="mb-1"><strong>Why:</strong> ${rec.reason}</p>
                                    <p class="mb-0"><strong>Composition:</strong> ${rec.composition}</p>
                                </div>
                            `).join('')}
                        </div>
                        <div class="flex-shrink-0" style="width: 30%;">
                            <div class="recommendations-legend">
                                <div class="card border-0">
                                    <div class="card-body p-3">
                                        <div class="mb-3">
                                            <div class="d-flex align-items-center mb-1">
                                                <div class="badge bg-primary px-2 py-1">Primary Choice</div>
                                            </div>
                                            <small class="text-muted d-block">Best for identification</small>
                                            <small class="text-success d-block mt-1">First primary choice is auto-selected</small>
                                        </div>
                                        <div class="mb-3">
                                            <div class="d-flex align-items-center mb-1">
                                                <div class="badge bg-secondary px-2 py-1">Secondary Choice</div>
                                            </div>
                                            <small class="text-muted d-block">Alternative option</small>
                                        </div>
                                        <div>
                                            <div class="d-flex align-items-center mb-1">
                                                <div class="badge bg-light text-dark border px-2 py-1">Additional</div>
                                            </div>
                                            <small class="text-muted d-block">Supports growth</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>`;

                recommendationsDiv.style.display = 'block';
            } else {
                recommendationsDiv.style.display = 'none';
            }
        });

        // Handle "Use Recommended Media" button click
        useRecommendedBtn.addEventListener('click', function() {
            const organism = organismSelect.value;
            if (mediaRecommendations[organism]) {
                const primaryMedia = mediaRecommendations[organism].find(m => m.priority === 1);
                if (primaryMedia) {
                    mediaSelect.value = primaryMedia.value;
                    customMediaSelection.style.display = 'block';
                    submitButton.style.display = 'block';
                }
            }
        });

        // Handle "Choose Different Media" button click
        chooseCustomBtn.addEventListener('click', function() {
            customMediaSelection.style.display = 'block';
            submitButton.style.display = 'block';
        });

        mediaSelect.addEventListener('change', function() {
            submitButton.style.display = this.value ? 'block' : 'none';
        });
    }
});

function addOption(select, value, text) {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = text;
    select.appendChild(option);
} 