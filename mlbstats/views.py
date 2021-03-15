from django.shortcuts import render
import pygal
import csv


# Create your views here.
def homepage(request):
    print('--------view homepage')
    
    bar_chart = pygal.Bar()
    bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
    b = bar_chart.render_data_uri()
    
    context = {
        'adoptions_needed': 5,
        'b': b, 
    }
    return render(request, 'homepage.html', context)

def season(request):
    print('--------view season')
    return render(request, 'season.html')

def team(request):
    print('--------view team')
    return render(request, 'team.html')

def player(request):
    print('--------view player')
    player_name = ''
    stat_line_chart = ''
    if 'player' in request.GET:
        print('player info request:', request.GET['player'])
        player_name = request.GET['player']
        file = 'mlbstats/static/player-stats/ryan-braun-player_stats.csv'
        x_labels = []
        with open(file) as csv.file:
            csv_reader = csv.reader(csv.file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                x_labels.append(row[0])
        print(x_labels)
        print(x_labels[0])
        print(len(x_labels))
        
        line_chart = pygal.Bar()
        line_chart.title = 'RBIs per Season'
        line_chart.x_labels = map(str, x_labels)
        line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
        line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
        line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
        line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
        stat_line_chart = line_chart.render_data_uri()


    context = {
        'player_name':  player_name,
        'line_chart': stat_line_chart,
    }

    return render(request, 'player.html', context)