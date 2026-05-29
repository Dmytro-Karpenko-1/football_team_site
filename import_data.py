import os
import django
import csv
from datetime import datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from team.models import Team, Player, Coach, Match, Standing, BlogPost, Sponsor


def clean(value, default=''):
    """Return a stripped CSV value or a default."""
    if value is None:
        return default
    value = value.strip()
    return value if value else default


def get_team(name):
    """Get a team by name, creating a placeholder when CSV references a missing team."""
    team_name = clean(name)
    team, created = Team.objects.get_or_create(
        name=team_name,
        defaults={
            'description': 'Команду створено автоматично під час імпорту CSV.',
            'founded_year': 2020,
            'city': '',
            'logo': '',
        }
    )
    if created:
        print(f"ℹ️ Створено відсутню команду: {team_name}")
    return team


def get_standing_team(name):
    """Find a team for standings while keeping the table display name intact."""
    team_name = clean(name)
    candidates = [team_name]

    if team_name.startswith('ФК '):
        candidates.append(team_name[3:])
    else:
        candidates.append(f'ФК {team_name}')

    for candidate in candidates:
        team = Team.objects.filter(name=candidate).first()
        if team:
            return team

    return get_team(team_name)


def parse_goal_difference(value):
    return int(clean(value, '0').replace('+', ''))


def goals_from_difference(goal_difference):
    if goal_difference >= 0:
        return goal_difference, 0
    return 0, abs(goal_difference)


def import_teams(csv_file):
    """Завантажити команди з CSV"""
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Team.objects.get_or_create(
                name=clean(row['name']),
                defaults={
                    'description': clean(row.get('description'), ''),
                    'founded_year': int(clean(row.get('founded_year'), '2020')),
                    'city': clean(row.get('city'), ''),
                    'logo': clean(row.get('logo'), '')
                }
            )
    print("✅ Команди завантажені")

def import_matches(csv_file):
    """Завантажити матчі з CSV"""
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            team = get_team(row['team'])
            opponent = get_team(row['opponent'])
            
            match_date = datetime.strptime(row['match_date'], '%Y-%m-%d %H:%M')
            match_date = timezone.make_aware(match_date)
            
            Match.objects.get_or_create(
                team=team,
                opponent=opponent,
                match_date=match_date,
                defaults={
                    'location': clean(row.get('location'), ''),
                    'team_goals': int(clean(row.get('team_goals'), '0')) if clean(row.get('team_goals')) else None,
                    'opponent_goals': int(clean(row.get('opponent_goals'), '0')) if clean(row.get('opponent_goals')) else None,
                    'status': clean(row.get('status'), 'upcoming')
                }
            )
    print("✅ Матчі завантажені")


def import_standings(csv_file):
    """Завантажити турнірну таблицю з CSV у форматі: #, Ім'я, І, Різн., О"""
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            display_name = clean(row["Ім'я"])
            goal_difference = parse_goal_difference(row['Різн.'])
            goals_for, goals_against = goals_from_difference(goal_difference)

            Standing.objects.update_or_create(
                team=get_standing_team(display_name),
                defaults={
                    'display_name': display_name,
                    'position': int(clean(row['#'], '0')),
                    'played': int(clean(row['І'], '0')),
                    'won': 0,
                    'draw': 0,
                    'lost': 0,
                    'goals_for': goals_for,
                    'goals_against': goals_against,
                    'points': int(clean(row['О'], '0')),
                }
            )
    print("✅ Турнірна таблиця завантажена")


def import_players(csv_file):
    """Завантажити гравців з CSV"""
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            team = get_team(row['team'])
            birth_date = datetime.strptime(row['birth_date'], '%Y-%m-%d').date()
            
            Player.objects.get_or_create(
                first_name=clean(row['first_name']),
                last_name=clean(row['last_name']),
                team=team,
                defaults={
                    'position': clean(row.get('position'), 'MID'),
                    'number': int(clean(row.get('number'), '0')),
                    'photo': clean(row.get('photo'), ''),
                    'birth_date': birth_date,
                    'nationality': clean(row.get('nationality'), '')
                }
            )
    print("✅ Гравці завантажені")

def import_coaches(csv_file):
    """Завантажити тренерів з CSV"""
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            team = get_team(row['team'])
            
            Coach.objects.get_or_create(
                first_name=clean(row['first_name']),
                last_name=clean(row['last_name']),
                team=team,
                defaults={
                    'position': clean(row.get('position'), ''),
                    'photo': clean(row.get('photo'), ''),
                    'bio': clean(row.get('bio'), ''),
                    'experience': int(clean(row.get('experience'), '0'))
                }
            )
    print("✅ Тренери завантажені")

def import_sponsors(csv_file):
    """Завантажити спонсорів з CSV"""
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            team = get_team(row['team'])
            
            Sponsor.objects.get_or_create(
                name=clean(row['name']),
                team=team,
                defaults={
                    'logo': clean(row.get('logo'), ''),
                    'website': clean(row.get('website'), ''),
                    'level': clean(row.get('level'), 'bronze')
                }
            )
    print("✅ Спонсори завантажені")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("""
        Використання: python import_data.py [команда] [файл.csv]
        
        Команди:
        - teams <teams.csv>
        - matches <matches.csv>
        - standings <standings.csv>
        - players <players.csv>
        - coaches <coaches.csv>
        - sponsors <sponsors.csv>
        
        Приклад: python import_data.py teams teams.csv
        """)
        sys.exit()
    
    command = sys.argv[1]
    csv_file = sys.argv[2] if len(sys.argv) > 2 else f'{command}.csv'
    
    if command == 'teams':
        import_teams(csv_file)
    elif command == 'matches':
        import_matches(csv_file)
    elif command == 'standings':
        import_standings(csv_file)
    elif command == 'players':
        import_players(csv_file)
    elif command == 'coaches':
        import_coaches(csv_file)
    elif command == 'sponsors':
        import_sponsors(csv_file)
    else:
        print(f"❌ Невідома команда: {command}")
