import matplotlib,requests,pygal

#加入中文显示
import  matplotlib.font_manager as fm
# 解决中文乱码，本案例使用宋体字
myfont=fm.FontProperties(fname=r"C:\\Windows\\Fonts\\simsun.ttc")



def repos_hist():
    #查看API速率限制
    url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
    r = requests.get(url)
    print("Status code:",r.status_code) # 状态码200表示成功
    response_dict = r.json() # 将API响应存储在一个变量里面
    print("Hithub总的Python仓库数：",response_dict['total_count'])

    # 探索有关仓库的信息
    repo_dicts = response_dict['items']
    names,stars = [],[]
    for repo_dict in repo_dicts:
        names.append(repo_dict['name'])
        stars.append(repo_dict['stargazers_count'])
    # 可视化,x_label_rotation围绕x轴旋转45度，show_legend图例隐藏与否
    my_config = pygal.Config()
    chart = pygal.Bar(my_config)
    chart.title = 'Github最受欢迎的星标项目'
    chart.x_labels = names
    chart.add('星标',stars)

    chart.render_to_file('python_repos.svg')

    # print('查看每个python仓库的信息：\n')
    # for repo_dict in repo_dicts:
    #     print('项目名称：',repo_dict['name'])
    #     print('所有者：',repo_dict['owner']['login'])
    #     print('星级评分：',repo_dict['stargazers_count'])
    #     print('项目URL：',repo_dict['html_url'])
    #     print('仓库描述：',repo_dict['description'])
    #     print('\n')



if __name__ == '__main__':
    repos_hist()