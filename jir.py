import sys
import os
from jira import JIRA
from pprint import pprint
import json
import pandas as pd

our_devs = set({
    'Andriy Ivanochko',
    'Andriy Romaniv',
    'Dmytro Horohotskyi',
    'Oleh Ziniak',
    'Taras Khoma',
    'Viktor Levytskyi',
    'Vitaliy Petryk'
})


def get_all_devs(lst):
    devs = set()
    for i in lst:
        for j in i['devs']:
            devs.add(j)
    return devs


# def construct_querry(num):
#     que = f"project = CRT AND status not in ('In Progress', 'Reopened', 'New') and Sprint = '{num}' and sprint not in ('{num+1}','{num+2}','{num+3}','{num+4}')"
#     return que


def construct_upd_querry(num):
    que = 'project = CRT AND issuetype in standardIssueTypes() AND status in (Closed, "In Production", "In Staging", "Ready For Prod", "Ready for Staging", "Ready for Testing", Resolved) AND Sprint = "{}" AND Sprint not in ("{}","{}","{}","{}")'.format(num,num+1,num+2,num+3,num+4,)
    return que


def form_iss_list(issues):
    formed_issues = []
    for issue in issues:
        formed_issue = []
        if issue.raw['fields']['customfield_12400'] is not None:
            formed_issues.append({
                'key': issue.raw['key'],
                'summary': issue.raw['fields']['summary'],
                'devs': [dev['displayName'] for dev in issue.raw['fields'].get('customfield_12400', {'displayName': "None"})],
                'points': issue.raw['fields']['customfield_10003']
            })
    return formed_issues


def form_person_list(issues_list):
    pers_list = {person: [] for person in dev_list}
    for iss in issues_list:
        for dev in iss['devs']:
            if iss['points'] is not None:
                pers_list[dev].append(
                    '{} - {}'.format(iss['key'], iss['points']))
            else:
                pers_list[dev].append('{} - {}'.format(iss['key'], 0))
    return pers_list


def get_stats(formed_iss):
    stats = {dev: {'tasks': 0, 'points': 0} for dev in dev_list}
    for iss in formed_iss:
        for dev in iss['devs']:
            stats[dev]['tasks'] += 1
            if iss['points'] is not None:
                stats[dev]['points'] += iss['points']
    return stats


def get_team_stats(stats):
    team_stats = {'our': {'devs': 0, 'points': 0},
                  'theirs': {'devs': 0, 'points': 0}}
    for dev in stats.keys():
        if dev in our_devs:
            team_stats['our']['devs'] += 1
            team_stats['our']['points'] += stats[dev]['points']
        else:
            team_stats['theirs']['devs'] += 1
            team_stats['theirs']['points'] += stats[dev]['points']
    return team_stats


if len(sys.argv) == 2:
    sprint = int(sys.argv[1])
# else:
#     sprint = int(input('sprint?: '))



def create_csv(sprint):
    j = JIRA('https://chromeriver.atlassian.net',
         basic_auth=('####################', '########################'))
    issues = j.search_issues(
        construct_upd_querry(sprint), maxResults=200)  # issues search
    formed_list = form_iss_list(issues)
    global dev_list
    dev_list = set()
    for i in formed_list:
        for j in i['devs']:
            dev_list.add(j)

    stats = get_stats(formed_list)
    print(stats)
    t_stats = get_team_stats(stats)
    print(t_stats)
    p_list = form_person_list(formed_list)
    # pprint(stats)
    # pprint(t_stats)
    pprint(p_list)

    result_line = ['Points', 'Dev number']
    result_line.extend([None for i in range(len(dev_list) - 2)])
    our_line = [int(t_stats['our']['points']), int(t_stats['our']['devs'])]
    our_line.extend([None for i in range(len(dev_list) - 2)])
    theirs_line = [int(t_stats['theirs']['points']), (t_stats['theirs']['devs'])]
    theirs_line.extend([None for i in range(len(dev_list) - 2)])

    print(our_line)
    print(theirs_line)

    frame = pd.DataFrame.from_dict(p_list, orient='index')
    frame['  '] = None
    frame['   '] = p_list.keys()
    frame['Points'] = [i['points'] for i in stats.values()]
    frame['Tasks'] = [i['tasks'] for i in stats.values()]
    frame[' '] = None
    frame[''] = None
    frame['Results'] = result_line
    frame['Our'] = our_line
    frame['Not our'] = theirs_line

    # print(frame)
    frame.transpose().to_csv('Sprint_{}_stats.csv'.format(sprint), sep=';')
    # print(frame.transpose())


    print('\n\nFile {}{} was created successfully!\n\n'.format(os.path.abspath('.'), 'Sprint_{}_stats.csv'.format(sprint)))
    # a = input('ok?')
    return 'Sprint_{}_stats.csv'.format(sprint)

create_csv(204)