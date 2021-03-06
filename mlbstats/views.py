from django.shortcuts import render
import pygal
import csv
import requests


def homepage(request):
    print('--------view homepage')
    context = {}
    return render(request, 'homepage.html', context)

def season(request):
    print('--------view season')
    nav_active_season = ' active'
    player_name = ''
    stat_line_chart = ''
    if 'stat' in request.GET:
        stat_form = request.GET['stat']
        team = request.GET['team']
        file = 'mlbstats/static/team-hist-stats/' + team + '-historical.csv'
        list_for_csv, x_labels, y_values = build_axes(file, stat_form)
        time_period = 'Over Time'
        if request.GET['numOfSeasons'] != '':
            x_labels, y_values = truncate_chart_x_y(x_labels, y_values, request.GET['numOfSeasons'])
            time_period = 'for the last ' + request.GET['numOfSeasons'] + ' Seasons'
        ### Create Chart ###
        line_chart = pygal.Line(x_label_rotation=70)
        line_chart.title = 'Team ' + stat_form + ' ' + time_period
        line_chart.x_labels = map(str, x_labels)
        line_chart.add(team, y_values)
        stat_line_chart = line_chart.render_data_uri()
  
    context = {
        'chart': stat_line_chart,
        'navActiveSeason': nav_active_season,
        }
    return render(request, 'season.html', context)

def truncate_chart_x_y(x_values, y_values, length):
    num_of_seasons = int(length)
    new_x_labels = x_values[(num_of_seasons*-1):]
    new_y_values = y_values[(num_of_seasons*-1):]
    return new_x_labels, new_y_values

def build_axes(file, stat_form):
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
            y_values.append(float(row[stat_csv_position]))
    x_labels.reverse()
    y_values.reverse()

    return list_for_csv, x_labels, y_values

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
    player_name1 = ''
    player_name2 = ''
    stat_line_chart = ''
    if 'player1' in request.GET:
        player_name1 = request.GET['player1']
        player_name2 = request.GET['player2']
        stat_form = request.GET['stat'].upper()
        file2 = None
        file1 = 'mlbstats/static/player-stats/' + player_name1 + '_player_stats.csv'
        if player_name2 != '':
            file2 = 'mlbstats/static/player-stats/' + player_name2 + '_player_stats.csv'
        stat_line_chart = create_chart(file1, stat_form, player_name1, file2, player_name2)
    context = {
        'player_name1':  player_name1,
        'line_chart': stat_line_chart,
        'navActivePlayer': ' active',
    }
    return render(request, 'player.html', context)

def generate_chart_values(file, stat_form):
    with open(file) as csv.file:
            csv_reader = csv.reader(csv.file, delimiter=',')
            header = next(csv_reader)
            for idx, item in enumerate(header):
                if item == stat_form:
                    stat_csv_position = idx
                    break
            list_for_csv = []
            x_labels = []
            y_values = []
            stats_dict = {}
            list_for_csv.append(csv_reader)
            for row in csv_reader:
                stats_dict[row[0]] = float(row[idx])
                x_labels.append(row[0])
                y_values.append(float(row[idx]))
    return x_labels, y_values, stats_dict

def create_chart(file, stat_form, player_name1, file2=None, player_name2=None):
    x_labels_1, y_values_1, stats_dict_1 = generate_chart_values(file, stat_form)
    if file2:
        x_labels_2, y_values_2, stats_dict_2 = generate_chart_values(file2, stat_form)
        set_1 = set(x_labels_1)
        set_2 = set(x_labels_2)
        two_not_in_one = list(set_2 - set_1)
        one_not_in_two = list(set_1 - set_2)
        x_labels_merged = x_labels_1 + two_not_in_one
        x_labels_merged.sort()
        for year in two_not_in_one:
            stats_dict_1[year] = 0
        for year in one_not_in_two:
            stats_dict_2[year] = 0
        y_labels_final_1 = []
        y_labels_final_2 = []
        for year in x_labels_merged:
            y_labels_final_1.append(stats_dict_1[year])
            y_labels_final_2.append(stats_dict_2[year])
    else:
        x_labels_merged = x_labels_1
    line_chart = pygal.Bar()
    line_chart.title = stat_form + ' per Season'
    line_chart.x_labels = map(str, x_labels_merged)
    if file2:
        line_chart.add(player_name1, y_labels_final_1)
        line_chart.add(player_name2, y_labels_final_2)
    else:
        line_chart.add(player_name1, y_values_1)
    stat_line_chart = line_chart.render_data_uri()
    return stat_line_chart






def scorespast(request):
    print('--------view scorespast')
    navActiveScoresPast = ' active'
    #get score information
    url = 'https://www.thesportsdb.com/api/v1/json/1/eventslast.php?id=135274'
    response = requests.get(url)
    scores_data = response.json() # Interpret response as JSON
    #get Away team information
    away_team_dict = {}
    #for item in scores_data['results']:
    #    url_away_team = 'https://www.thesportsdb.com/api/v1/json/1/eventslast.php?id=135274'
    #    response = requests.get(url)
    #    scores_data = response.json() # Interpret response as JSON
    url_brewers = 'https://www.thesportsdb.com/api/v1/json/1/lookupteam.php?id=135274'
    response = requests.get(url_brewers)
    brewres_data = response.json() # Interpret response as JSON
    brewers_img = brewres_data['teams'][0]['strTeamBadge']
    
    context = {
        "navActiveScoresPast": navActiveScoresPast,
        'scores_data': scores_data['results'],
        'team_image': brewers_img

    }

    return render(request, 'scorespast.html', context)

