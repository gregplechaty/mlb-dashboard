from django.shortcuts import render
import pygal
import csv


# Create your views here.
def homepage(request):
    print('--------view homepage')
    
    
    
    context = {
        'adoptions_needed': 5,
 
    }
    return render(request, 'homepage.html', context)

def season(request):
    print('--------view season')
    nav_active_season = ' active'
    player_name = ''
    stat_line_chart = ''
    if 'stat' in request.GET and request.GET['stat'] != "":
        print('Historical statistic info request:', request.GET['stat'])
        stat = request.GET['stat']
        stat_form = request.GET['stat']
        file = 'mlbstats/static/team-hist-stats/brewers-historical.csv'
        ####################
        list_for_csv = []
        x_labels = []
        y_values = []
        ####################
        with open(file) as csv.file:
            csv_reader = csv.reader(csv.file, delimiter=',')
            header = next(csv_reader)
            for idx, item in enumerate(header):
                if item == stat_form:
                    stat_csv_position = idx
                    break
            list_for_csv.append(csv_reader)
            print(stat_csv_position)
            for row in csv_reader:
                x_labels.append(row[0])
                y_values.append(float(row[stat_csv_position]))
        x_labels.reverse()
        y_values.reverse()
        ### Create Chart ###
        line_chart = pygal.Line(x_label_rotation=70)
        line_chart.title = 'Team stats for ' + stat_form + ' over time'
        line_chart.x_labels = map(str, x_labels)
        line_chart.add('Brewers', y_values)
        stat_line_chart = line_chart.render_data_uri()
  
    context = {
        'chart': stat_line_chart,
        'navActiveSeason': nav_active_season,
        }
    return render(request, 'season.html', context)

def team(request):
    print('--------view team')
    nav_active_team = ' active'
    ##read in file
    file = 'mlbstats/static/team-year-detail-stats/brewers-2020.csv'
    list_of_rows = []
    with open(file) as csv.file:
            csv_reader = csv.reader(csv.file, delimiter=',')
            
    #create header. format = list
            header = next(csv_reader)
    #Create each record. loop through .csv
            for row in csv_reader:
                row[2] = row[2].split('\\')[0]
                print(row[2])
                list_of_rows.append(row)
            
    #return lists. html will actually format
    context = {
        'header': header,
        'rows': list_of_rows,
        'navActiveTeam': nav_active_team,
    }
    
    return render(request, 'team.html', context)

def player(request):
    print('--------view player')
    nav_active_player = ' active'
    player_name = ''
    stat_line_chart = ''
    if 'player1' in request.GET:
        print('player info request:', request.GET['player1'])
        player_name = request.GET['player1']
        stat_form = request.GET['stat'].upper()
        file = 'mlbstats/static/player-stats/ryan-braun_player_stats.csv'
        ####################
        list_for_csv = []
        x_labels = []
        y_values = []
        ####################
        with open(file) as csv.file:
            csv_reader = csv.reader(csv.file, delimiter=',')
            header = next(csv_reader)
            for idx, item in enumerate(header):
                if item == stat_form:
                    stat_csv_position = idx
                    break
            list_for_csv.append(csv_reader)
            for row in csv_reader:
                x_labels.append(row[0])
                y_values.append(float(row[idx]))
            
        

        ### Create chart ###
        line_chart = pygal.Bar()
        line_chart.title = stat_form + ' per Season'
        line_chart.x_labels = map(str, x_labels)
        line_chart.add('Ryan Braun', y_values)
        stat_line_chart = line_chart.render_data_uri()


    context = {
        'player_name':  player_name,
        'line_chart': stat_line_chart,
        'navActivePlayer': nav_active_player,
    }

    return render(request, 'player.html', context)