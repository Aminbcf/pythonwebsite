from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Predefined modules with proper structure for both study types
MODULES = {
    'lmd': {
        1: {  # First Year
            1: [  # Semester 1
                {'name': 'Analyse 1', 'credits': 4},
                {'name': 'Algèbre 1', 'credits': 3},
                {'name': 'Algorithmique et structure de données 1', 'credits': 4},
                {'name': 'Structure machine 1', 'credits': 3},
                {'name': 'Terminologie Scientifique et expression écrite', 'credits': 1},
                {'name': 'Langue étrangère 1', 'credits': 1},
                {'name': 'Physique 1 (mécanique du point)', 'credits': 2},
                {'name': 'Electronique et composants des systèmes', 'credits': 4}
            ],
            2: [  # Semester 2
                {'name': 'Analyse 2', 'credits': 2},
                {'name': 'Algèbre 2', 'credits': 4},
                {'name': 'Algorithmique et structure de données 2', 'credits': 2},
                {'name': 'Structure machine 2', 'credits': 4},
                {'name': 'Introduction aux probabilités et statistique descriptive', 'credits': 2},
                {'name': 'Technologie de l\'Information et de la Communication', 'credits': 2},
                {'name': 'Outils de programmation pour les mathématiques', 'credits': 1},
                {'name': 'Physique 2 (électricité générale)', 'credits': 1}
            ]
        },
        2: {  # Second Year
            1: [  # Semester 3
                {'name': 'Architecture des ordinateurs', 'credits': 3},
                {'name': 'Algorithmique et structure de données 3', 'credits': 3},
                {'name': 'Systèmes d\'information', 'credits': 3},
                {'name': 'Théorie des graphes', 'credits': 2},
                {'name': 'Méthodes numériques', 'credits': 2},
                {'name': 'Logique mathématique', 'credits': 2},
                {'name': 'Langue étrangère 2', 'credits': 1}
            ],
            2: [  # Semester 4
                {'name': 'Théorie des langages', 'credits': 3},
                {'name': 'Système d\'exploitation 1', 'credits': 3},
                {'name': 'Bases de données', 'credits': 3},
                {'name': 'Réseaux', 'credits': 2},
                {'name': 'Programmation orientée objet', 'credits': 2},
                {'name': 'Développement d\'Applications Web', 'credits': 2},
                {'name': 'Langue étrangère 3', 'credits': 1}
            ]
        },
        3: {  # Third Year
            1: [  # Semester 5
                {'name': 'Système d\'information distribué', 'credits': 6},
                {'name': 'Système d\'aide à la décision', 'credits': 4},
                {'name': 'Génie Logiciel', 'credits': 6},
                {'name': 'Interface Homme Machine', 'credits': 4},
                {'name': 'Administration des Systèmes d\'information', 'credits': 4},
                {'name': 'Programmation avancée pour le Web', 'credits': 4},
                {'name': 'Economie numérique et veille stratégique', 'credits': 2}
            ],
            2: [  # Semester 6
                {'name': 'Recherche d\'information', 'credits': 5},
                {'name': 'Sécurité Informatique', 'credits': 5},
                {'name': 'Données semi structurées', 'credits': 5},
                {'name': 'Système d\'exploitation 2', 'credits': 5},
                {'name': 'Projet', 'credits': 6},
                {'name': 'Business Intelligence', 'credits': 2},
                {'name': 'Rédaction Scientifique', 'credits': 2}
            ]
        }
    },
    'engineering': {
        1: {  # First Year
            1: [
                {'name': 'Algorithme 1', 'coefficient': 5},
                {'name': 'Structure machine', 'coefficient': 4},
                {'name': 'Introduction aux system d\'exploitation', 'coefficient': 3},
                {'name': 'Analyse 1', 'coefficient': 3},
                {'name': 'Algebre 1', 'coefficient': 3},
                {'name': 'Elctronique Fondamentale', 'coefficient': 1},
                {'name': 'Technique d\'expression ecrit et bureutique', 'coefficient': 1}
            ],
            2: [
                {'name': 'Algorithme 2', 'coefficient': 4},
                {'name': 'Architecture des ordinateurs', 'coefficient': 4},
                {'name': 'Analyse 2', 'coefficient': 3},
                {'name': 'Algebre 2', 'coefficient': 3},
                {'name': 'Logic mathematique', 'coefficient': 3},
                {'name': 'probabilites et statistique', 'coefficient': 2},
                {'name': 'probabilites et statistique', 'coefficient': 1}
            ]
        },
        2: {
            1: [  # Updated first semester modules
                {'name': 'Structure de Fichiers et Structure de Données', 'coefficient': 5},
                {'name': 'Algorithmique et Complexité', 'coefficient': 4},
                {'name': 'Entreprenariat', 'coefficient': 1},
                {'name': 'Architecture des Ordinateurs 2', 'coefficient': 5},
                {'name': 'Probabilité et Statistique 2', 'coefficient': 2},
                {'name': 'Algèbre 3', 'coefficient': 4},
                {'name': 'Programmation Orientée Objet', 'coefficient': 5},
                {'name': 'Analyse Mathématique 3', 'coefficient': 4}
            ],
            2: [
                {'name': 'Introduction aux system d\'information', 'coefficient': 3},
                {'name': 'Programmation Orientée Objet 2', 'coefficient': 6},
                {'name': 'Introduction aux reseaux informatique', 'coefficient': 4},
                {'name': 'Introduction aux base de donnes', 'coefficient': 3},
                {'name': 'Theorie de language', 'coefficient': 3},
                {'name': 'Theorie des graphes', 'coefficient': 3},
                {'name': 'Projet pluridisciplinaire', 'coefficient': 6},
                {'name': 'Anglais 2', 'coefficient': 2}
            ]
        },
        3: {  # Third Year
            1: [
                {'name': 'Fondements de l\'AI', 'coefficient': 2},
                {'name': 'Système d\'Exploitation', 'coefficient': 3},
                {'name': 'Algorithmique et Complexité Avancées', 'coefficient': 4},
                {'name': 'Génie Logiciel', 'coefficient': 4},
                {'name': 'Administration et Architecture', 'coefficient': 4},
                {'name': 'Techniques d\'Optimisation', 'coefficient': 3}
            ],
            2: [
                {'name': 'Conception de logiciles', 'coefficient': 4},
                {'name': 'Programmation WEB (PWEB)', 'coefficient': 3},
                {'name': 'BDD : Optimisation', 'coefficient': 3},
                {'name': 'Analyse numerique', 'coefficient': 4},
                {'name': 'Introduction a la securite informatique', 'coefficient': 2},
                {'name': 'Compilation 1', 'coefficient': 4}

            ]
        }
    }
}


def validate_grade(grade_value):
    """Validate a single grade value"""
    try:
        grade = float(grade_value)
        return 0 <= grade <= 20
    except (ValueError, TypeError):
        return False


def calculate_module_grade(exam, td):
    """Calculate module grade using the formula: exam * 0.6 + td * 0.4"""
    return exam * 0.6 + td * 0.4


def calculate_semester_average(grades, weight_key):
    """Calculate semester average using the formula: sum(module_grade * credits) / sum(credits)"""
    if not grades:
        return 0

    total_credits = sum(float(grade[weight_key]) for grade in grades)
    weighted_sum = sum(calculate_module_grade(float(grade['exam']), float(grade['td'])) * float(grade[weight_key]) for grade in grades)

    return round(weighted_sum / total_credits, 2) if total_credits > 0 else 0


def calculate_statistics(grades):
    """Calculate additional statistics for grades"""
    if not grades:
        return {
            "highest_grade": 0,
            "lowest_grade": 0,
            "passing_modules": 0,
            "failing_modules": 0,
            "total_modules": 0
        }

    module_grades = [calculate_module_grade(float(grade['exam']), float(grade['td'])) for grade in grades]

    return {
        "highest_grade": max(module_grades),
        "lowest_grade": min(module_grades),
        "passing_modules": sum(1 for g in module_grades if g >= 10),
        "failing_modules": sum(1 for g in module_grades if g < 10),
        "total_modules": len(grades)
    }


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/modules', methods=['GET'])
def get_modules():
    """Get modules for a specific year, semester, and study type"""
    study_type = request.args.get('type', 'lmd')
    year = int(request.args.get('year', 1))
    semester = int(request.args.get('semester', 1))

    if study_type in MODULES and year in MODULES[study_type]:
        return jsonify(MODULES[study_type][year].get(semester, []))
    return jsonify([])


@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Calculate semester average and statistics"""
    data = request.json
    study_type = data.get('study_type', 'lmd')
    grades = data.get('grades', [])

    # Validate grades
    for grade in grades:
        if not validate_grade(grade.get('exam')) or not validate_grade(grade.get('td')):
            return jsonify({"error": "Invalid grade value. Grades must be between 0 and 20"}), 400

    weight_key = 'credits' if study_type == 'lmd' else 'coefficient'
    average = calculate_semester_average(grades, weight_key)
    statistics = calculate_statistics(grades)

    return jsonify({
        "average": average,
        "statistics": statistics
    })


if __name__ == '__main__':
    app.run(debug=True)
