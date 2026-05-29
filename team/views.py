from django.shortcuts import render, get_object_or_404
from .models import Team, Player, Coach, Match, BlogPost, Standing
from .forms import JoinTeamForm


def home(request):
    """Home page view"""
    recent_matches = (
        Match.objects
        .select_related('team', 'opponent')
        .filter(status='played', team__name="ФК Зазим'є")
        .order_by('-match_date')[:3]
    )
    
    context = {
        'recent_matches': recent_matches,
    }
    return render(request, 'home.html', context)


def about(request):
    """About page view"""
    teams = Team.objects.all()
    players = Player.objects.select_related('team').order_by('team__name', 'number', 'last_name')
    coaches = Coach.objects.select_related('team').order_by('team__name', 'position', 'last_name')
    context = {
        'teams': teams,
        'players': players,
        'coaches': coaches,
    }
    return render(request, 'team/about.html', context)


def team(request):
    """Team roster page."""
    coach = (
        Coach.objects
        .select_related('team')
        .filter(team__name="ФК Зазим'є")
        .order_by('position', 'last_name', 'first_name')
        .first()
    )
    players = (
        Player.objects
        .select_related('team')
        .filter(team__name="ФК Зазим'є")
        .order_by('number', 'last_name', 'first_name')
    )
    context = {
        'coach': coach,
        'players': players,
    }
    return render(request, 'team/team.html', context)


def matches(request):
    """Matches list view"""
    upcoming_matches = (
        Match.objects
        .select_related('team', 'opponent')
        .filter(status='upcoming', team__name="ФК Зазим'є")
        .order_by('match_date')
    )
    played_matches_qs = (
        Match.objects
        .select_related('team', 'opponent')
        .filter(status='played', team__name="ФК Зазим'є")
        .order_by('-match_date')
    )
    played_matches = []
    team_form = []
    for match in played_matches_qs:
        if match.team_goals > match.opponent_goals:
            result = 'win'
            label = 'W'
        elif match.team_goals == match.opponent_goals:
            result = 'draw'
            label = 'D'
        else:
            result = 'lose'
            label = 'L'

        played_matches.append({
            'match': match,
            'result': result,
            'label': label,
        })

        if len(team_form) < 5:
            team_form.append({
                'match': match,
                'result': result,
                'label': label,
            })
    
    context = {
        'upcoming_matches': upcoming_matches,
        'played_matches': played_matches,
        'team_form': team_form,
    }
    return render(request, 'team/matches.html', context)


def standings(request):
    """Standings view"""
    standings = Standing.objects.all().order_by('position')
    recent_team_matches = (
        Match.objects
        .select_related('team', 'opponent')
        .filter(status='played', team__name="ФК Зазим'є")
        .order_by('-match_date')[:3]
    )
    recent_form = []
    for match in recent_team_matches:
        if match.team_goals > match.opponent_goals:
            result = 'win'
            label = 'W'
        elif match.team_goals == match.opponent_goals:
            result = 'draw'
            label = 'D'
        else:
            result = 'lose'
            label = 'L'

        recent_form.append({
            'match': match,
            'result': result,
            'label': label,
        })

    context = {
        'standings': standings,
        'recent_form': recent_form,
    }
    return render(request, 'team/standings.html', context)


def blog(request):
    """Blog list view"""
    blog_posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(blog_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'team/blog.html', context)


def blog_detail(request, pk):
    """Blog post detail view"""
    blog_post = get_object_or_404(BlogPost, pk=pk, is_published=True)
    context = {'blog_post': blog_post}
    return render(request, 'team/blog_detail.html', context)


def join(request):
    """Join team form view"""
    if request.method == 'POST':
        form = JoinTeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'team/join.html', {
                'success': True,
            })
    else:
        form = JoinTeamForm()
    
    context = {'form': form}
    return render(request, 'team/join.html', context)


def sponsors(request):
    """Partner search page."""
    return render(request, 'team/sponsors.html')
