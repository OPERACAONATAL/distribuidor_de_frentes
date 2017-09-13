import pandas as pd
import re
import copy
import math

# Padrão para remover vírgulas e espaços
pattern = re.compile("^\s+|\s*,\s*|\s+$")    
teams = ['Endomarketing', 'Fotografia', 'Programação', 'Vídeo', 'Workshop']
dates_times = ['Seg 12h30min -- 14h', 'Seg 18h - 19h', 'Seg 19 - 20h', 'Seg 20 - 21h', 'Seg 21 - 22h', 'Ter 12h30min - 14h', 'Ter 18h - 19h', 'Ter 19 - 20h', 'Ter 20 - 21h', 'Ter 21 - 22h', 'Qua 12h30min - 14h', 'Qua 18h - 19h', 'Qua 19 - 20h', 'Qua 20 - 21h', 'Qua 21 - 22h', 'Qui 12h30min - 14h', 'Qui 20 - 21h', 'Qui 21 - 22h', 'Sábado ou Domingo']

def strip(arg, array):
    values = copy.deepcopy(array)
    options = sorted([x for x in pattern.split(arg) if x])

    for i in range(0, len(values)):
        if values[i] not in options:
            values[i] = math.nan
        else:
            values[i] = 1

    return values

def strip_teams(arg):
    return strip(arg, teams)

def strip_date_time(arg):
    return strip(arg, dates_times)

df = pd.read_csv('answers.csv')
df.drop(df.columns[0], axis=1, inplace=True)

df['Frentes'] = df.pop('Qual frente você gostaria de participar nesse primeiro momento?').apply(strip_teams)
df[teams] = df.pop('Frentes').apply(pd.Series)

df['Opções'] = df.pop('Horários').apply(strip_date_time)
df[dates_times] = df.pop('Opções').apply(pd.Series)

# Ordena os melhores horários de acordo com as frentes
for team in teams:
    team_times = df[df[f"{team}"] == 1]
    team_times.drop(teams, axis=1, inplace=True)

    # Adiciona a linha de total
    sum_row = team_times[dates_times].sum()
    team_times_sum = pd.DataFrame(data=sum_row).T
    team_times_sum = team_times_sum.reindex(columns=team_times.columns)
    team_times = team_times.append(team_times_sum, ignore_index=True)

    team_times = team_times.dropna(axis=1, how='all')
    team_times.to_csv(f"{team}.csv", index=False)
    
df.to_csv('new_answers.csv', index=False)
